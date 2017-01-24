from django.conf.urls import url
from . import views

app_name = 'MOOCsite'
urlpatterns = [
    url(r'^$', views.indexView, name='index'),
    url(r'^search',views.ajaxSearch2,name='autocomplete')
]