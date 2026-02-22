from django.contrib import admin

from .models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque', 'slug', 'criado', 'modificado', 'ativo')


# 
from .models import Montadora, Carro, Chassi

@admin.register(Montadora)
class MontadoraAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Chassi)
class ChassiAdmin(admin.ModelAdmin):
    list_display = ('numero',)
    # para opython 111 é int, 111, é tupla, (111) é int, (111,) é tupla

@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'preco', 'chassi', 'montadora', 'get_motoristas')

    def get_motoristas(self, obj):
        return ', '.join([m.username for m in obj.motoristas.all()])