from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib import auth
from django.contrib.auth.models import User
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Reference
# Create your views here.


# class User(object):
# 	uname = ""
# 	pwd = ""
#
# 	def __init__(self, username, password):
# 		self.uname = username
# 		self.pwd = password

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
		# Retrieve references posted by logged-in user
        references_object_array = Reference.objects.filter(user_id=request.user.id)
        context = {
            'user':request.user,
			'references':references_object_array,
        }
        return render(request, 'strange_references/authenticated.html', context)

    else:
        context = {}
        return render(request, 'strange_references/invalid.html', context)


    #
    # return HttpResponse(template.render(context))

def register(request):
    username = request.POST.get('uname')
    password = request.POST.get('pwd')
    password1 = request.POST.get('pwd2')
    email = request.POST.get('email')

    # if email is already used
    if User.objects.filter(email=email).exists():
        context = {
            'error_msg':'Email already in use',
        }
        return render(request, 'strange_references/register.html', context)
    # if passwords do not match
    elif password != password1:
        context = {
            'pwd_error': 'The two passwords entered did not match please try registering again',
        }
        return render(request,'strange_references/login.html', context)
    # otherwise add user to db
    else:
        user = User.objects.create_user(username, email, password)
        user.first_name = request.POST.get('fname')
        user.last_name = request.POST.get('lname')
        user.save()
        auth.login(request,user)
        context = {
            'username': request.user.username,
            'user_id': request.user.id,
        }
        return render(request, 'strange_references/authenticated.html', context)
