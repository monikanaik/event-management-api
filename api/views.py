import json

from django.core import paginator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import User, Event, Ticket

from api.serializers import UserSerializer, EventSerializer, TicketSerializer
import pandas as pd


class RegisterUserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []


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
                {"error": "Event not found."},
                status=status.HTTP_404_NOT_FOUND,
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
            user=request.user,
            event=event,
            quantity=quantity,
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


def get_lazy_loading(request):
    data = {}
    tickets = Ticket.objects.all()
    for ticket in tickets:
        data["user"] = ticket.user.role
        data["event"] = ticket.event.name
        data["quantity"] = ticket.quantity
        data["purchase"] = ticket.purchase_date
        print(data)
    return HttpResponse("hello")


def get_select_related(request):
    tickets = Ticket.objects.select_related("event")
    page = request.GET.get("page", 1)
    size = 10

    # Use the paginator efficiently with the selected tickets
    paginator = Paginator(tickets, size)

    try:
        items_on_page = paginator.page(page)
    except PageNotAnInteger:
        items_on_page = paginator.page(1)  # Deliver the first page
    except EmptyPage:
        items_on_page = paginator.page(paginator.num_pages)  # Deliver the last page

    # Create the data dictionary using list comprehension with correct attribute access
    data = [
        {
            "user": ticket.user.role,
            "event": ticket.event.name,
            "quantity": ticket.quantity,
            "purchase_date": ticket.purchase_date,  # Use the correct attribute name
        }
        for ticket in items_on_page.object_list  # Iterate over paginated objects
    ]

    # Context dictionary with paginator information for template rendering
    context = {
        "tickets": data,
        "items": items_on_page,  # Include the paginator object for pagination logic
    }

    return render(request, "api/tickets.html", context)
