from asyncio.windows_events import NULL
from typing import Any
from django.shortcuts import render, redirect

from django.http import HttpResponse
import datetime

from .models import User, Tag, Vida, Dominio, Reino, Filo, Classe, Ordem, Familia, Genero, Especie, SubEspecie

from .forms import VidaForm

# Create your views here.
'''def home(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body><html>" % now
    return HttpResponse(html)'''

def home(request):
    return render(request, 'home/home.html')

def argu(request, name, inteiro):
    return render(request, 'home/argu.html', {'name' : name, 'inteiro' : inteiro})

def dashboard(request):
    return render(request, 'home/dashboard.html')

def tree(request):
    return render(request, 'home/tree.html')




from itertools import chain

def dbaccess(request):
    data = {}

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

    return render(request, 'home/dbaccess.html', data)

def about(request):
    return render(request, 'home/about.html')




def adicionar(request):
    data = {}
    
    form = VidaForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('url_dbaccess') 

    data['form'] = form
    return render(request, 'home/form.html', data)

def update(request, pk):
    data = {}
    obj = Vida.objects.get(pk=pk)
    form = VidaForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return redirect('url_dbaccess') 

    data['form'] = form
    return render(request, 'home/form.html', data)

def delete(request, pk):

    obj = Vida.objects.get(pk=pk)
    obj.delete()

    return redirect('url_dbaccess')