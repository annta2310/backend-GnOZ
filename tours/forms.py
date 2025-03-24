from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Tour, Agent

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2')

class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('name', 'description', 'agent', 'total_seats', 'available_seats', 'price', 'start_date', 'end_date')
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TourForm, self).__init__(*args, **kwargs)
        # If the user is an agent, they can only select themselves as the agent
        if user and user.is_agent():
            self.fields['agent'].queryset = Agent.objects.filter(user=user)
            self.fields['agent'].initial = Agent.objects.get(user=user)
            self.fields['agent'].widget = forms.HiddenInput()

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ('bio', 'phone', 'profile_pic')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')