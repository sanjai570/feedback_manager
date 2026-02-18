from django import forms
from django.contrib.auth.hashers import make_password
from .models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'name', 'role', 'status')

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Use make_password to hash
        user.password = make_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    # Read-only password field to prevent raw text edits
    password = forms.CharField(
        label="Password Hash",
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        help_text="Raw password hash. Cannot be changed directly here."
    )

    class Meta:
        model = User
        fields = ('email', 'name', 'role', 'status', 'password')

    def clean_password(self):
        return self.initial.get('password')
