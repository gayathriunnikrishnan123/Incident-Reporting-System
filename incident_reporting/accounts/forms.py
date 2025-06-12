
from django import forms
from masterdata.models import Department, Division
from accounts.models import CustomUserProfile



class UserCreationForm(forms.Form):
    email = forms.EmailField(label="Email",widget=forms.TextInput(attrs={
            'placeholder': 'someone@gmail.com',
            'autocomplete': 'email',
        }))
    fullname = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
            'placeholder': 'enter fullname',
        }))
    phone = forms.CharField(max_length=15,widget=forms.TextInput(attrs={
            'placeholder': 'enter 10-digits ',
        }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'enter password',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'confirm password',
    }))

    default_department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        empty_label="Select Department"
    )
    
    default_division = forms.ModelChoiceField(
        queryset=Division.objects.all(),
        required=False,
        empty_label="Select Division"
    )


    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if CustomUserProfile.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip().replace('-', '')
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        if CustomUserProfile.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already used.")
        return phone



    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password != confirm:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data
