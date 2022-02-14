from datetime import datetime
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm, RoomForm, PanelForm, SlotForm, StudentForm
from users.models import User
from .models import PanelRoom, PanelMember, InterviewSlot, ParticipantDetail

# Create your views here.

def loginPage(request):
    page = 'login'
    
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('panel-home')
        else:
            return redirect('student-home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        is_teacher = request.POST.get('is_teacher')
        
        try:
            user = User.objects.all(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_teacher:
                login(request, user)
                return redirect('panel-home')
            else:
                login(request, user)
                return redirect('student-home')
        else:
            messages.error(request, 'Email OR password does not exist!')
            
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    return render(request, 'base/home.html')

@login_required(login_url='login')
def panel_home(request):
    if request.user.is_teacher:
        pass
    else:
        return redirect('student-home')
    return render(request, 'base/panel_home.html')

def registerPage(request):
    form = MyUserCreationForm()
    
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            if user.is_teacher:
                return redirect('panel-home')
            else:
                return redirect('student-detail', user.id)
        else:
            messages.error(request, 'An error occured')
    
    context = {'form': form}
    return render(request, 'base/login_register.html', context)

#-------------------- Panel -------------------------
@login_required(login_url='login')
def panel_show(request, pk):
    if request.user.is_teacher:
        user = User.objects.get(id=pk)
        panels= user.panelroom_set.all()
        
        if request.user != user:
            return redirect('panel-home')
        
        participants = ParticipantDetail.objects.filter()
    else:
        return redirect('student-home')
    
    context={'panels': panels, 'participants': participants}
    return render(request, 'base/panel_show.html', context)
    
@login_required(login_url='login')
def createPanel(request, pk):
    if request.user.is_teacher:
        user = User.objects.get(id=pk)
        if request.user != user:
            return redirect('panel-home')
        
        form = RoomForm()
        panels = PanelRoom.objects.all()
        members = PanelMember.objects.all()
        
        if request.method == 'POST':
            
            #Creating Interview Slot
            date_instance = request.POST.get('set_time_0')
            time_instance = request.POST.get('set_time_1')
            name_instance = request.POST.get('panel_name')
            i = " :: "
            slot_name = name_instance + i + time_instance + i + date_instance 
            
            InterviewSlot.objects.create(
                date=request.POST.get('set_time_0'),
                time=request.POST.get('set_time_1'),
                slot=slot_name
            ) 
            
            #Creating Panel member
            panel_member=request.POST.get('panel_member')
            PanelMember.objects.create(
                member_name=panel_member
            )
            
            #Creating Panel Room (without member n slots)
            PanelRoom.objects.create(
                host=request.user,
                name=request.POST.get('panel_name'),
            )
            
            #Adding Panel member
            panel = PanelRoom.objects.filter(name=request.POST.get('panel_name'))
            if panel:
                panel = panel[0]
            member1 = PanelMember.objects.filter(member_name=panel_member)
            if member1: 
                mem = member1[0]
            panel.panel_members.add(mem)
            
            #Adding Panel interview Slot
            slot = InterviewSlot.objects.filter(slot=slot_name)
            if slot:
                slot = slot[0]
            panel.set_time.add(slot)
            return redirect('panel-home')
    else:
        return redirect('student-home')
        
    context = {'form': form, 'panels': panels, 'members': members}
    return render(request, 'base/panel_form.html', context)

@login_required(login_url='login')
def updatePanel(request, pk):
    if request.user.is_teacher:
        page = 'update'
        panel = PanelRoom.objects.get(id=pk)
        
        #Changing Slug name in Slot database to avoid disturbance
        #bcoz its name is related to panel room name
        i_slots = panel.set_time.all()
        i_slot_name = str(i_slots[0])
        name = i_slot_name.split('::')
        
        #Changing Slot database
        get_slot = InterviewSlot.objects.filter(slot__contains=name[0])
        get_slot_name = str(get_slot[0])
        prev_slot_name = get_slot_name.split('::')
        i= "::"
        
        #Panel host check
        if request.user != panel.host:
            return redirect('panel-home')
        
        form = RoomForm(instance=panel)
        members = panel.panel_members.all()
        slots = panel.set_time.all()
        
        if request.method == 'POST':
            panel.name = request.POST.get('name')
            
            #Changing Interview Slot Slug name
            slot = str(panel.name) + " " + i + prev_slot_name[1] + i + prev_slot_name[2]
            InterviewSlot.objects.filter(slot__contains=name[0]).update(slot=slot)
            
            panel.save()
            return redirect('panel-show', request.user.id)

    else:
        return redirect('student-home')
        
    context = {'page': page, 'form': form, 'panel': panel, 'members': members, 'slots': slots}
    return render(request, 'base/panel_form.html', context)

@login_required(login_url='login')
def deletePanel(request, pk):
    if request.user.is_teacher:
        panel = PanelRoom.objects.get(id=pk)
        
        temp = panel.name
        slot_temp = InterviewSlot.objects.filter(slot__contains=temp)
        
        if request.user != panel.host:
            return redirect('panel-home')
        
        if request.method == 'POST':
            slot_temp.delete()
            panel.delete()
            return redirect('panel-show', request.user.id)
    else:
        return redirect('student-home')
    
    return render(request, 'base/delete.html', {'obj': panel})

#-------------------- Panel Members ------------------------
@login_required(login_url='login')
def member_detail(request, pk):
    user = PanelMember.objects.get(id=pk)
    
    context={'user':user}
    return render(request, 'base/member_detail.html', context)

@login_required(login_url='login')
def addMembers(request, pk):
    if request.user.is_teacher:
        form = PanelForm()
        panel = PanelRoom.objects.get(id=pk)
        
        if request.user != panel.host:
            return redirect('panel-home')
        
        members = PanelMember.objects.all()
        
        if request.method == 'POST':
            form = PanelForm(request.POST)
            member__name = request.POST.get('member_name')
        
            if form.is_valid():
                member_name = form.save(commit=False)
                member_name = member__name

                PanelMember.objects.create(
                member_name=member_name,
                email = request.POST.get('email'),
                phone = request.POST.get('phone'),
                branch = request.POST.get('branch'),
            )                
                member1 = PanelMember.objects.get(member_name=member__name)
                
                panel.panel_members.add(member1)
                return redirect('panel-show', pk=request.user.id)
    else:
        return redirect('student-home')
        
    context = {'form': form, 'panel': panel, 'members': members}
    return render(request, 'base/member_form.html', context)

@login_required(login_url='login')
def updateMember(request, host, pk):
    if request.user.is_teacher:
        page = 'update'
        user = PanelMember.objects.get(id=pk)
        
        if str(request.user) != host:
            return redirect('panel-home')
        
        form = PanelForm(instance=user)
        
        if request.method == 'POST':
            user.member_name = request.POST.get('member_name')
            user.email = request.POST.get('email')
            user.phone = request.POST.get('phone')
            user.branch = request.POST.get('branch')
            
            user.save()
            return redirect('panel-show', request.user.id)
    else:
        return redirect('student-home')
    
    context={'user':user, 'form':form, 'page':page}
    return render(request, 'base/member_form.html', context)

@login_required(login_url='login')
def deleteMember(request, host, pk):
    if request.user.is_teacher:
        user = PanelMember.objects.get(id=pk)
         
        if str(request.user) != host:
            return redirect('panel-home')
        
        if request.method == 'POST':
            user.delete()
            return redirect('panel-show', request.user.id)
    else:
        return redirect('student-home')
    
    return render(request, 'base/delete.html', {'obj': user})

#-------------------- Panel Slots ------------------------
@login_required(login_url='login')
def addSlots(request, pk):
    if request.user.is_teacher:
        form = SlotForm()
        panel = PanelRoom.objects.get(id=pk)
        
        if request.user != panel.host:
            return redirect('panel-home')
        
        if request.method == 'POST':
            #Creating Interview Slot
            date_instance = request.POST.get('date_0')
            time_instance = request.POST.get('date_1')
            name_instance = panel.name
            i = " :: "
            slot_name = name_instance + i + time_instance + i + date_instance 
            
            InterviewSlot.objects.create(
                date=request.POST.get('date_0'),
                time=request.POST.get('date_1'),
                slot=slot_name
            )
            member1 = InterviewSlot.objects.get(slot=slot_name)
            panel.set_time.add(member1)
            return redirect('panel-show', pk=request.user.id)
    else:
        return redirect('student-home')
    
    context = {'form': form, 'panel': panel}
    return render(request, 'base/slot_form.html', context)

@login_required(login_url='login')
def updateSlot(request, pk):
    if request.user.is_teacher:
        page = 'update'
        i_slot = InterviewSlot.objects.get(id=pk)
        form = SlotForm()
        
        #To indirectly find PanelRoom
        panel = i_slot.panelroom_set.get()
        
        #To authenticate the correct host
        if request.user != panel.host:
                return redirect('panel-home')
            
        if request.method == 'POST':
            i_slot.date = request.POST.get('date_0')
            i_slot.time = request.POST.get('date_1')
            i = " :: "
            i_slot.slot = panel.name + i + i_slot.time + i + i_slot.date 
            
            i_slot.save()
            return redirect('panel-show', request.user.id)
    else:
        return redirect('student-home')
    
    context = {'page': page, 'form': form, 'slot':i_slot}
    return render(request, 'base/slot_form.html', context)

@login_required(login_url='login')
def deleteSlot(request, pk):
    if request.user.is_teacher:
        i_slot = InterviewSlot.objects.get(id=pk)
        
        #indirectly to find Panel name
        panel = i_slot.panelroom_set.get()
        
        #To authenticate the correct host
        if request.user != panel.host:
                return redirect('panel-home')
            
        if request.method == 'POST':
            i_slot.delete()
            return redirect('panel-show', request.user.id)
    else:
        return redirect('student-home')
    
    return render(request, 'base/delete.html', {'obj': i_slot})

#-------------------- ------------ ------------------------
#-------------------- ------------ ------------------------
#-------------------- Participants ------------------------
#-------------------- ------------ ------------------------
#-------------------- ------------ ------------------------
@login_required(login_url='login')
def participant_detail(request, pk):
    user = ParticipantDetail.objects.get(id=pk)
    
    context={'user':user}
    return render(request, 'base/participant_detail.html', context)

@login_required(login_url='login')
def student_home(request):
    if request.user.is_student:
        pass
    else:
        return redirect('panel-home')
    return render(request, 'base/student_home.html')

@login_required(login_url='login')
def studentDetail(request, pk):
    if request.user.is_student:
        user = User.objects.get(id=pk)
        form = StudentForm()

        if request.user != user:
            return redirect('student-home')
        
        if request.method == 'POST':
            form = StudentForm(request.POST)
            member_name = request.POST.get('member_name')
            
            if form.is_valid():
                member_name = user
                ParticipantDetail.objects.create(
                    id = pk,
                    member_name = member_name,
                    email = request.POST.get('email'),
                    phone = request.POST.get('phone'),
                    branch = request.POST.get('branch'),
                )
                return redirect('student-home')
    else:
        return redirect('panel-home')
    
    context = {'user': user, 'form': form}
    return render(request, 'base/student_form.html', context)

@login_required(login_url='login')
def studentUpdate(request, pk):
    if request.user.is_student:
        page = 'update'
        user = User.objects.get(id=pk)
        participant = ParticipantDetail.objects.get(id=pk)
             
        if request.user != user:
            return redirect('student-home')
        
        form = StudentForm(instance=participant)

        if request.method == 'POST':
            participant.phone = request.POST.get('phone')
            user.email = request.POST.get('email')
            participant.email = request.POST.get('email')
            participant.branch = request.POST.get('branch')
            user.save()
            
            #Participant member name must be instance of user model
            participant.member_name = user
            participant.save()
            
            return redirect('student-home')
    else:
        return redirect('panel-home')
    
    context = {'participant': participant, 'page': page, 'form': form}
    return render(request, 'base/student_form.html', context)

@login_required(login_url='login')
def joinPanel(request, pk):
    if request.user.is_student:
        
        q = request.GET.get('date_0') if request.GET.get('date_0') != None else ''
        participant = ParticipantDetail.objects.get(id=pk)
        
        form = SlotForm()
        
        user = User.objects.get(id=pk)
        if request.user != user:
            return redirect('student-home')
        
        slots = InterviewSlot.objects.order_by('date').values_list('date', flat=True).distinct()
        slots_for_id = InterviewSlot.objects.order_by('date').distinct()
        
        if request.method == 'POST':
            sk = InterviewSlot.objects.get(id=request.POST.get('date_0'))

            panel = sk.panelroom_set.all()
            panel[0].participants.add(participant)

            participant.slot_booked = sk
            participant.save()
            return redirect('student-home')

    else:
        return redirect('panel-home')
    
    context = {'participant':participant, 'form': form, 'slots': slots, 'slots_for_id': slots_for_id}
    return render(request, 'base/joinPanel_form.html', context)

# @login_required(login_url='login')
# def bookSlot(request, date, pk):
#     if request.user.is_student:
#         participant = ParticipantDetail.objects.get(id=pk)
#         user = User.objects.get(id=pk)
#         if request.user != user:
#             return redirect('student-home')
        
#         panel = PanelRoom.objects.filter(set_time__date__icontains=date)

#         if request.method == 'POST':
#             return redirect('student-home')
#     else:
#         return redirect('panel-home')
    
#     context = {'participant':participant, 'panel':panel}
#     return render(request, 'base/bookForm.html', context)