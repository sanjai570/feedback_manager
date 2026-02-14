from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from .models import Feedback, Event, StudentProfile, EventAttendance


class StudentRegistrationForm(UserCreationForm):
    """Student Registration Form with Department and Year"""
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email Address'
        })
    )
    department = forms.ChoiceField(
        choices=StudentProfile.DEPARTMENT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    year = forms.ChoiceField(
        choices=StudentProfile.YEAR_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Confirm Password'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                department=self.cleaned_data['department'],
                year=self.cleaned_data['year']
            )
        return user


class StudentAuthenticationForm(AuthenticationForm):
    """Custom Student Login Form"""
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
        })
    )


class AdminAuthenticationForm(AuthenticationForm):
    """Custom Admin Login Form"""
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
        })
    )


class EventForm(forms.ModelForm):
    """Admin Event Creation/Edit Form"""
    event_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-input',
            'type': 'datetime-local'
        })
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'venue', 'organizer', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Event Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Event Description',
                'rows': 5
            }),
            'venue': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Venue Location'
            }),
            'organizer': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Organizer Name'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-file',
                'accept': 'image/*'
            }),
        }


class EventFeedbackForm(forms.ModelForm):
    """Student Event Feedback Form"""
    rating = forms.ChoiceField(
        choices=[(i, f'{i} ★') for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'}),
        label='Rate your experience'
    )

    class Meta:
        model = Feedback
        fields = ['rating', 'feedback_message']
        widgets = {
            'feedback_message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Share your feedback about the event...',
                'rows': 6,
                'required': True,
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        feedback_message = cleaned_data.get('feedback_message')
        
        if feedback_message and len(feedback_message.strip()) < 10:
            raise forms.ValidationError("Feedback must be at least 10 characters long.")
        
        return cleaned_data


class EventAttendanceForm(forms.ModelForm):
    """Mark event attendance"""
    class Meta:
        model = EventAttendance
        fields = []


class EventFilterForm(forms.Form):
    """Filter events or feedback"""
    FILTER_CHOICES = [('', 'All Events')]
    
    event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="All Events"
    )
    rating = forms.ChoiceField(
        choices=[('', 'All Ratings')] + [(i, f'{i} ★') for i in range(1, 6)],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Search feedback...'
        })
    )


class StudentPasswordResetForm(PasswordResetForm):
    """Custom Password Reset Form for Students"""
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your registered email address'
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "No account found with this email address. Please register first."
            )
        return email


class StudentSetPasswordForm(SetPasswordForm):
    """Custom Set Password Form for Students"""
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter new password'
        })
    )
    new_password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm new password'
        })
    )
