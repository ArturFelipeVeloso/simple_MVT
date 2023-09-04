
## Passo-a-passo MVT

Instale o python

Instale o pip

Instale o virtualenv
```bash
  pip install virtualenv
```

Crie a máquina virtual
```bash
  virtualenv venv
```

Ative a máquina virtual

Win:
```bash
  venv/Scripts/activate
```

Lin:
```bash
  source venv/bin/activate
```

Instale os módulos
```bash
  pip install django
```

Criar um projeto
```bash
  django-admin startproject BatLoja .
```

Faça as migrações
```bash
  python manage.py makemigrations
  python manage.py migrate
```

Crie o super usuário do django
```bash
  python manage.py createsuperuser
```

Suba o servidor
```bash
  python manage.py runserver
```

Agora acesse o site em:
http://127.0.0.1:8000/

Acesso o admin em:
http://127.0.0.1:8000/admin/

Crie uma pasta apps/

Dentro da pasta apps/ crie um app
```bash
  cd apps
  django-admin startapp produtos
  cd ..
```

Acesse o settings.py e coloque a aplicação em INSTALLED_APPS
```bash
  INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.produtos'
  ]
```

Acesse o apps/produtos/apps.py e altere o name
```bash
from django.apps import AppConfig

class ProdutosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.produtos'
```

Agora vamos criar nosso model em apps/produtos/models.py
```bash
from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.nome
```

Faça as migrações
```bash
  python manage.py makemigrations
  python manage.py migrate
```

Agora vamos registrar o model no Django Admin
```bash
from django.contrib import admin
from .models import Produto

admin.site.register(Produto)
```

Pronto, nosso APP já tem uma tabela de produtos, agora vamos fazer o nosso front-end, primeiro crie um arquivo urls.py dentro da pasta apps/produtos/

Dentro de apps/produtos/urls.py crie a seguinte url:
```bash
from django.urls import path
from .views import home

urlpatterns = [
    path('', home),
]
```

Agora vamos ajustar a nossa urls.py do projeto, em BatLoja/urls.py
```bash
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('produto/', include('apps.produtos.urls')),
]
```

A partir de agora temos as seguintes URLS:
```bash
127.0.0.1 -> url do foguetinho
127.0.0.1/admin/ -> url do Django Admin
127.0.0.1/produto/ -> url que nós criamos para listar os produtos
```

Porém, nossa view "home()" ainda não existe, vamos cria-la:
```bash
from django.shortcuts import render

def home(request):
    return render(request, 'home.html', data)
```

Nossa view está chamando o "home.html" que é uma página HTML que ainda não criamos, então vamos lá!

Na mesma altura do manage.py (na pasta do projeto), crie uma pasta chamada templates/

Dentro dela, cria um arquivo html, chamado templates/home.html
```bash
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <h1>Olá Mundo!</h1>
</body>

</html>
```

Só que nosso front-end ainda não está completamente pronto, agora vamos acessar o settings.py e configura-lo:

Primeiramente, importe o módulo "os" no começo do settings.py

```bash
import os
...
```

Agora procure por TEMPLATES, e vamos configurar o diretório dos nossos templates:
```bash
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'Templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

Pronto, nosso front-end está configurado, agora só subir o servidor:
```bash
  python manage.py runserver
```

Agora acesse o site em:
http://127.0.0.1:8000/produto/


Agora vamos aprender como mandar dados da VIEW para o HTML utilizando o JINJA

Na view, crie o seguinte dicionário:
```bash
  from django.shortcuts import render

  def home(request):
    data = {
        "produto":"Batmóvel",
        "valor": 10.9
    }
    return render(request, 'home.html', data)
```

E no HTML, altere as tags para receber os dados da VIEW usando as tags do JINJA = {{}}
```bash
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Document</title>
  </head>

  <body>
      <h1>{{ produto }}</h1>
      <h2>{{ valor }}</h2>
  </body>

  </html>
```

Agora você aprendeu como passar dados da view para o HTML, vamos agora aprender como pegar os dados do banco de dados e levar pro HTML

Em view, faça o seguinte comando:
```bash
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
```

Neste código importamos o Produtos de models.py e fazemos um QUERY, ou seja, vamos no banco de dados e puxamos TODOS (ALL) os registros que tem salvo. Ao final, retornamos em nosso dicionário DATA.

Agora vamos apresentar todos estes dados no HTML:
```bash
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>BatLoja</title>
  </head>

  <body>
      {% for produto in produtos %}
          <h1>{{ produto.nome }}</h1>
          <h2>{{ produto.price }}</h2>
      {% endfor %}
  </body>

  </html>
```

As tags {% %} são utilizadas para quando usamos comandos que não tem retorno. E as tags {{ }} utilizamos para tags que tem retorno. Neste exemplo, fizemos um for no jinja, e para cada produto, imprimimos seu nome e seu preço.