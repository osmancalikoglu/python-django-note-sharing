from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from content.models import Category, Content, Images, Comment
from home.forms import RegisterForm, SearchForm
from home.models import Setting, ContactForm, ContactFormMessage, UserProfile, FAQ
from django.db.models import Avg


def index(request):
    setting = Setting.objects.first()
    category = Category.objects.all()
    recent_notes = Content.objects.all().filter(status='True').order_by('-created_at')[:4]
    random_notes = Content.objects.all().filter(status='True').order_by('?')[:4]
    most_liked = Content.objects.all().filter(status='True').order_by('?').order_by('comment__rate')[:4]

    context = {
        'setting': setting,
        'most_liked': most_liked,
        'category': category,
        'recent_notes': recent_notes,
        'random_notes': random_notes
    }
    return render(request, 'index.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Message sent successfully. Thanks.')
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.first()
    category = Category.objects.all()
    recent_notes = Content.objects.all().filter(status='True')[:4]
    form = ContactForm()
    context = {
        'setting': setting,
        'category': category,
        'recent_notes': recent_notes,
        'form': form
    }
    return render(request, 'contact.html', context)


def about(request):
    setting = Setting.objects.first()
    category = Category.objects.all()
    recent_notes = Content.objects.all().filter(status='True')[:4]
    context = {
        'setting': setting,
        'recent_notes': recent_notes,
        'category': category
    }
    return render(request, 'about.html', context)


def references(request):
    setting = Setting.objects.first()
    category = Category.objects.all()
    recent_notes = Content.objects.all().filter(status='True')[:4]
    context = {
        'setting': setting,
        'recent_notes': recent_notes,
        'category': category
    }
    return render(request, 'references.html', context)


def category_notes(request,id,slug):
    setting = Setting.objects.first()
    category = Category.objects.all()
    recent_notes = Content.objects.all().filter(status='True')[:4]
    categorydata = Category.objects.get(pk=id)
    contents = Content.objects.filter(category_id=id, status='True')
    context = {
        'setting': setting,
        'category': category,
        'recent_notes': recent_notes,
        'categorydata': categorydata,
        'contents': contents
    }
    return render(request, 'notes.html', context)


def note_detail(request,id,slug):
    comments = Comment.objects.filter(content_id=id, status='True')
    setting = Setting.objects.first()
    category = Category.objects.all()
    recent_notes = Content.objects.all().filter(status='True')[:4]
    notedata = Content.objects.get(pk=id, status=True)
    images = Images.objects.filter(content_id=id)
    context = {
        'comments': comments,
        'setting': setting,
        'category': category,
        'recent_notes': recent_notes,
        'notedata': notedata,
        'images': images
    }
    return render(request, 'note_detail.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, 'Login error! Please check your credentials.')
            return HttpResponseRedirect('/login')
    setting = Setting.objects.first()
    category = Category.objects.all()
    recent_notes = Content.objects.all().filter(status='True')[:4]
    context = {
        'setting': setting,
        'recent_notes': recent_notes,
        'category': category
    }
    return render(request, 'login.html', context)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                data = UserProfile()
                data.user_id = user.id
                data.image = "images/users/user.png"
                data.save()
                return HttpResponseRedirect('/')
    setting = Setting.objects.first()
    category = Category.objects.all()
    recent_notes = Content.objects.all().filter(status='True')[:4]
    form = RegisterForm()
    context = {
        'setting': setting,
        'category': category,
        'recent_notes': recent_notes,
        'form': form
    }
    return render(request, 'register.html', context)


def note_search(request):
    form = SearchForm(request.POST)
    if form.is_valid():
        setting = Setting.objects.first()
        category = Category.objects.all()
        recent_notes = Content.objects.all().filter(status='True')[:4]
        query = form.cleaned_data['query']
        notes = Content.objects.filter(title__icontains=query) # Select * from contents where title like %query%
        context = {
            'query': query,
            'notes': notes,
            'setting': setting,
            'recent_notes': recent_notes,
            'category': category
        }
        return render(request, 'notes_search.html', context)
    return HttpResponseRedirect('/')


def faq(request):
    setting = Setting.objects.first()
    category = Category.objects.all()
    recent_notes = Content.objects.all().filter(status='True')[:4]
    faqs = FAQ.objects.filter(status=True)
    context = {
        'faqs': faqs,
        'setting': setting,
        'recent_notes': recent_notes,
        'category': category
    }
    return render(request, 'faq.html', context)