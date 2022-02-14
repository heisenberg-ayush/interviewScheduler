from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    
    path('panel-home/', views.panel_home, name='panel-home'),
    
    path('panel-show/<str:pk>/', views.panel_show, name='panel-show'),
    path('create-panel/<str:pk>/', views.createPanel, name='create-panel'),
    path('update-panel/<str:pk>/', views.updatePanel, name='update-panel'),
    path('delete-panel/<str:pk>/', views.deletePanel, name='delete-panel'),
    
    path('member-detail/<str:pk>/', views.member_detail, name='member-detail'),
    path('add-members/<str:pk>/', views.addMembers, name='add-members'),
    path('update-member/<str:host>/<str:pk>/', views.updateMember, name='update-member'),
    path('delete-member/<str:host>/<str:pk>/', views.deleteMember, name='delete-member'),
    
    path('add-slots/<str:pk>/', views.addSlots, name='add-slots'),
    path('update-slot/<str:pk>/', views.updateSlot, name='update-slot'),
    path('delete-slot/<str:pk>/', views.deleteSlot, name='delete-slot'),
    
    path('student-home/', views.student_home, name='student-home'),
    path('participant-detail/<str:pk>/', views.participant_detail, name='participant-detail'),
    path('student-detail/<str:pk>/', views.studentDetail, name='student-detail'),
    path('student-update/<str:pk>/', views.studentUpdate, name='student-update'),
    path('join-panel/<str:pk>/', views.joinPanel, name='join-panel'),
    # path('book-slot/<str:date>/<str:pk>/', views.bookSlot, name='book-slot'),
]