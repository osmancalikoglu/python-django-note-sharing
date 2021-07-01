"""NoteSharing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from ckeditor_uploader import views as ckeditor_views
from django.views.decorators.cache import never_cache

from home import views

urlpatterns = [
    path('', include('home.urls')),
    path('home/', include('home.urls')),
    path('admin/', admin.site.urls),
    path('content/', include('content.urls')),
    path('user/', include('user.urls')),
    url(r'^ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
    url(r'^ckeditor/browse/', never_cache(login_required(ckeditor_views.browse)), name='ckeditor_browse'),

    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('references/', views.references, name='references'),
    path('category/<int:id>/<slug:slug>/', views.category_notes, name='category_notes'),
    path('note/<int:id>/<slug:slug>/', views.note_detail, name='note_detail'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('search/', views.note_search, name='note_search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
