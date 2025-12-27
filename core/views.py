from django.shortcuts import render
from django.contrib import messages
# Create your views here.

from .forms import ContatoForm

def index(request):
    return render(request, 'index.html')

def contato(request):
    form = ContatoForm(request.POST or None) # diz que esse form vai ter dadis ou nao(so entrou na pagina)

    if str(request.method) == 'POST':
        if form.is_valid():
            form.send_mail()

            messages.success(request, 'E-mail enviado com sucesso!')        # mensagem que aparece na tela para o user
            form = ContatoForm() # limpa o form após o envio
        else:
            messages.error(request, 'Erro ao enviar e-mail. Verifique os dados preenchidos.')

    context = {
        'form': form
    }
    return render(request, 'contato.html', context)

def produto(request):
    return render(request, 'produto.html')