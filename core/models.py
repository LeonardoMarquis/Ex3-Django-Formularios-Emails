from django.db import models
from stdimage.models import StdImageField

# SIGNALS
from django.db.models import signals
from django.template.defaultfilters import slugify

class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True)
    modificado = models.DateField('Data de Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True


class Produto(Base):
    nome = models.CharField('Nome', max_length=100)
    preco = models.DecimalField('Preço', max_digits=8, decimal_places=2)
    estoque = models.IntegerField('Estoque')
    imagem = StdImageField('Imagem', upload_to='produtos', variations={'thumb': (124, 124)})
    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)

    def __str__(self):
        return self.nome

def produto_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.nome)
# quando o produto for salvo, ele vai gerar o slug
# ex o Maria Mole vai virar maria-mole
signals.pre_save.connect(produto_pre_save, sender=Produto)



# ===============================

class Chassi (models.Model):
    numero = models.CharField('Numero do Chassi', max_length=16, help_text='Máximo 16 caracteres')

    class Meta:
        verbose_name = 'Chassi'
        verbose_name_plural = 'Chassis'
    
    def __str__(self):
        return self.numero
    
class Montadora(models.Model):
    nome = models.CharField('Nome da Montadora', max_length=100)

    class Meta:
        verbose_name = 'Montadora'
        verbose_name_plural = 'Montadoras'
    
    def __str__(self):
        return self.nome

class Carro (models.Model):

    # models.OneToOneField
    # um para um

    # models.ForeignKey
    # um para muitos, tipo uma montadora para muitos carros


    chassi = models.OneToOneField(Chassi, on_delete=models.CASCADE)     # esse one to one é para dizer que o relacionamento de carro, vai ter 1 chassi e cada chassi so vai ter 1 carro
    montadora = models.ForeignKey(Montadora, on_delete=models.CASCADE)
    modelo = models.CharField('Modelo', max_length=100)
    preco = models.DecimalField('Preço', max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Carro'
        verbose_name_plural = 'Carros'

        def __str__(self):
            return f"{self.montadora}-{self.modelo}"