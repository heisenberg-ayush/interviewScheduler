from django.db import models
from users.models import User
# from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
# from django import forms
# Create your models here.
    
class InterviewSlot(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    slot = models.SlugField()
    booked = models.BooleanField(default=False)
    
    def __str__(self):
        return self.slot
    
class PanelMember(models.Model):
    member_name = models.CharField(max_length=150)
    
    email= models.CharField(max_length=40)
    phone = models.CharField(max_length=12)
    branch = models.CharField(max_length=12, null=True)
    
    def __str__(self):
        return str(self.member_name)
    
class ParticipantDetail(models.Model):
    member_name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    email= models.CharField(max_length=40)
    phone = models.CharField(max_length=12)
    branch = models.CharField(max_length=12, null=True)
    slot_booked = models.ForeignKey(InterviewSlot, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return str(self.member_name)

class PanelRoom(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    
    panel_members = models.ManyToManyField(PanelMember, related_name='members', blank=True)
    participants = models.ManyToManyField(ParticipantDetail, related_name='participants', blank=True)
    
    set_time = models.ManyToManyField(InterviewSlot, blank=True)
    
    def __str__(self):
        return self.name