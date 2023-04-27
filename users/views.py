from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth
from django.contrib.auth.password_validation import validate_password


def cadastro(request):
    if request.method == "GET":
        return render(request,'cadastro.html')
    
    elif request.method == "POST": #pegando as requisições POST para trabalhar com os dados
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha') 
        confirmarSenha = request.POST.get('confirmar_senha')

        try:
            validate_password(senha)
        except Exception as e:
            messages.add_message(request,constants.WARNING, "A senha é fraquinha: {}".format(e))
            return render(request,'cadastro.html')

        if senha != confirmarSenha:
            messages.add_message(request,constants.ERROR, 'As senhas não coincidem')
            return render(request,'cadastro.html') 

        user = User.objects.filter(username=username)
        if user.exists():
            messages.add_message(request, constants.ERROR, "Usuário já existente")
            return render(request,'cadastro.html')
        
        if User.objects.filter(email=email).exists():
            messages.add_message(request, constants.ERROR, "email já cadastrado")
            return render(request,'cadastro.html')

        
        user = User.objects.create_user(username=username, email=email, password=senha)# criando um usuário no banco de dados
        messages.add_message(request, constants.SUCCESS,'Usuário salvo com sucesso XD!')
        return HttpResponseRedirect(reverse('login'))
    

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