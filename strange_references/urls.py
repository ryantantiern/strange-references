from django.conf.urls import url
from . import views

app_name = 'strange_references'
urlpatterns = [
    # url(r'dashboard', views.dashboard, name='dashboard'),
    url(r'^delete_reference/(?P<reference_id>[0-9]+)$', views.delete_reference, name='delete_reference'),
    url(r'^save_reference/(?P<reference_id>[0-9]+)$', views.save_reference, name='save_reference'),
    url(r'^edit_reference/(?P<reference_id>[0-9]+)$', views.edit_form, name='edit_reference'),
    url(r'^add_reference$', views.add_reference, name = 'add_reference'),
	url(r'^dashboard$', views.dashboard, name = 'dashboard'),
    url(r'^register$', views.register, name = 'register'),
	url(r'^auth$', views.authenticate, name='authenticate'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name = 'register'),
    url(r'^logout$', views.logout_account, name='logout'),
	url(r'^dashboard$', views.dashboard, name = 'dashboard'),
	url(r'^', views.login, name='login'),
	# url(r'home', views.dashboard, name='dashboard'),
]
