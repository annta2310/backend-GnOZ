from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from .models import User, Tour, Agent
from .forms import CustomUserCreationForm, TourForm, AgentForm, UserUpdateForm

class HomeView(TemplateView):
    template_name = 'tours/home.html'

# User Sign Up
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create agent profile for agent users
            if user.user_type == 'AGENT':
                Agent.objects.create(user=user)
                
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'tours/signup.html', {'form': form})

# Dashboard based on user role
@login_required
def dashboard(request):
    user = request.user
    context = {'user': user}
    
    if user.is_admin():
        context['tours'] = Tour.objects.all()
        context['agents'] = Agent.objects.all()
        context['users'] = User.objects.all()
    elif user.is_manager():
        context['tours'] = Tour.objects.all()
        context['agents'] = Agent.objects.all()
    elif user.is_agent():
        try:
            agent = Agent.objects.get(user=user)
            context['tours'] = Tour.objects.filter(agent=agent)
            context['agent'] = agent
        except Agent.DoesNotExist:
            agent = Agent.objects.create(user=user)
            context['agent'] = agent
            context['tours'] = Tour.objects.filter(agent=agent)
    
    return render(request, 'tours/dashboard.html', context)

# Tour Views
class TourListView(ListView):
    model = Tour
    template_name = 'tours/tour_list.html'
    context_object_name = 'tours'

class TourDetailView(DetailView):
    model = Tour
    template_name = 'tours/tour_detail.html'
    context_object_name = 'tour'

class TourCreateView(LoginRequiredMixin, CreateView):
    model = Tour
    form_class = TourForm
    template_name = 'tours/tour_edit.html'
    success_url = reverse_lazy('dashboard')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        if self.request.user.is_agent():
            # If agent, set the agent to their profile
            try:
                agent = Agent.objects.get(user=self.request.user)
                form.instance.agent = agent
            except Agent.DoesNotExist:
                messages.error(self.request, "You need an agent profile to create tours")
                return redirect('dashboard')
        return super().form_valid(form)

class TourUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tour
    form_class = TourForm
    template_name = 'tours/tour_edit.html'
    success_url = reverse_lazy('dashboard')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def test_func(self):
        tour = self.get_object()
        user = self.request.user
        
        # Admin and Manager can edit any tour
        if user.is_admin() or user.is_manager():
            return True
            
        # Agent can only edit their own tours
        if user.is_agent():
            try:
                agent = Agent.objects.get(user=user)
                return tour.agent == agent
            except Agent.DoesNotExist:
                return False
                
        return False

# Agent Views
class AgentListView(ListView):
    model = Agent
    template_name = 'tours/agent_list.html'
    context_object_name = 'agents'

class AgentDetailView(DetailView):
    model = Agent
    template_name = 'tours/agent_detail.html'
    context_object_name = 'agent'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tours'] = Tour.objects.filter(agent=self.object)
        return context

class AgentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Agent
    form_class = AgentForm
    template_name = 'tours/agent_edit.html'
    success_url = reverse_lazy('dashboard')
    
    def test_func(self):
        agent = self.get_object()
        user = self.request.user
        
        # Admin and Manager can edit any agent
        if user.is_admin() or user.is_manager():
            return True
            
        # Agents can only edit their own profile
        if user.is_agent():
            return agent.user == user
                
        return False
        
    def form_valid(self, form):
        # Handle user form as well if provided
        if 'first_name' in self.request.POST:
            user_form = UserUpdateForm(self.request.POST, instance=self.object.user)
            if user_form.is_valid():
                user_form.save()
        return super().form_valid(form)