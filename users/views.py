from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth


def cadastro(request):
    if request.method == "GET":
        return render(request,'cadastro.html')
    
    elif request.method == "POST": #pegando as requisições POST para trabalhar com os dados
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha') 
        confirmarSenha = request.POST.get('confirmar_senha')

        if senha != confirmarSenha:
            messages.add_message(request,constants.ERROR, 'As senhas não coincidem')
            return redirect(reverse('cadastro')) 

        user = User.objects.filter(username=username)
        if user.exists():
            messages.add_message(request, constants.ERROR, "Usuário já existente")
            return redirect(reverse('cadastro'))
        
        if User.objects.filter(email=email).exists():
            messages.add_message(request, constants.ERROR, "email já cadastrado")
            return redirect(reverse('cadastro'))

        
        user = User.objects.create_user(username=username, email=email, password=senha)# criando um usuário no banco de dados
        messages.add_message(request, constants.SUCCESS,'Usuário salvo com sucesso XD!')
        return redirect(reverse('login'))
    

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('senha')

        user = auth.authenticate(username=username,password=password) #methodo para fazer a autenticação do usuário
        if not user:
            messages.add_message(request,constants.ERROR, 'Username ou senha inválidos.')
            return redirect(reverse('login'))
        
        auth.login(request,user)
        return redirect('/eventos/novo_evento/')


    
    #TODO: validar força da senha