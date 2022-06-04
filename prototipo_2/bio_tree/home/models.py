from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    role = models.TextField(blank=True)

#----------------------------------------------------------------------------------------

class Tag(models.Model):
    nome = models.CharField(max_length=50)
    data_criação = models.DateTimeField(auto_now_add=True)
    descrição = models.TextField(null=True, blank=True)
    description_language_II = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to='imagens/', null=True, blank=True)
    image2 = models.FileField(upload_to='imagens/', null=True, blank=True)
    class Meta:
        verbose_name_plural = 'Tags'
    #resolvendo o object no admim nome melhor
    def __str__(self):
        return self.nome

class Vida(models.Model):
    nome = models.CharField(max_length=50)
    origem = models.BigIntegerField()
 
    extinção = models.BigIntegerField(null=True,  blank=True)#Se NULL ainda não foi extinto
    data_criação = models.DateTimeField(auto_now_add=True)
    descrição = models.TextField(null=True, blank=True)
    description_language_II = models.TextField(null=True, blank=True)
    
    antepassados = models.ManyToManyField('self', blank = True, symmetrical=False)
    
    image = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_2 = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_3 = models.FileField(upload_to='imagens/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, symmetrical=False, blank=True)
    class Meta:
        verbose_name_plural = 'Vidas'
    #resolvendo o object no admim nome melhor
    def __str__(self):
        return self.nome

class Dominio(models.Model):
    vida = models.ForeignKey(Vida, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    nome_popular = models.CharField(max_length=100, null=True,  blank=True)
    #---------Nivel
    origem = models.BigIntegerField()
    #origem = models.IntegerField()
    extinção = models.BigIntegerField(null=True,  blank=True)#Se NULL ainda não foi extinto
    descrição = models.TextField(null=True, blank=True)
    description_language_II = models.TextField(null=True, blank=True)
    #------------------------------------------------------------sem numero fixo de antepassados!!!!!!!!!!!!!!! OneToMany
    #antepassados = models.ForeignKey('self', on_delete=models.CASCADE,null=True,  blank=True)#!!!!!
    antepassados = models.ManyToManyField('self', blank = True, symmetrical=False)
    #------------------------------------------------------------sem numero fixo de antepassados!!!!!!!!!!!!!
    image = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_2 = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_3 = models.FileField(upload_to='imagens/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, symmetrical=False, blank=True)

    class Meta:
        verbose_name_plural = 'Dominios'
    #resolvendo o object no admim nome melhor
    def __str__(self):
        return self.nome
    
class Reino(models.Model):
    dominio = models.ForeignKey(Dominio, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    nome_popular = models.CharField(max_length=100, null=True,  blank=True)
    #---------Nivel
    origem = models.BigIntegerField()
    #origem = models.IntegerField()
    extinção = models.BigIntegerField(null=True,  blank=True)#Se NULL ainda não foi extinto
    descrição = models.TextField(null=True, blank=True)
    description_language_II = models.TextField(null=True, blank=True)
    #------------------------------------------------------------sem numero fixo de antepassados!!!!!!!!!!!!!!! OneToMany
    #antepassados = models.ForeignKey('self', on_delete=models.CASCADE, null=True,  blank=True)#!!!!!
    antepassados = models.ManyToManyField('self', blank = True, symmetrical=False)
    #------------------------------------------------------------sem numero fixo de antepassados!!!!!!!!!!!!!
    image = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_2 = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_3 = models.FileField(upload_to='imagens/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, symmetrical=False, blank=True)

    class Meta:
        verbose_name_plural = 'Reinos'
    #resolvendo o object no admim nome melhor
    def __str__(self):
        return self.nome

class Filo(models.Model):
    reino = models.ForeignKey(Reino, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    nome_popular = models.CharField(max_length=100, null=True,  blank=True)
    #---------Nivel
    origem = models.BigIntegerField()
    #origem = models.IntegerField()
    extinção = models.BigIntegerField(null=True,  blank=True)#Se NULL ainda não foi extinto
    descrição = models.TextField(null=True, blank=True)
    description_language_II = models.TextField(null=True, blank=True)
    #------------------------------------------------------------sem numero fixo de antepassados!!!!!!!!!!!!!!! OneToMany
    #antepassados = models.ForeignKey('self', on_delete=models.CASCADE, null=True,  blank=True)#!!!!!
    antepassados = models.ManyToManyField('self', blank = True, symmetrical=False)
    #------------------------------------------------------------sem numero fixo de antepassados!!!!!!!!!!!!!
    image = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_2 = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_3 = models.FileField(upload_to='imagens/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, symmetrical=False, blank=True)
    
    class Meta:
        verbose_name_plural = 'Filos'
    #resolvendo o object no admim nome melhor
    def __str__(self):
        return self.nome
    
class Classe(models.Model):
    filo = models.ForeignKey(Filo, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    nome_popular = models.CharField(max_length=100, null=True,  blank=True)
    #---------Nivel
    origem = models.BigIntegerField()
    #origem = models.IntegerField()
    extinção = models.BigIntegerField(null=True,  blank=True)#Se NULL ainda não foi extinto
    descrição = models.TextField(null=True, blank=True)
    description_language_II = models.TextField(null=True, blank=True)
    #------------------------------------------------------------sem numero fixo de antepassados!!!!!!!!!!!!!!! OneToMany
    #antepassados = models.ForeignKey('self', on_delete=models.CASCADE, null=True,  blank=True)#!!!!!
    antepassados = models.ManyToManyField('self', blank = True, symmetrical=False)
    #------------------------------------------------------------sem numero fixo de antepassados!!!!!!!!!!!!!
    image = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_2 = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_3 = models.FileField(upload_to='imagens/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, symmetrical=False, blank=True)
    class Meta:
        verbose_name_plural = 'Classes'
    #resolvendo o object no admim nome melhor
    def __str__(self):
        return self.nome

class Ordem(models.Model):
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    nome_popular = models.CharField(max_length=100, null=True,  blank=True)
    #---------Nivel
    origem = models.BigIntegerField()
    #origem = models.IntegerField()
    extinção = models.BigIntegerField(null=True,  blank=True)#Se NULL ainda não foi extinto
    descrição = models.TextField(null=True, blank=True)
    description_language_II = models.TextField(null=True, blank=True)
    #------------------------------------------------------------sem numero fixo de antepassados!!!!!!!!!!!!!!! OneToMany
    #antepassados = models.ForeignKey('self', on_delete=models.CASCADE, null=True,  blank=True)#!!!!!
    antepassados = models.ManyToManyField('self', blank = True, symmetrical=False)
    #------------------------------------------------------------sem numero fixo de antepassados!!!!!!!!!!!!!
    image = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_2 = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_3 = models.FileField(upload_to='imagens/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, symmetrical=False, blank=True)
    class Meta:
        verbose_name_plural = 'Ordens'
    #resolvendo o object no admim nome melhor
    def __str__(self):
        return self.nome

class Familia(models.Model):
    ordem = models.ForeignKey(Ordem, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    nome_popular = models.CharField(max_length=100, null=True,  blank=True)
    #---------Nivel
    origem = models.BigIntegerField()
    #origem = models.IntegerField()
    extinção = models.BigIntegerField(null=True,  blank=True)#Se NULL ainda não foi extinto
    descrição = models.TextField(null=True, blank=True)
    description_language_II = models.TextField(null=True, blank=True)
    #------------------------------------------------------------sem numero fixo de antepassados!!!!!!!!!!!!!!! OneToMany
    #antepassados = models.ForeignKey('self', on_delete=models.CASCADE, null=True,  blank=True)#!!!!!
    antepassados = models.ManyToManyField('self', blank = True, symmetrical=False)
    #------------------------------------------------------------sem numero fixo de antepassados!!!!!!!!!!!!!
    image = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_2 = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_3 = models.FileField(upload_to='imagens/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, symmetrical=False, blank=True)
    class Meta:
        verbose_name_plural = 'Familias'
    #resolvendo o object no admim nome melhor
    def __str__(self):
        return self.nome

class Genero(models.Model):
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    nome_popular = models.CharField(max_length=100, null=True,  blank=True)
    #---------Nivel
    origem = models.BigIntegerField()
    #origem = models.IntegerField()
    extinção = models.BigIntegerField(null=True,  blank=True)#Se NULL ainda não foi extinto
    descrição = models.TextField(null=True, blank=True)
    description_language_II = models.TextField(null=True, blank=True)
    #------------------------------------------------------------sem numero fixo de antepassados!!!!!!!!!!!!!!! OneToMany
    #antepassados = models.ForeignKey('self', on_delete=models.CASCADE, null=True,  blank=True)#!!!!!
    antepassados = models.ManyToManyField('self', blank = True, symmetrical=False)
    #------------------------------------------------------------sem numero fixo de antepassados!!!!!!!!!!!!!
    image = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_2 = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_3 = models.FileField(upload_to='imagens/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, symmetrical=False, blank=True)
    class Meta:
        verbose_name_plural = 'Generos'
    #resolvendo o object no admim nome melhor
    def __str__(self):
        return self.nome

class Especie(models.Model):
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    epíteto_específico = models.CharField(max_length=100)
    nome_popular = models.CharField(max_length=100, null=True,  blank=True)
    #---------Nivel
    origem = models.BigIntegerField()
    #origem = models.IntegerField()
    extinção = models.BigIntegerField(null=True,  blank=True)#Se NULL ainda não foi extinto
    descrição = models.TextField(null=True, blank=True)
    description_language_II = models.TextField(null=True, blank=True)
    #------------------------------------------------------------sem numero fixo de antepassados!!!!!!!!!!!!!!! OneToMany
    #antepassados = models.ForeignKey('self', on_delete=models.CASCADE, null=True,  blank=True)#!!!!!
    antepassados = models.ManyToManyField('self', blank = True, symmetrical=False)#!!!!!
    #------------------------------------------------------------sem numero fixo de antepassados!!!!!!!!!!!!!
    image = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_2 = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_3 = models.FileField(upload_to='imagens/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, symmetrical=False, blank=True)
    class Meta:
        verbose_name_plural = 'Especies'
    #resolvendo o object no admim nome melhor
    def __str__(self):
        return self.nome

class SubEspecie(models.Model):
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    epíteto_subespecífico = models.CharField(max_length=100)
    nome_popular = models.CharField(max_length=100, null=True,  blank=True)
    #---------Nivel
    origem = models.BigIntegerField()
    #origem = models.IntegerField()
    extinção = models.BigIntegerField(null=True,  blank=True)#Se NULL ainda não foi extinto
    descrição = models.TextField(null=True, blank=True)
    description_language_II = models.TextField(null=True, blank=True)
    #------------------------------------------------------------sem numero fixo de antepassados!!!!!!!!!!!!!!! OneToMany
    #antepassados = models.ForeignKey('self', on_delete=models.CASCADE, null=True,  blank=True)#!!!!!
    antepassados = models.ManyToManyField('self', blank = True, symmetrical=False)
    #------------------------------------------------------------sem numero fixo de antepassados!!!!!!!!!!!!!
    image = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_2 = models.FileField(upload_to='imagens/', null=True, blank=True)
    image_3 = models.FileField(upload_to='imagens/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, symmetrical=False, blank=True)
    class Meta:
        verbose_name_plural = 'Sub-Especies'
    #resolvendo o object no admim nome melhor
    def __str__(self):
        return self.nome