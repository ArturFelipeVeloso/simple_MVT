from django.shortcuts import render
from .models import Produto

def home(request):
    produtos = Produto.objects.all()

    data = {
        "produto":"Batmóvel",
        "valor": 10.9,
        "produtos": produtos
    }
    return render(request, 'home.html', data)