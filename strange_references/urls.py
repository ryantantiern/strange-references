from django.conf.urls import url

from . import views

app_name = 'strange_references'
urlpatterns = [
	url(r'^$', views.login, name='login'),
]