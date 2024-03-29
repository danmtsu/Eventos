from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Evento, Certificado
from django.contrib import messages
from django.contrib.messages import constants
import csv
from secrets import token_urlsafe
import os
from django.conf import settings
from io import BytesIO  
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageDraw, ImageFont
import sys


# Create your views here.
# criar uma validação para data de inicio e data de fim dataf>dataI
@login_required
def novo_evento(request):
    if request.method == "GET":
        return render(request, 'novo_evento.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        data_inicio = request.POST.get('data_inicio')
        data_termino = request.POST.get('data_termino')
        carga_horaria = request.POST.get('carga_horaria')

        cor_principal = request.POST.get('cor_principal')
        cor_secundaria = request.POST.get('cor_secundaria')
        cor_fundo = request.POST.get('cor_fundo')
        
        logo = request.FILES.get('logo')
        
        evento = Evento(
            criador=request.user, #criador = usuario logado
            nome=nome,
            descricao=descricao,
            data_inicio=data_inicio,
            data_termino=data_termino,
            carga_horaria=carga_horaria,
            cor_principal=cor_principal,
            cor_secundaria=cor_secundaria,
            cor_fundo=cor_fundo,
            logo=logo,
        )
    
        evento.save()
        
        messages.add_message(request, constants.SUCCESS, 'Evento cadastrado com sucesso')
        return redirect(reverse('novo_evento'))
    

def gerenciar_evento(request):
    if request.method == "GET":
        nome = request.GET.get('nome')
        eventos = Evento.objects.filter(criador=request.user)
        #realizar outros filtros
        if nome:
            eventos = eventos.filter(nome__contains=nome)
        return render(request, 'gerenciar_evento.html', {'eventos':eventos})


@login_required
def inscrever_evento(request, id):
    evento = get_object_or_404(Evento,id=id)
    if request.method == 'GET':
        return render(request, 'inscrever_evento.html',{'evento':evento})
    
    elif request.method == "POST":
        #validar se o usuário já é um participante
        evento.participantes.add(request.user)
        evento.save()

        messages.add_message(request,constants.SUCCESS,'Inscrição realizada com sucesso')

        return redirect(f'/eventos/inscrever_evento/{evento.id}/')


def participantes_evento(request, id):
    evento = get_object_or_404(Evento,id=id)
    if not evento.criador == request.user:
        raise(Http404('Deu ruim, evento não encontrado'))
    if request.method == 'GET':
        participantes = evento.participantes.all()[::3]# caso queira mostrar apenas 3 participantes adicionar isso [::3] ao final da linha
        return render(request,'participantes_evento.html', {'participantes':participantes, 'evento': evento})
    
def gerar_csv(request,id):
    evento = get_object_or_404(Evento,id=id)
    if not evento.criador == request.user:
        raise Http404('Deu ruim,evento não encontrado')
    participantes =evento.participantes.all()
    token = f'{token_urlsafe(6)}.csv'
    path = os.path.join(settings.MEDIA_ROOT, token)
    with open(path,'w',) as arq:                #abrir um arquivo com o path e com o valor de leitura
        writer = csv.writer(arq, delimiter=",")
        for participante in participantes:
            x = (participante.username, participante.email)
            writer.writerow(x)



    return redirect(f'/media/{token}')

def certificados_evento(request,id):
    evento = get_object_or_404(Evento,id=id)
    qtd_certificados = evento.participantes.all().count() - Certificado.objects.filter(evento=evento).count()
    if not evento.criador == request.user:
        raise Http404('deu ruim em cria')
    
    elif request.method == 'GET':
        return render(request,'certificados_evento.html', {'evento':evento, 'qtd_certificados':qtd_certificados, })

def gerar_certificado(request,id):
    evento = get_object_or_404(Evento, id=id)
    if not evento.criador == request.user:
        raise Http404('Esse evento não é seu')

    path_template = os.path.join(settings.BASE_DIR, 'templates/static/evento/img/template_certificado.png')
    path_fonte = os.path.join(settings.BASE_DIR, 'templates/static/fontes/arimo.ttf')
    for participante in evento.participantes.all():
        # TODO: Validar se já existe certificado desse participante para esse evento
        img = Image.open(path_template)# Abrindo a imagem para conseguir escrever os dados no certificado
        path_template = os.path.join(settings.BASE_DIR, 'templates/static/evento/img/template_certificado.png')
        draw = ImageDraw.Draw(img) #escrever na imagem
        fonte_nome = ImageFont.truetype(path_fonte, 60)#criando uma fonte com os atributos caminho e tamanho
        fonte_info = ImageFont.truetype(path_fonte, 30)
        draw.text((230, 651), f"{participante.username}", font=fonte_nome, fill=(0, 0, 0))#coordenadas onde irá escrever na imagem
        draw.text((761, 782), f"{evento.nome}", font=fonte_info, fill=(0, 0, 0))
        draw.text((816, 849), f"{evento.carga_horaria} horas", font=fonte_info, fill=(0, 0, 0))
        output = BytesIO()
        img.save(output, format="PNG", quality=100)# salvando, usando o BytesIO para salvar dentro da variavel output
        output.seek(0)
        img_final = InMemoryUploadedFile(output,'ImageField',f'{token_urlsafe(8)}.png','image/jpeg',sys.getsizeof(output),None)
        certificado_gerado = Certificado(
            certificado=img_final,
            participante=participante,
            evento=evento,
        )
        certificado_gerado.save()
    
    messages.add_message(request, constants.SUCCESS, 'Certificados gerados')
    return redirect(reverse('certificados_evento', kwargs={'id': evento.id}))

@login_required
def procurar_certificado(request,id):
    evento = get_object_or_404(Evento, id=id)
    if not evento.criador == request.user:
        raise Http404('Esse evento não é seu')
    email = request.POST.get('email')
    certificado = Certificado.objects.filter(evento=evento).filter(participante__email=email).first()#participante em si não possui o campo email, mas com o __ conseguimos buscar o campo email relacionado ao participante

    if not certificado:
        messages.add_message(request, constants.ERROR, 'Certificado não foi gerado.')
        return redirect(reverse('certificados_evento', kwargs={'id': evento.id}))
    return redirect(certificado.certificado.url)