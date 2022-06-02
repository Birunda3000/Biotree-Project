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
    data['Vida'] = Vida.objects.all()
    return render(request, 'home/home.html', data)

def create(request):
    data = {}
    form = VidaForm(data=request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('url_dbaccess')   
    data['form'] = form    
    return render(request, 'home/create.html', data)

def update(request, pk):
    object_to_update = Vida.objects.get(pk=pk)
    form = VidaForm(request.POST or None, instance=object_to_update)
    data = {}   
    data['form'] = form
    data['obj'] = object_to_update
    if form.is_valid():
        form.save()
        return redirect('url_dbaccess')
    return render(request, 'home/create.html', data)

def delete(request, pk):
    object_to_update = Vida.objects.get(pk=pk)
    object_to_update.delete()
    return redirect('url_home')

def profile(request):
    return render(request,'home/profile.html')

#TREE

def tree(request):
    return render(request, 'home/tree.html')

import numpy as np
from django.template.defaulttags import register
@register.filter
def get_item (dictionary, key):
    x = np.array(dictionary.get(key))
    return x

def dbaccess(request):
    data = {}
    vida = Vida.objects.all()
    t = {}
    for v in vida:
        t[v.name] = [x for x in v.tags.all()]
        t[v.name] = [[x.name, x.id] for x in t[v.name] ]
    data['Vida'] = vida
    data['Tags'] = t
    return render(request, 'home/dbaccess.html', data)

def about(request):
    return render(request, 'home/about.html')

def tag_detail (request, pk):
    data = {}
    object = Tag.objects.get(pk=pk)
    data['dado'] = object

    return render(request, 'home/tag_detail.html', data)