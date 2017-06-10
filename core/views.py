from django.http import request
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .forms import *
from .models import *


def logout_view(request):
    logout(request)

    return redirect('index')


def index(request):
    form = Login()
    papel = ""
    if request.POST:
        form = Login(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is None:
                messages.warning(request, "Login ou Senha incorretos")
            else:
                messages.success(request, "Login realizado com sucesso")
                login(request, user)

    if not request.user.is_anonymous():
        user = Usuario.objects.get(django_user=request.user)
        if user.tipo_usuario == 'ED':
            papel = 'Editor'
        if user.tipo_usuario == 'RH':
            papel = 'RH'
        if user.tipo_usuario == 'FO':
            papel = 'Fotografo'
        if user.tipo_usuario == 'JO':
            papel = 'Jornalista'

    return render(request, 'index.html', {'form': form, 'papel': papel})


def createUser(request):
    form = NewUser()

    if request.POST:
        form = NewUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            senha = form.cleaned_data['senha']
            nome = form.cleaned_data['nome']
            tipo = form.cleaned_data['tipo_usuario']
            email = form.cleaned_data['email']
            duser = User.objects.create_user(username=username, password=senha, first_name=nome, email=email)
            user = ''

            if tipo == 'RH':
                user = RH()
            if tipo == 'FO':
                user = Fotografo()
            if tipo == 'ED':
                user = Editor()
            if tipo == 'JO':
                user = Jornalista()
            user.save()
            user2 = Usuario(django_user=duser, pk_user=user.pk, tipo_usuario=tipo)
            user2.save()
            user.user = user2
            user.save()
            return redirect('index')

    return render(request, 'create_user.html', {'form': form})