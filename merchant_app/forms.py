from django import forms
from merchant_app.models import Job


class CreateJob(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('recruiter', 'title', 'skills',
                  'available_posts', 'description')
