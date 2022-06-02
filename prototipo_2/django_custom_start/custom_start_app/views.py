from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import *
import datetime
from .models import *

# Create your views here.

'''def home(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)'''

def home(request):
    data = {}
    data['image_test_objects'] = image_test.objects.all()
    return render(request, 'custom_start_app/home.html', data)

def create(request):
    data = {}
    form = image_testForm(data=request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('url_home')   
    data['form'] = form    
    return render(request, 'custom_start_app/create.html', data)

def update(request, pk):
    object_to_update = image_test.objects.get(pk=pk)
    form = image_testForm(request.POST or None, instance=object_to_update)
    data = {}   
    data['form'] = form
    data['obj'] = object_to_update
    if form.is_valid():
        form.save()
        return redirect('url_home')
    return render(request, 'custom_start_app/create.html', data)

def delete(request, pk):
    object_to_update = image_test.objects.get(pk=pk)
    object_to_update.delete()
    return redirect('url_home')

def profile(request):

    return render(request,'custom_start_app/profile.html')
