from django import forms
from django.forms import ModelForm
from django.core import validators
from django.core.validators import FileExtensionValidator
from flatprojectapi.models import Merges, Status

#Form to Merge two branches
class MergeForm(ModelForm):
    title = forms.CharField(max_length=30)
    description = forms.CharField(
        widget=forms.Textarea,
        validators=[validators.MinLengthValidator(10,'Field description should be at least 10 chraracters'),]
    )
    status = forms.ModelChoiceField(queryset=Status.objects.exclude(pk=2), empty_label=None)

    class Meta:
        model = Merges
        fields = ['title', 'description', 'base_branch', 'compare_branch', 'status']
        labels = {
            "title": "Title",
            "description": "Description",
            "base_branch": "Base Branch",
            "compare_branch": "Compare Branch",
            "base_branch": "Base Branch",
        }
        error_messages = {
            'title': {
                'required': "Title is required",
            },
            'description': {
                'required': "Description is required",
            },
        }

