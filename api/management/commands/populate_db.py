import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Event, Ticket

# Initialize Faker
fake = Faker()

# Get the custom User model
User = get_user_model()


class Command(BaseCommand):
    help = "Populate the database with fake data."

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to populate the database...")

        # Create fake users
        self.create_users(50)

        # Create fake events
        self.create_events(20)

        # Create fake tickets
        self.create_tickets(100)

        self.stdout.write("Database population completed successfully!")

    def create_users(self, num_users=50):
        """Create fake users with random roles."""
        roles = ["admin", "user"]
        for _ in range(num_users):
            user = User.objects.create_user(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password="password123",
                role=random.choice(roles),
            )
        self.stdout.write(f"{num_users} fake users created.")

    def create_events(self, num_events=20):
        """Create fake events."""
        for _ in range(num_events):
            Event.objects.create(
                name=fake.catch_phrase(),
                date=fake.date_this_year(),
                total_tickets=random.randint(50, 200),
                tickets_sold=random.randint(0, 50),
            )
        self.stdout.write(f"{num_events} fake events created.")

    def create_tickets(self, num_tickets=100):
        """Create fake tickets for events."""
        users = list(User.objects.all())
        events = list(Event.objects.all())

        if not users or not events:
            self.stdout.write("No users or events available to create tickets.")
            return

        for _ in range(num_tickets):
            Ticket.objects.create(
                user=random.choice(users),
                event=random.choice(events),
                quantity=random.randint(1, 5),
            )
        self.stdout.write(f"{num_tickets} fake tickets created.")
