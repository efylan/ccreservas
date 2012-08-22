# coding: latin1
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from ccreservas.forms import LoginForm
from django.contrib import auth
from django.contrib import messages

#TODO use class based views
def home(request):
    return render_to_response('index.html', {}, RequestContext(request))

def login(request):
    if request.POST:
        f = LoginForm(request.POST)
        if f.errors:
            return render_to_response('login.html', {'form':f}, RequestContext(request))
        else:
            username = f.cleaned_data['username']
            password = f.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    if request.GET:
                        next=request.GET['next']
                        return HttpResponseRedirect('%s'%next)
                    else:
                        return HttpResponseRedirect('/')
                else:
                    messages.error(request,mensaje)
                    return render_to_response('login.html', {'form':f}, 
RequestContext(request))
            else:
                mensaje = "Nombre de usuario o contraseña incorrectos."
                messages.error(request,mensaje)
                return render_to_response('login.html', {'form':f}, RequestContext(request))
    else:
        f = LoginForm()
        return render_to_response('login.html', {'form':f}, RequestContext(request))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
