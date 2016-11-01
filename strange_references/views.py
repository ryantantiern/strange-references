from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.


class User(object):
	uname = ""
	pwd = ""

	def __init__(self, username, password):
		self.uname = username
		self.pwd = password



def login(request):

	template = loader.get_template('strange_references/login.html')
	context = {}
	return HttpResponse(template.render(context, request))

def authenticate (request):
	template = loader.get_template('strange_references/dashboard.html')

	username = request.POST.get('uname')
	password = request.POST.get('pwd')

	user = User(username, password)

	context = {
		'user': user,
	}
	
	return HttpResponse(template.render(context))

