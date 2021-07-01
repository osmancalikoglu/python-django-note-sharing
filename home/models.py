from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.forms import ModelForm, TextInput, Textarea
from django.utils.safestring import mark_safe


class Setting(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır')
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    address = models.CharField(blank=True, max_length=150)
    phone = models.CharField(blank=True, max_length=15)
    fax = models.CharField(blank=True, max_length=15)
    email = models.CharField(blank=True, max_length=50)
    smtpServer = models.CharField(blank=True, max_length=20)
    smtpEmail = models.CharField(blank=True, max_length=20)
    smtpPassword = models.CharField(blank=True, max_length=10)
    smtpPort = models.CharField(blank=True, max_length=5)
    icon = models.ImageField(blank=True, upload_to='images/')
    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    aboutUs = RichTextUploadingField()
    contact = RichTextUploadingField()
    references = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ContactFormMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed')
    )
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=255)
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class ContactForm(ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name & Surname'}),
            'subject': TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'message': Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': '5'})
        }


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='images/users/')
    phone = models.CharField(blank=True, max_length=50)
    address = models.CharField(blank=True, max_length=50)
    city = models.CharField(blank=True, max_length=50)
    country = models.CharField(blank=True, max_length=50)
    school = models.CharField(blank=True, max_length=50)
    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    briefly = models.CharField(blank=True, max_length=50)

    def image_tag(self):
        return mark_safe('<img src="{}" height="50" />'.format(self.image.url))

    def __str__(self):
        return self.user.username

    def user_name(self):
        return '@' + self.user.username + ' [' + self.user.first_name + ' ' + self.user.last_name + ']'


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', 'phone', 'address', 'city', 'country', 'school', 'facebook', 'instagram', 'twitter', 'briefly']

