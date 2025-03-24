from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Home and auth
    path('', views.HomeView.as_view(), name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='tours/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Tours
    path('tours/', views.TourListView.as_view(), name='tour-list'),
    path('tours/<int:pk>/', views.TourDetailView.as_view(), name='tour-detail'),
    path('tours/new/', views.TourCreateView.as_view(), name='tour-create'),
    path('tours/<int:pk>/edit/', views.TourUpdateView.as_view(), name='tour-edit'),
    
    # Agents
    path('agents/', views.AgentListView.as_view(), name='agent-list'),
    path('agents/<int:pk>/', views.AgentDetailView.as_view(), name='agent-detail'),
    path('agents/<int:pk>/edit/', views.AgentUpdateView.as_view(), name='agent-edit'),
]