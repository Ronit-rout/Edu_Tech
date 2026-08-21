from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.accounts.models import User, Profile

class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'STUDENT'
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'bio', 'github_url', 'linkedin_url')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-background border border-outline-variant rounded-lg px-4 py-3 font-body-md text-body-md text-on-surface focus:outline-none focus:border-primary-container'}),
            'bio': forms.Textarea(attrs={'class': 'w-full bg-background border border-outline-variant rounded-lg px-4 py-3 font-body-md text-body-md text-on-surface focus:outline-none focus:border-primary-container', 'rows': 4}),
            'github_url': forms.URLInput(attrs={'class': 'w-full bg-background border border-outline-variant rounded-lg px-4 py-3 font-body-md text-body-md text-on-surface focus:outline-none focus:border-primary-container'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'w-full bg-background border border-outline-variant rounded-lg px-4 py-3 font-body-md text-body-md text-on-surface focus:outline-none focus:border-primary-container'}),
        }
