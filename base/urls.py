from django.urls import path
from . import views
from django.contrib import admin

urlpatterns= [
    path('', views.home, name="home"),
    
    path('shop/', views.shop, name="shop"),
    path('animalinfo/<str:pk>/', views.animalinfo, name="animalinfo"),
    
    path('add-animal', views.addAnimal, name = "add-animal"),
    path('update-animal/<str:pk>', views.updateAnimal, name = "update-animal"), 
    path('delete-animal/<str:pk>', views.deleteAnimal, name = "delete-animal"),
    
    
    path('facts/', views.facts, name="facts"),
    path('factinfo/<str:pk>/', views.factinfo, name="factinfo"),
    
    path('add-fact', views.addFact, name = "add-fact"),
    path('update-fact/<str:pk>', views.updateFact, name = "update-fact"), 
    path('delete-fact/<str:pk>', views.deleteFact, name = "delete-fact"),
    
    path('delete-comment/<str:pk>', views.deleteComment, name = "delete-comment"),
    path('buyAnimal/<str:pk>', views.buyAnimal, name = "buyAnimal"),
    
    path('animalOrders', views.animalOrders, name="animalOrders"),
    
    path('information', views.information, name="information"),
    
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('profile/<str:pk>', views.userProfile, name = "user-profile" ),
]