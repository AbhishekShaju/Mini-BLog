from django import forms
from .models import Post, Profile
from django.utils import timezone
from datetime import timedelta

class PostForm(forms.ModelForm):
    published_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False,
        help_text='Leave empty to publish immediately'
    )
    expires_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False,
        help_text='Leave empty for no expiration'
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'published_at', 'expires_at']
        widgets = {
            'published_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        published_at = cleaned_data.get('published_at')
        expires_at = cleaned_data.get('expires_at')
        
        if published_at and published_at <= timezone.now():
            cleaned_data['is_draft'] = False
        
        if expires_at and published_at and expires_at <= published_at:
            self.add_error('expires_at', 'Expiration date must be after published date')
        
        return cleaned_data

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'location', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
