from django.contrib import admin

# Register your models here.
from .models import PanelRoom, PanelMember, InterviewSlot, ParticipantDetail

admin.site.register(PanelRoom)
admin.site.register(PanelMember)
admin.site.register(ParticipantDetail)
admin.site.register(InterviewSlot)