from django import forms
from .models import Topic


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'row': 5, 'placeholder': 'What is your mind?'}
        ),
        max_length=4000,
        help_text='max length 4000'
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']
