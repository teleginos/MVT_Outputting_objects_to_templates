from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse
from .forms import *
from .models import Buyer, Game

# Create your views here.

def home_page(request):
    buyer_name = request.session.get('buyer_name')
    
    buyer = None
    if buyer_name:
        try:
            buyer = Buyer.objects.get(name=buyer_name)
        except Buyer.DoesNotExist:
            buyer = None
    
    
    context = {
        'buyer': buyer,
    }
    
    
    return render(request, "home_page.html", context)


def shop(request):
    games = Game.objects.all()
    
    buyer_name = request.session.get('buyer_name')
    
    buyer = None
    if buyer_name:
        try:
            buyer = Buyer.objects.get(name=buyer_name)
        except Buyer.DoesNotExist:
            buyer = None
    
    
    context = {
        'buyer': buyer,
        'games': games,
    }
    return render(request, "shop.html", context)


def shopping_cart(request):
    buyer_name = request.session.get('buyer_name')
    
    buyer = None
    if buyer_name:
        try:
            buyer = Buyer.objects.get(name=buyer_name)
        except Buyer.DoesNotExist:
            buyer = None
    
    
    context = {
        'buyer': buyer,
    }
    
    return render(request, "shopping_cart.html", context)



def authorization(request):
    info = {'err': []}
    
    form = UserAuthentication(request.POST if request.method == 'POST' else None)
    
    if request.method == 'POST':    
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                buyer = Buyer.objects.get(name=username)
                request.session['buyer_name'] = buyer.name
            except Buyer.DoesNotExist:
                buyer = None
            
            if buyer and check_password(password, buyer.password):
                buyer.login = True
                buyer.save()
                request.session['buyer_name'] = buyer.name
                return redirect('/')
            else:
                info['err'].append('Неправильное имя или пароль')

    context = {
        'form': form,
        'info': info,
    }
    
    
    return render(request, 'login_page.html', context)

def logout(request):
    buyer_name = request.session.get('buyer_name')

    if buyer_name:
        try:
            buyer = Buyer.objects.get(name=buyer_name)
            buyer.login = False
            buyer.save()
            request.session.flush()
        except Buyer.DoesNotExist:
            print('Пользователь не был найден')
    return redirect('/')

def registration(request):
    info = {'err': []}
    if request.method == 'POST':
        form = UserRegister(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            if Buyer.objects.filter(name=username).exists():
                info['err'].append('Пользователь с таким именем уже существует')
            
            if password != repeat_password:
                info['err'].append('Пароли не совпадают')
            
            # if int(age) < 18:
            #     info['err'].append('Вы не достигли 18 лет')
            
            if not info['err']:
                buyer = Buyer(name=username, password=make_password(password), age=age)
                buyer.save()
                info['success_message'] = f'Регистрация прошла успешно, {username}'
    
    else:
        form = UserRegister()


    context = {
        'info': info,
        'form': form,
    }
    return render(request, 'registration_page.html', context)