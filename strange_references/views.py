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
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
import subprocess
import hmac, hashlib
import os

from .models import Reference

def login(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('dashboard')
	else:
		template = loader.get_template('strange_references/login.html')
		context = {}
		return HttpResponse(template.render(context, request))

@login_required
def logout_account(request):
	logout(request)
	return HttpResponseRedirect('login')


def authenticate(request):
    username = request.POST.get('uname')
    password = request.POST.get('pwd')

	# Prevents direct access to URL
    if username is None or password is None:
		return HttpResponseRedirect('login')
    else:        
	    user = auth.authenticate(username=username, password=password)
	    if user is not None:
	        auth.login(request, user)
	        return HttpResponseRedirect('dashboard')
	    else:
	        context = {
            'error_msg':"Username or password is incorrect"
            }
            return render(request, 'strange_references/login.html', context)

def register(request):
    username = request.POST.get('uname')
    password = request.POST.get('pwd')
    password1 = request.POST.get('pwd2')
    email = request.POST.get('email')

	# Prevents direct access to URL
    if username is None or password is None or email is None:
		return HttpResponseRedirect('login')

    # if email is already used
    if User.objects.filter(email=email).exists():
        context = {
            'error_msg':'Email already in use',
        }
        return render(request, 'strange_references/login.html', context)
    # if passwords do not match
    elif password != password1:
        context = {
            'error_msg': 'The two passwords entered did not match please try registering again',
        }
        return render(request,'strange_references/login.html', context)
    # otherwise add user to db
    else:
        user = User.objects.create_user(username, email, password)
        user.first_name = request.POST.get('fname')
        user.last_name = request.POST.get('lname')
        user.save()
        auth.login(request,user)
        return HttpResponseRedirect('dashboard')

@login_required
def dashboard(request):
	# Retrieve references posted by logged-in user
    references_object_array = Reference.objects.filter(user_id=request.user.id).order_by('-last_modified')
    total_ref = Reference.objects.filter(user_id=request.user.id).count()
    context = {
        'user':request.user,
		'references':references_object_array,
        'total_ref':total_ref,
    }
    return render(request, 'strange_references/dashboard.html', context)

@login_required
def add_reference(request):
    user_id = request.user.id
    title = request.POST.get('title')
    note = request.POST.get('note')
    link = request.POST.get('link')
    last_modified = timezone.now()
    r = Reference(title=title, note=note, link=link, last_modified=last_modified, user_id=user_id)
    r.save()
    return HttpResponseRedirect('/dashboard')

@login_required
def save_reference(request, reference_id):
    title = request.POST.get('title')
    note = request.POST.get('note')
    link = request.POST.get('link')
    r = Reference.objects.get(pk=reference_id)
    r.title = title
    r.note = note
    r.link = link
    r.last_modified = timezone.now()
    r.save()
    return HttpResponseRedirect('/dashboard')

@login_required
def delete_reference(request, reference_id):
	r = Reference.objects.get(pk=reference_id)
	if r is not None:
		r.delete()
	return HttpResponseRedirect('/dashboard')

@login_required
def edit_form(request, reference_id):
    r = Reference.objects.get(pk=reference_id)
    context = {
        'reference':r,
    }
    return render(request, 'strange_references/edit_reference.html', context)

@login_required
def add_form(request):
    return render(request, 'strange_references/add_reference.html', {})

@csrf_exempt
def hook(request):
    if request.method != 'POST':
        return HttpResponse(status=404)

    body = request.body
    GOOD_SIG = "sha1=" + hmac.new("strange1", msg=body, digestmod=hashlib.sha1).hexdigest()
    if not hmac.compare_digest(request.META['HTTP_X_HUB_SIGNATURE'], GOOD_SIG):
        return HttpResponse("Signature invalid", status=403)
    event = request.META['HTTP_X_GITHUB_EVENT']

    if event == "push":
        # Check for branch and run deployment script
        with open("/home/ec2-user/logme.txt", "w") as myfile:
            myfile.write("got push event")
        process = subprocess.call(['/home/ec2-user/s-ref/deploy.sh'], shell=True)
        parsed_json = json.loads(body)
        
        branch = parsed_json['ref'].split("/")[2] # format: refs/heads/master
        if os.environ['DEPLOY_TYPE'] == "production" and branch == 'master':
            process = subprocess.call(['/home/ec2-user/s-ref/deploy.sh'], shell=True)
        else:
            process = subprocess.call(['/home/ec2-user/s-ref/deploy.sh'], shell=True)
        

    return HttpResponse(status=200)
