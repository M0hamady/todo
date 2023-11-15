from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

class TaskAdminForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    # Add custom form fields or override field attributes as needed
    actions = ['mark_completed']

    def mark_completed(self, request, queryset):
        queryset.update(completed=True)

    mark_completed.short_description = "Mark selected tasks as completed"


class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-class','autocomplete': 'off'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'my-class'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'my-class'}))

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]