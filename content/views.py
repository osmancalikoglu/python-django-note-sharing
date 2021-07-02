from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
from content.models import CommentForm, Comment


def index(request):
    context = {'text': 'Hello Content App'}
    return HttpResponse(context.values())


@login_required(login_url='/login')
def add_comment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user
            data = Comment()
            data.user_id = current_user.id
            data.content_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Your comment is successfully sent')
            url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(url)
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect(url)
    else:
        messages.error(request, 'Unexpected error occurred.<br>')
        return HttpResponseRedirect(url)
