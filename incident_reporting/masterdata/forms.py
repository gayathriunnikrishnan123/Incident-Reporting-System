from django import forms
from masterdata.models import Department, Division, IncidentSeverity, IncidentStatus

class DepartmentForm(forms.ModelForm):
    division = forms.ModelChoiceField(
        queryset=Division.objects.filter(is_deleted=False),  # Only active divisions
        empty_label="Select Division",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Department
        fields = ['name', 'division', 'description']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensures dropdown does not show soft-deleted divisions
        self.fields['division'].queryset = Division.objects.filter(is_deleted=False)

class DivisionForm(forms.ModelForm):

    class Meta:
        model = Division
        fields = ['name','description']
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class IncidentSeverityForm(forms.ModelForm):
    class Meta:
        model = IncidentSeverity
        fields = ['level', 'description', 'weight', 'is_active']
        widgets = {
            'level':forms.TextInput(attrs={'placeholder':'eg : Low, High '}),
            'description': forms.Textarea(attrs={'rows': 2,'placeholder':'Enter description'}),


        }

    def clean(self):
        cleaned_data = super().clean()
        level = cleaned_data.get("level")

        if level:
            normalized_level = level.strip().lower()
            qs = IncidentSeverity.objects.filter(level__iexact=normalized_level)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError("Severity already exists")
        return cleaned_data
    


class IncidentStatusForm(forms.ModelForm):
    class Meta:
        model = IncidentStatus
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name':forms.TextInput(attrs={'placeholder':'Enter status'}),
            'description': forms.Textarea(attrs={'rows': 2,'placeholder':'Enter description'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")

        if name:
            normalized_name = name.strip().lower()
            qs = IncidentStatus.objects.filter(name__iexact=normalized_name)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError("Status already exists")
        return cleaned_data


from django import forms
from .models import RoleStatusMapping

class RoleStatusMappingForm(forms.ModelForm):
    class Meta:
        model = RoleStatusMapping
        fields = ['role', 'status', 'is_active']