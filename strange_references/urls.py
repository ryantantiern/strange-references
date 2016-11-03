from django.conf.urls import url
from . import views

app_name = 'strange_references'
urlpatterns = [	
	# url(r'dashboard', views.dashboard, name='dashboard'),
    url(r'^register$', views.register, name = 'register'),
	url(r'^auth$', views.authenticate, name='authenticate'),
	url(r'^', views.login, name='login'),
	url(r'^hook$', views.hook, name='hook')
	# url(r'home', views.dashboard, name='dashboard'),

]