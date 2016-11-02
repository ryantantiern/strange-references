from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib import auth
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

def authenticate(request):
    # template = loader.get_template('strange_references/dashboard.html')

    username = request.POST.get('uname')
    password = request.POST.get('pwd')

    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        context = {
            'username': request.user.username,
            'user_id':request.user.id,
        }
        return render(request, 'strange_references/authenticated.html', context)
    else:
        return render(request, 'strange_references/invalid.html', context)


    #
    # return HttpResponse(template.render(context))

def register(request):
	context = {}
	return render(request, 'strange_references/register.html', context)
