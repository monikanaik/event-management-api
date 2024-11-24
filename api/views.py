from django.db import connection
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import User, Event, Ticket

from api.serializers import UserSerializer, EventSerializer, TicketSerializer


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EventListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != "admin":  # Check for admin role
            return Response(
                {"error": "Only admins can create events."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketPurchaseView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return Response(
                {"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND
            )

        quantity = int(request.data.get("quantity", 0))
        if quantity <= 0:
            return Response(
                {"error": "Quantity must be a positive number."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if event.tickets_sold + quantity > event.total_tickets:
            return Response(
                {"error": "Not enough tickets available."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        event.tickets_sold += quantity
        event.save()

        ticket = Ticket.objects.create(
            user=request.user, event=event, quantity=quantity
        )
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def top_3_events_by_tickets_sold():
    with connection.cursor() as cursor:
        query = """
        SELECT e.id, e.name, e.date, e.total_tickets, e.tickets_sold
        FROM api_event e
        ORDER BY e.tickets_sold DESC
        LIMIT 3;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        return [
            {
                "id": r[0],
                "name": r[1],
                "date": r[2],
                "total_tickets": r[3],
                "tickets_sold": r[4],
            }
            for r in results
        ]
