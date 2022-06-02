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

#from itertools import chain

def dbaccess(request):
    data = {}
    data['Vida'] = Vida.objects.all()
    '''    
    vida = Vida.objects.all() 
    dominio = Dominio.objects.all()
    reino = Reino.objects.all() 
    filo = Filo.objects.all()
    classe = Classe.objects.all()
    ordem = Ordem.objects.all()
    familia = Familia.objects.all()
    genero = Genero.objects.all()
    especie = Especie.objects.all()
    subespecie = SubEspecie.objects.all()   
    data['dados'] = chain(vida, dominio, reino, filo, classe, ordem, familia, genero, especie, subespecie)
    data['dados2'] = vida
    '''
    return render(request, 'home/dbaccess.html', data)

def about(request):
    return render(request, 'home/about.html')