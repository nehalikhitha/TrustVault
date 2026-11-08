
from django import forms
from .models import Document


class DocumentUploadForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = [
            "title",
            "description",
            "category",
            "file",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Enter document title"
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Enter document description",
                "rows": 4
            }),
            "category": forms.Select(),
            "file": forms.ClearableFileInput(),
        }
