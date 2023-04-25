from django.contrib import admin
from .models import Animal, Classification, Comment, Fact, OrdersAnimal
# Register your models here.

admin.site.register(Animal)
admin.site.register(Classification)
admin.site.register(Comment)
admin.site.register(Fact)
admin.site.register(OrdersAnimal)

