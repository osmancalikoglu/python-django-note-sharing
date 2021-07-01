from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm, Select, TextInput, FileInput
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır')
    )
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        p = self.parent
        while p is not None:
            full_path.append(p.title)
            p = p.parent
        return ' / '.join((full_path[::-1]))

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{}" height="50" />'.format(self.image.url))
        else:
            return None

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    image_tag.short_description = 'Image'


class Content(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır')
    )

    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    detail = RichTextUploadingField()
    file = models.FileField(blank=True, upload_to='files/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50" />'.format(self.image.url))

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    image_tag.short_description = 'Image'


class Images(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50" />'.format(self.image.url))

    image_tag.short_description = 'Image'


class ContentForm(ModelForm):
    class Meta:
        model = Content
        category = Category.objects.all()
        fields = ['category', 'title', 'slug', 'keywords', 'description', 'detail', 'image', 'file']
        widgets = {
            'category': Select(attrs={'class': 'form-control', 'placeholder': 'Category'}, choices=category),
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'slug': TextInput(attrs={'class': 'form-control', 'placeholder': 'Slug'}),
            'keywords': TextInput(attrs={'class': 'form-control', 'placeholder': 'Keywords'}),
            'description': TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'image': FileInput(attrs={'class': 'form-control', 'placeholder': 'Image'}),
            'file': FileInput(attrs={'class': 'form-control', 'placeholder': 'File'}),
            'detail': CKEditorWidget()
        }


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False')
    )
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    comment = models.CharField(max_length=200)
    rate = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']