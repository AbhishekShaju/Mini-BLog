from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to=user_directory_path)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        return reverse('user_posts', kwargs={'username': self.user.username})

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    is_draft = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} by {self.author.username}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def is_published(self):
        if not self.is_draft and self.published_at:
            return self.published_at <= timezone.now()
        return False

    def is_expired(self):
        if self.expires_at:
            return self.expires_at <= timezone.now()
        return False

    def save(self, *args, **kwargs):
        if self.published_at and self.published_at <= timezone.now():
            self.is_draft = False
        if self.expires_at and self.expires_at <= timezone.now():
            self.is_deleted = True
        super().save(*args, **kwargs)
