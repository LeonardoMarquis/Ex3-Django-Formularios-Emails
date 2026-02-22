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
from django.contrib.auth import get_user_model


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

def set_default_montadora():
    return Montadora.objects.get_or_create(nome='Padrao')[0]


class Carro (models.Model):

    # models.OneToOneField
    # um para um

    # models.ForeignKey
    # um para muitos, tipo uma montadora para muitos carros

    # many to many, muitos para muitos
    # carro pode ter varios motoristae e motoristas podem ter varios carros,

    chassi = models.OneToOneField(Chassi, on_delete=models.CASCADE)     # esse one to one é para dizer que o relacionamento de carro, vai ter 1 chassi e cada chassi so vai ter 1 carro
    montadora = models.ForeignKey(Montadora, on_delete=models.SET(set_default_montadora))  # se remover a montadora vai deletar o carro em cascata, por isso botamos esse CASCADE, para depois nao ficar os restos, lixo de dados
    modelo = models.CharField('Modelo', max_length=100)                 # ja que nao faz sentido um objeto existir se o vinculo dele com outro nao existir
    preco = models.DecimalField('Preço', max_digits=12, decimal_places=2)
                                                                            # mas nesse caso colocamos para se a montadora for deletada
                                                                            # botamos para deixar a montadora padrao, para nao ter um caso de se deletar uma coisa por engano nao dele
                                                                            # tar outros meio milhao de coisas


    motoristas = models.ManyToManyField(get_user_model())

    class Meta:
        verbose_name = 'Carro'
        verbose_name_plural = 'Carros'

        def __str__(self):
            return f"{self.montadora}-{self.modelo}"