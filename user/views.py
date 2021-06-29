from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from content.models import Category, Content, Images
from home.models import Setting, UserProfile
from user.forms import UserUpdateForm, ProfileUpdateForm


@login_required(login_url='/login')
def index(request):
    setting = Setting.objects.first()
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'setting': setting,
        'category': category,
        'profile': profile
    }
    return render(request, 'user_profile.html', context)


@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        current_user = request.user
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
            'profile': profile
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        current_user = request.user
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {
            'form': form,
            'category': category,
            'profile': profile
        }
        return render(request, 'change_password.html', context)


@login_required(login_url='/login')
def user_notes(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    notes = Content.objects.filter(user_id=current_user.id)
    context = {
        'notes': notes,
        'category': category,
        'profile': profile
    }
    return render(request, 'user_notes.html', context)


@login_required(login_url='/login')
def user_note_detail(request,id):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    notedata = Content.objects.get(user_id=current_user.id, pk=id)
    images = Images.objects.filter(content_id=id)
    context = {
        'notedata': notedata,
        'category': category,
        'profile': profile,
        'images': images
    }
    return render(request, 'user_note_detail.html', context)
