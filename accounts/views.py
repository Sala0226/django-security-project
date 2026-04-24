from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .validators import valider_mot_de_passe
from django.core.exceptions import ValidationError


def home(request):
    return redirect('login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} !')
            return redirect('dashboard')
        else:
            messages.error(request, 'Nom d utilisateur ou mot de passe incorrect.')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        erreurs = []

        if User.objects.filter(username=username).exists():
            erreurs.append('Ce nom d utilisateur existe déjà.')

        if password != password2:
            erreurs.append('Les mots de passe ne correspondent pas.')

        try:
            valider_mot_de_passe(password)
        except ValidationError as e:
            erreurs.extend(e.messages)

        if erreurs:
            for erreur in erreurs:
                messages.error(request, erreur)
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Compte créé ! Connectez-vous.')
            return redirect('login')

    return render(request, 'accounts/register.html')


@login_required
def dashboard(request):
    users = User.objects.all()
    return render(request, 'accounts/dashboard.html', {'users': users})


# Injection SQL Vulnerabilité et Securité 
from django.db import connection

def search_vulnerable(request):
    resultats = []
    requete = ""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        requete = f"SELECT id, username, email FROM auth_user WHERE username = '{nom}'"
        with connection.cursor() as cursor:
            try:
                cursor.execute(requete)
                resultats = cursor.fetchall()
            except:
                resultats = []
    return render(request, 'accounts/search.html', {
        'resultats': resultats,
        'requete': requete,
        'mode': 'vulnerable'
    })


def search_secure(request):
    resultats = []
    requete = ""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        requete = "SELECT id, username, email FROM auth_user WHERE username = %s"
        with connection.cursor() as cursor:
            cursor.execute(requete, [nom])
            resultats = cursor.fetchall()
    return render(request, 'accounts/search.html', {
        'resultats': resultats,
        'requete': requete,
        'mode': 'secure'
    })