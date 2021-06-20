from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from content.models import Category
from home.models import Setting, ContactForm, ContactFormMessage


def index(request):
    setting = Setting.objects.first()
    category = Category.objects.all()

    context = {
        'setting': setting,
        'category' : category
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
            data.save()
            messages.success(request, 'Message sent successfully. Thanks.')
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.first()
    form = ContactForm()
    context = {'setting': setting, 'form': form}
    return render(request, 'contact.html', context)


def about(request):
    setting = Setting.objects.first()
    context = {'setting': setting}
    return render(request, 'about.html', context)


def references(request):
    setting = Setting.objects.first()
    context = {'setting': setting}
    return render(request, 'references.html', context)
