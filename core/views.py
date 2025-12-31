from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect

from core.models import Produto
# Create your views here.

from .forms import ContatoForm, ProdutoModelForm

def index(request):
    context = {
        'produtos': Produto.objects.all()
    }
    return render(request, 'index.html', context)

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

    if str(request.user) != 'AnonymousUser':

        if request.method == 'POST':
            form = ProdutoModelForm(request.POST, request.FILES)  # esse request.FILES é para poder upar arquivos
            if form.is_valid():
                # prod= form.save(commit=False)  # commit false para nao salvar ainda no banco

                # print(f'Nome: {prod.nome}')
                # print(f'Preço: {prod.preco}')
                # print(f'Estoque: {prod.estoque}')
                # print(f'Imagem: {prod.imagem}')
                # do jeito acima nao salva no Banco de Dados
                form.save() # salva de fato no banco
                messages.success(request, 'Produto salvo com sucesso!')
                form = ProdutoModelForm()

            else:
                messages.error(request, 'Erro ao salvar produto. Verifique os dados preenchidos.')
        else:
            form = ProdutoModelForm()
        context = {
            'form': form
        }
        return render(request, 'produto.html', context)
    else:
        return redirect('index')