from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Classification(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
8
class Animal(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    classification = models.ForeignKey(Classification, on_delete=models.SET_NULL, null=True)
    species = models.CharField(max_length=50)
    size = models.IntegerField()
    gender = models.CharField(max_length=50)
    diet = models.CharField(max_length=50)
    price = models.IntegerField()
    picture = models.ImageField(upload_to = 'files/picturesAnimals')
    birth = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-created']
    def __str__(self):
        return self.species
    
class Fact(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    classification = models.ForeignKey(Classification, on_delete=models.SET_NULL, null=True)
    species = models.CharField(max_length=50)
    picture = models.ImageField(upload_to = 'files/picturesFacts')
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        ordering = ['-updated', '-created']
    def __str__(self):
        return self.species
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, blank=True, null=True)
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField() 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.body[0:50]
    
        
class OrdersAnimal(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, null=True, blank=True)
    phoneNumber = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=15, null=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']
    def __str__(self):
        return str(self.animal)