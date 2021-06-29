from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from content.models import Category, Content, Images, ContentForm
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


@login_required(login_url='/login')
def user_add_note(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Content()
            data.user_id = current_user.id
            data.category = form.cleaned_data['category']
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.detail = form.cleaned_data['detail']
            data.file = form.cleaned_data['file']
            data.slug = form.cleaned_data['slug']
            data.status = 'False'
            data.save()
            messages.success(request, 'Your note was successfully inserted!')
            return HttpResponseRedirect('/user/notes')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/notes/add')
    else:
        category = Category.objects.all()
        form = ContentForm()
        current_user = request.user
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {
            'form': form,
            'category': category,
            'profile': profile
        }
        return render(request, 'user_add_note.html', context)


@login_required(login_url='/login')
def user_edit_note(request,id):
    content = Content.objects.get(id=id)
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your note was successfully updated!')
            return HttpResponseRedirect('/user/notes')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/notes/edit/' + str(id))
    else:
        form = ContentForm(instance=content)
        category = Category.objects.all()
        current_user = request.user
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {
            'form': form,
            'category': category,
            'profile': profile
        }
        return render(request, 'user_add_note.html', context)


@login_required(login_url='/login')
def user_delete_note(request,id):
    current_user = request.user
    Content.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Your note was successfully deleted!')
    return HttpResponseRedirect('/user/notes')
