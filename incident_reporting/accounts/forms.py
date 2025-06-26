from django import forms
from masterdata.models import Department, Division,IncidentStatus
from accounts.models import CustomUserProfile, Role, DepartmentProfile,RoleStatusMapping
from django.contrib.auth.forms import AuthenticationForm


class UserCreationForm(forms.Form):
    fullname = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "enter fullname",
            }
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(
            attrs={
                "placeholder": "someone@gmail.com",
                "autocomplete": "email",
            }
        ),
    )

    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={
                "placeholder": "enter 10-digits ",
            }
        ),
    )

    default_division = forms.ModelChoiceField(
        queryset=Division.objects.filter(is_deleted=False), required=False, empty_label="Select Division"
    )

    default_department = forms.ModelChoiceField(
        queryset=Department.objects.filter(is_deleted=False),
        required=False,
        empty_label="Select Department",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "enter password",
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "confirm password",
            }
        )
    )
    is_active = forms.BooleanField(required=False, initial=True)
    is_staff = forms.BooleanField(required=False)
    is_admin = forms.BooleanField(required=False)

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if CustomUserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
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


class InternalUserEditForm(forms.Form):
    fullname = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "enter fullname",
            }
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(
            attrs={
                "placeholder": "someone@gmail.com",
                "autocomplete": "email",
            }
        ),
    )

    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={
                "placeholder": "enter 10-digits ",
            }
        ),
    )
    default_department = forms.ModelChoiceField(
        queryset=Department.objects.filter(is_deleted=False),
        required=False,
        empty_label="Select Department",
    )
    default_division = forms.ModelChoiceField(
        queryset=Division.objects.filter(is_deleted=False), required=False, empty_label="Select Division"
    )
    is_active = forms.BooleanField(required=False)
    is_staff = forms.BooleanField(required=False)
    is_admin = forms.BooleanField(required=False)


class CustomEmailLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"autofocus": True})
    )


class RoleCreationForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "enter role",
            }
        ),
    )
    description = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "enter description",
            }
        ),
    )

    class Meta:
        model = Role
        fields = ["name", "description", "level"]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")

        if name:
            normalized_name = name.strip().lower()
            qs = Role.objects.filter(name__iexact=normalized_name)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError("Role name already exists")
        return cleaned_data




class DepartmentProfileForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=CustomUserProfile.objects.filter(is_deleted=False), empty_label="Select User"
    )
    division = forms.ModelChoiceField(
        queryset=Division.objects.filter(is_deleted=False), required=False, empty_label="Select Division"
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(is_deleted=False),
        required=False,
        empty_label="Select Department",
    )
    role = forms.ModelChoiceField(
        queryset=Role.objects.filter(is_deleted=False), empty_label="Select Role"
    )

    class Meta:
        model = DepartmentProfile
        fields = ["user", "division", "department", "role", "is_active"]


class StatusProfileForm(forms.ModelForm):

    role = forms.ModelChoiceField(
        queryset=Role.objects.filter(is_deleted=False), empty_label="Select Role"
    )
    status = forms.ModelChoiceField(
        queryset=IncidentStatus.objects.filter(is_deleted=False), empty_label="Select Status"
    )

    class Meta:
        model = RoleStatusMapping
        fields = ["role", "status"]