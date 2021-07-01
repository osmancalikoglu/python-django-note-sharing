from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    url(r'^add_comment/(?P<id>\d+)', views.add_comment, name='add_comment'),
    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
]