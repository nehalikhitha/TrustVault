
from django import forms
from django.contrib.auth import get_user_model

from .models import DocumentPermission

User = get_user_model()


class DocumentShareForm(forms.ModelForm):

    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        label="Select User"
    )

    class Meta:
        model = DocumentPermission
        fields = ["user", "access_level"]

        widgets = {
            "access_level": forms.Select()
        }
