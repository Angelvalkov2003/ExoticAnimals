from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Animal, Classification, Comment, Fact, OrdersAnimal
from .forms import AnimalForm, FactForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test



# Create your views here.
def home(request):
    return render(request, 'home.html')

def shop(request):
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ''

    animals = Animal.objects.filter(
        Q(classification__name__icontains=q) |
        Q(species__icontains = q) 
    )
    
    
    
    classifications = Classification.objects.all()
    animal_count = animals.count()
    animal_comments = Comment.objects.filter(Q(animal__classification__name__icontains = q))
    context = {'animals' : animals, 'classifications' : classifications, 'animal_count' : animal_count, 'animal_comments': animal_comments}
    return render(request, 'shop.html', context)

def animalinfo(request, pk):
    animal = Animal.objects.get(id=pk)
    animal_comments = animal.comment_set.all()
    
    if request.method == "POST":
        comment = Comment.objects.create(
            user = request.user,
            animal = animal,
            body = request.POST.get('body')
        )
        return redirect('animalinfo', pk = animal.id)
    context = {'animal':animal, 'animal_comments': animal_comments}
    return render(request, 'animalinfo.html', context)

@user_passes_test(lambda u: u.is_superuser)
def addAnimal(request):
    form = AnimalForm()
    classifications = Classification.objects.all()
    if request.method == "POST":
        form = AnimalForm(request.POST, request.FILES)
        classification_name = request.POST.get('classification')
        classification, create = Classification.objects.get_or_create(name=classification_name)
        Animal.objects.create(
            host=request.user,
            classification = classification,
            species = request.POST.get('species'),
            size = request.POST.get('size'),
            gender = request.POST.get('gender'),
            diet = request.POST.get('diet'),
            price = request.POST.get('price'),
            picture = request.FILES.get('picture'),
            birth = request.POST.get('birth'),
            description = request.POST.get('description'),
            )
        return redirect('shop')
    context = {'form': form, 'classifications':classifications}
    return render(request, 'animal_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def updateAnimal(request, pk):
    animal = Animal.objects.get(id=pk)
    form = AnimalForm(instance=animal)
    classifications = Classification.objects.all()
    if request.method == "POST":
        form = AnimalForm(request.POST, request.FILES)
        classification_name = request.POST.get('classification')
        classification, created = Classification.objects.get_or_create(name=classification_name)
        animal.species = request.POST.get('species')
        animal.classification = classification
        animal.size = request.POST.get('size')
        animal.gender = request.POST.get('gender')
        animal.diet = request.POST.get('diet')
        animal.price = request.POST.get('price')
        animal.picture = request.FILES.get('picture')
        animal.birth = request.POST.get('birth')
        animal.description = request.POST.get('description')
        animal.save()
        return redirect('shop')
        
    context = {'form': form, 'classifications':classifications}
    return render(request, 'animal_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def deleteAnimal(request, pk):
    animal = Animal.objects.get(id=pk)
    if request.method == "POST":
        animal.delete()
        return redirect('shop')
    return render(request, 'delete.html', {'obj': animal})

def facts(request):
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ''

    facts = Fact.objects.filter(
        Q(classification__name__icontains=q) |
        Q(species__icontains = q) 
    )
        
    classifications = Classification.objects.all()
    fact_count = facts.count()
    fact_comments = Comment.objects.filter(Q(fact__classification__name__icontains = q))
    context = {'facts' : facts, 'classifications' : classifications, 'fact_count' : fact_count, 'fact_comments': fact_comments}
    return render(request, 'facts.html', context)

def factinfo(request, pk):
    fact = Fact.objects.get(id=pk)
    fact_comments = fact.comment_set.all()
    if request.method == "POST":
        comment = Comment.objects.create(
            user = request.user,
            fact = fact,
            body = request.POST.get('body')
        )
        return redirect('factinfo', pk = fact.id)
    context = {'fact':fact, 'fact_comments': fact_comments}
    return render(request, 'factinfo.html', context)

@user_passes_test(lambda u: u.is_superuser)
def addFact(request):
    form = FactForm()
    classifications = Classification.objects.all()
    if request.method == "POST":
        classification_name = request.POST.get('classification')
        classification, create = Classification.objects.get_or_create(name=classification_name)
        Fact.objects.create(
            host=request.user,
            classification = classification,
            species = request.POST.get('species'),
            picture = request.FILES.get('picture'),
            description = request.POST.get('description'),
            )
        return redirect('facts')
    context = {'form': form, 'classifications':classifications}
    return render(request, 'fact_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def updateFact(request, pk):
    fact = Fact.objects.get(id=pk)
    form = FactForm(instance=fact)
    classifications = Classification.objects.all()
    if request.method == "POST":
        classification_name = request.POST.get('classification')
        classification, created = Classification.objects.get_or_create(name=classification_name)
        fact.species = request.POST.get('species')
        fact.classification = classification
        fact.picture = request.FILES.get('picture')
        fact.description = request.POST.get('description')
        fact.save()
        return redirect('facts')      
    context = {'form': form, 'classifications':classifications}
    return render(request, 'fact_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def deleteFact(request, pk):
    fact = Fact.objects.get(id=pk)
    if request.method == "POST":
        fact.delete()
        return redirect('facts')
    return render(request, 'delete.html', {'obj': fact})


@login_required(login_url='login')
def buyAnimal(request, pk):
    animal = Animal.objects.get(id=pk)
    if request.method == "POST":
        OrdersAnimal.objects.create(
            customer=request.user,
            animal=animal,
            phoneNumber=request.POST.get('phoneNumber'),
            email=request.POST.get('email'),
        )
        return redirect('shop')
    return render(request, 'buyAnimal.html', {'obj': animal})


@login_required(login_url='login')
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.user != comment.user:
        return HttpResponse("You are not allowed here")
    if request.method == "POST":
        comment.delete()
        return redirect('shop')
    return render(request, 'delete.html', {'obj': comment})

@user_passes_test(lambda u: u.is_superuser)
def animalOrders(request):
    ordersAnimals = OrdersAnimal.objects.all()
    context = {"ordersAnimals": ordersAnimals}
    return render(request, 'animalOrders.html', context)


def information(request):
    return render(request, 'information.html')


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect("home")
    if request.method=='POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong password')
    context = {'page': page}
    return render(request, 'login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            redirect('home')
        else:
            messages.error(request, 'An error accured during registration')
    context = {'form': form}
    return render(request, 'login_register.html', context)

@login_required(login_url='login')
def userProfile(request, pk):
    user= User.objects.get(id=pk)
    ordersAnimals = OrdersAnimal.objects.filter(customer = user)
    context = {'user': user, 'ordersAnimals': ordersAnimals}
    return render(request, 'profile.html', context)
