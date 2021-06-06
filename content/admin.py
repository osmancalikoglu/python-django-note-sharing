from django.contrib import admin

# Register your models here.
from content.models import Category, Content, Images


class ContentImageInline(admin.TabularInline):
    model = Images
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag', 'status']
    list_filter = ['status']
    readonly_fields = ['image_tag']


class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image_tag', 'status']
    list_filter = ['category', 'status']
    inlines = [ContentImageInline]
    readonly_fields = ['image_tag']


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'image_tag']
    readonly_fields = ['image_tag']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Images, ImagesAdmin)
