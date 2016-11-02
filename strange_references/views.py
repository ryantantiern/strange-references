from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

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

def logout_account(request):
	logout(request)
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
        references_object_array = Reference.objects.filter(user_id=request.user.id).order_by('-last_modified')
        context = {
            'user':request.user,
			'references':references_object_array,
        }
        return render(request, 'strange_references/dashboard.html', context)

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
            'user':request.user,
        }
        return render(request, 'strange_references/authenticated.html', context)

def dashboard(request):
    context = {}
    return render(request,'strange_references/dashboard.html',context)

def add_reference(request):
	user_id = request.user.id
	title = request.POST.get('title')
	note = request.POST.get('note')
	link = request.POST.get('link')
	last_modified = timezone.now()
	r = Reference(title=title, note=note, link=link, last_modified=last_modified, user_id=user_id)
	r.save()

def save_reference(request):
	reference_id = request.POST.get('id')
	title = request.POST.get('title')
	note = request.POST.get('note')
	link = request.POST.get('link')
	r = Reference.objects.get(pk=reference_id)
	r.title = title
	r.note = note
	r.link = link
	r.last_modified = timezone.now()
	r.save()

def delete_reference(request):
	reference_id = request.POST.get('id')
	r = Reference.objects.get(pk=reference_id)
	r.delete()
