from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def novo_evento(request):
    if request.method == "GET":
        return render(request,'novo_evento.html')