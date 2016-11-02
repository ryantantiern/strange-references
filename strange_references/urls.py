from django.conf.urls import url
from . import views

app_name = 'strange_references'
urlpatterns = [
    # url(r'dashboard', views.dashboard, name='dashboard'),
    url(r'^add_reference$', views.add_reference, name = 'add_reference'),
	url(r'^dashboard$', views.dashboard, name = 'dashboard'),
    url(r'^register$', views.register, name = 'register'),
	url(r'^auth$', views.authenticate, name='authenticate'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name = 'register'),
    url(r'^logout$', views.logout_account, name='logout'),
    url(r'^auth$', views.authenticate, name='authenticate'),
	url(r'^dashboard$', views.dashboard, name = 'dashboard'),
	url(r'^', views.login, name='login'),
	# url(r'home', views.dashboard, name='dashboard'),
]
