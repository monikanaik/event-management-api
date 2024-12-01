from django.contrib import admin

from app.models import Ticket
from app.models import User, Event

# Register your models here.
admin.site.register(User)
admin.site.register(Event)
admin.site.register(Ticket)
