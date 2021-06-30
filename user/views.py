from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin

from content.models import Category, Content, Images, ContentForm
from home.models import Setting, UserProfile
from user.forms import UserUpdateForm, ProfileUpdateForm, ContentImageForm, ContentImageFormSet


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
        content_form = ContentForm(request.POST, request.FILES)
        image_form = ContentImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())
        if content_form.is_valid() and image_form.is_valid():
            current_user = request.user
            data = Content()
            data.user_id = current_user.id
            data.category = content_form.cleaned_data['category']
            data.title = content_form.cleaned_data['title']
            data.keywords = content_form.cleaned_data['keywords']
            data.description = content_form.cleaned_data['description']
            data.image = content_form.cleaned_data['image']
            data.detail = content_form.cleaned_data['detail']
            data.file = content_form.cleaned_data['file']
            data.slug = content_form.cleaned_data['slug']
            data.status = 'False'
            data.save()
            for form in image_form.cleaned_data:
                # this helps to not crash if the user
                # do not upload all the photos
                if form:
                    title = form['title']
                    image = form['image']
                    record = Images(content=data, title=title, image=image)
                    record.save()
            messages.success(request, 'Your note was successfully inserted!')
            return HttpResponseRedirect('/user/notes')
        else:
            messages.error(
                request,
                'Please correct the error below.<br>' +
                'Content Form Errors:<br>' +
                str(content_form.errors) +
                '<br>Image Form Errors:<br> '
                + str(image_form.errors)
            )
            return HttpResponseRedirect('/user/notes/add')
    else:
        category = Category.objects.all()
        content_form = ContentForm()
        image_form = ContentImageFormSet()
        current_user = request.user
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {
            'content_form': content_form,
            'image_form': image_form,
            'category': category,
            'profile': profile,
            'type': 'add'
        }
        return render(request, 'user_add_note.html', context)


@login_required(login_url='/login')
def user_edit_note(request,id):
    content = Content.objects.get(id=id)
    images = Images.objects.filter(content_id=content.id)
    if request.method == 'POST':
        content_form = ContentForm(request.POST, request.FILES, instance=content)
        image_form = ContentImageFormSet(request.POST, request.FILES, queryset=images)
        if content_form.is_valid() and image_form.is_valid():
            content_form.save()
            for form in image_form.cleaned_data:
                # this helps to not crash if the user
                # do not upload all the photos
                if form:
                    title = form['title']
                    image = form['image']
                    record = Images(content=content, title=title, image=image)
                    record.save()
            messages.success(request, 'Your note was successfully updated!')
            return HttpResponseRedirect('/user/notes')
        else:
            messages.error(
                request,
                'Please correct the error below.<br>' +
                'Content Form Errors:<br>' +
                str(content_form.errors) +
                '<br>Image Form Errors:<br> '
                + str(image_form.errors)
            )
            return HttpResponseRedirect('/user/notes/edit/' + str(id))
    else:
        content_form = ContentForm(instance=content)
        image_form = ContentImageFormSet(instance=images)
        category = Category.objects.all()
        current_user = request.user
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {
            'content_form': content_form,
            'image_form': image_form,
            'category': category,
            'profile': profile,
            'type': 'edit'
        }
        return render(request, 'user_add_note.html', context)


class ContentImageEditView(SingleObjectMixin, FormView):
    model = Content
    template_name = 'user_add_note.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Content.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Content.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return ContentImageFormSet(**self.get_form_kwargs(), instance=self.object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_form = ContentForm(instance=self.object)
        category = Category.objects.all()
        current_user = self.object.user
        profile = UserProfile.objects.get(user_id=current_user.id)
        context['category'] = category
        context['content_form'] = content_form
        context['profile'] = profile
        context['type'] = 'edit'
        return context

    def form_valid(self, form):
        form.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes were saved.'
        )
        return HttpResponseRedirect('/user/notes')


@login_required(login_url='/login')
def user_delete_note(request,id):
    current_user = request.user
    Content.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Your note was successfully deleted!')
    return HttpResponseRedirect('/user/notes')


@login_required(login_url='/login')
def user_notes_gallery(request,id):
    category = Category.objects.all()
    images = Images.objects.filter(content_id=id)
    context = {
        'category': category,
        'images': images
    }
    return render(request, 'user_note_gallery_modal.html', context)
