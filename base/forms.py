from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from users.models import User
from .models import InterviewSlot, PanelRoom, PanelMember, ParticipantDetail

from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'is_student', 'is_teacher', 'password1', 'password2']
        
class RoomForm(ModelForm):
    class Meta:
        model= PanelRoom
        fields = '__all__'
        widgets = {'set_time': forms.widgets.SplitDateTimeWidget(date_attrs={'type': 'date'}, time_attrs={'type': 'time'})}
        date_input = forms.DateField(widget=AdminDateWidget(), required=False)
        time_input = forms.TimeField(widget=AdminTimeWidget(), required=False)
        exclude = ['host', 'participants', 'panel_members']
        
class PanelForm(ModelForm):
    class Meta:
        model = PanelMember
        fields = '__all__'
        exclude = ['member_name']
        
class SlotForm(ModelForm):
    class Meta:
        model = InterviewSlot
        fields = ['date']
        
        widgets = {'date': forms.widgets.SplitDateTimeWidget(date_attrs={'type': 'date'}, time_attrs={'type': 'time'})}
        date_input = forms.DateField(widget=AdminDateWidget(), required=False)
        time_input = forms.TimeField(widget=AdminTimeWidget(), required=False)
        exclude = ['host', 'participants', 'panel_members']
        
class StudentForm(ModelForm):
    class Meta:
        model = ParticipantDetail
        fields = '__all__'
        exclude = ['member_name', 'slot_booked']