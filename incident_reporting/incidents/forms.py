from django import forms
from incidents.models import Incident, IncidentSeverity, IncidentStatus,IncidentQuestion, IncidentAnswer
from masterdata.models import Division, Department


class IncidentForm(forms.ModelForm):
    file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'multiple': True}),
        label="Attach files (optional)"
    )
    division = forms.ModelChoiceField(
        queryset=Division.objects.filter(is_deleted=False),
        empty_label="Select Division",
        required=False,
        widget=forms.Select()
    )

    priority=forms.ModelChoiceField(
        queryset=IncidentSeverity.objects.filter(is_deleted=False),
        empty_label="Select Severity",
        required=False,
        widget=forms.Select()
    )
    class Meta:
        model = Incident
        fields = [
            'title',
            'description',
            'division',
            'department',
            'priority',
            'email',
            'phone',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter incident title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe the issue'}),
            'department': forms.Select(),
            'email': forms.EmailInput(attrs={'placeholder': 'Optional'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Optional'}),
        }
        labels = {
            'title': 'Incident Title',
            'description': 'Description',
            'division': 'Select Division (optional)',
            'department': 'Select Department (optional)',
            'priority': 'Priority (optional)',
            'email': 'Your Email (optional)',
            'phone': 'Your Phone (optional)',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError("Phone number should contain digits only.")
        return phone






class IncidentStatusUpdateForm(forms.ModelForm):
    status = forms.ModelChoiceField(
        queryset=IncidentStatus.objects.filter(is_deleted=False),
        empty_label="Select Status",
        required=True,
        widget=forms.Select())
    transfer_reason = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}))
    to_division = forms.ModelChoiceField(queryset=Division.objects.filter(is_deleted=False),empty_label="Select Division", required=False)
    to_department = forms.ModelChoiceField(queryset=Department.objects.filter(is_deleted=False), required=False)
    class Meta:
        model = Incident
        fields = ['status']


class DynamicIncidentAnswerForm(forms.Form):
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if questions:
            for question in questions:
                self.fields[f"question_{question.id}"] = forms.CharField(
                    label=question.question_text,
                    required=question.is_required
                )
class IncidentQuestionForm(forms.ModelForm):
    class Meta:
        model = IncidentQuestion
        fields = ['department', 'question_text', 'is_required']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'question_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your question'}),
            'is_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'department': 'Select Department',
            'question_text': 'Question Text',
            'is_required': 'Is Required?',
        }