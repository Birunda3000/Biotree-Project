from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User (AbstractUser):
    user_image = models.ImageField(upload_to='user_images/',blank=True)
    user_description = models.TextField(blank=True)

class image_test(models.Model):
    name = models.CharField(blank=True, max_length=100)
    image = models.ImageField(upload_to='images_test_folder/',blank=True)

    class Meta:
        verbose_name_plural = 'image_tests'
    #resolvendo o object no admim nome melhor
    def __str__(self):
        return self.name



class Taxon(models.Model):
    name = models.CharField(blank=True, max_length=100)
    description = models.TextField(blank=True)
    class Meta:
        verbose_name_plural = 'Taxons'
    #resolvendo o object no admim nome melhor
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(blank=True, max_length=100)
    description = models.TextField(blank=True)
    class Meta:
        verbose_name_plural = 'Tags'
    #resolvendo o object no admim nome melhor
    def __str__(self):
        return self.name

class Vida(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(Taxon, on_delete=models.CASCADE,null=True,  blank=True)#!!!!!

    origin = models.BigIntegerField()
    extintion = models.BigIntegerField(null=True,  blank=True)#Se NULL ainda não foi extinto
    
    creation_date = models.DateTimeField(auto_now_add=True)
    
    ancestors = models.ManyToManyField('self', blank = True, symmetrical=False)
    
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_3 = models.ImageField(upload_to='images/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, symmetrical=False, blank=True)

    description = models.TextField(null=True, blank=True)
    description_language_II = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Vidas'
    #resolvendo o object no admim nome melhor
    def __str__(self):
        return self.name