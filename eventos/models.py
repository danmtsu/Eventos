from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Evento(models.Model):
    criador =models.ForeignKey(User,on_delete=models.DO_NOTHING, null=True, blank=True)
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_termino = models.DateField()
    carga_horaria = models.IntegerField() #apenas cargas horárias com vindo como int
    logo = models.ImageField(upload_to="logos")
    participantes = models.ManyToManyField(User, related_name='evento_participante',null=True,blank=True)

    #paleta de cores
    cor_principal = models.CharField(max_length=7)
    cor_secundaria = models.CharField(max_length=7)
    cor_fundo = models.CharField(max_length=7)


    def __str__(self) -> str:
        return self.nome
    #executar python3 manage.py makemigrations para criar as migrações dessa classe e o python3 manage.py migrate para criar o banco com as migrações

class Certificado(models.Model):
    certificado = models.ImageField(upload_to='certificados')
    participante = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)