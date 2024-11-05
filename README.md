# Gelato API

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

Este projeto é uma API RESTful contruída com **Python** e **Django Rest Framework** para controle de vendas de sorvetes e doces semelhantes.

## Como usar o projeto

Instale o Docker e o Python caso não possuir em sua maquina

obs.: Docker será usado para subir o servidor de banco de dados MySQL

### Clone o Repositório
```sh
git clone https://github.com/Hiago-Laureano/gelato-api.git
```

### Crie o arquivo .env com o comando abaixo

```sh
python generate_ENVFILE.py
```
Se o comando não funcionar e você estiver em um ambiente linux tente:
```sh
python3 generate_ENVFILE.py
```
Caso funcionar com python3, nos seguintes comandos que exister "python" cambie por "python3"


### No arquivo .env criado atualize os dados que achar necessário
```dosini
DATABASE_NAME -- nome do banco de dados
ROOT_PASSWORD -- senha do banco da dados
DATABASE_HOST -- host do banco de dados
DATABASE_PORT -- porta que o banco de dados
SECRET_KEY -- key da API
```

## Ambiente de Desenvolvimento

### Crie um ambiente virtual para instalar as dependências do python

```sh
python -m venv venv
```
### Acesse o ambiente virtual

Windows
```sh
. venv/Scripts/activate
```
Linux
```sh
. venv/bin/activate
```

### Instale as Dependências
```sh
pip install -r requirements-dev.txt
```

### Subir o serviço com o banco de dados
```sh
docker-compose -f docker-compose-dev.yml up -d
```

### Criar as migrations
```sh
python manage.py makemigrations
```

### Migrar para o banco de dados as migrations
```sh
python manage.py migrate
```

### Criar um superusuário inicial
```sh
python manage.py createsuperuser
```

### Rodar o projeto
```sh
python manage.py runserver
```

### Acessar o projeto

[http://localhost:8000](http://localhost:8000)


## API Endpoints

### Autenticação
```
POST /api/v1/token/ - Obter token access JWT [permissão: qualquer um]

CAMPOS DE /api/v1/token = [
    email[texto] <-- apenas POST - obrigatório
    password[texto] <-- apenas POST - obrigatório
    access[token JWT] <-- retorno POST
    refresh[token JWT] <-- retorno POST
]

POST /api/v1/token/refresh/ - Obter token refresh JWT [permissão: qualquer um]

CAMPOS DE /api/v1/token/refresh/ = [
    refresh[token JWT] <-- apenas POST - obrigatório
    access[token JWT] <-- retorno POST
]
```

### Produtos [Ex.: sorvetes 300ml, açai 500ml, bolo de pote pequeno, etc]

```
GET /api/v1/products/ - Obter uma lista de todos os produtos [permissão: qualquer um]

GET /api/v1/products/{id}/ - Obter um produto específico [permissão: qualquer um]

DELETE /api/v1/products/{id}/ - Deletar um produto [permissão: apenas membros da equipe]

POST /api/v1/products/ - Registrar um produto [permissão: apenas membros da equipe]

PUT /api/v1/products/{id}/ - Atualizar todos os dados de um produto [permissão: apenas membros da equipe]

PATCH /api/v1/products/{id}/ - Atualizar dados de um produto parcialmente [permissão: apenas membros da equipe]

CAMPOS DE /api/v1/products/ = [
    id[inteiro] <-- apenas GET
    name[texto] <-- obrigatório
    price[decimal com duas cadas após vírgula] <-- obrigatório
    description[texto] <-- obrigatório
    image[imagem] <-- não obrigatório
    max_complements[inteiro] <-- obrigatório
    in_stock[booleano] <-- não obrigatório
    category[inteiro - id Categoria] <-- obrigatório
    created[data]<-- apenas GET
    updated[data] <-- apenas GET
]

GET /api/v1/products//products/{id}/complements/ - Obter os complementos de um produto específico [permissão: qualquer um]

CAMPOS DE /api/v1/products/{id}/complements/ = [
    id[inteiro] <-- apenas GET
    name[texto] <-- apenas GET
    increase_value[decimal com duas cadas após vírgula] <-- apenas GET
    image[imagem] <-- apenas GET
    categories[lista de inteiros - ids Categorias] <-- apenas GET
]
```

### Complementos [Ex.: cobertura de chocolate, confete, etc]

```
GET /api/v1/complements/ - Obter uma lista de todos os complementos [permissão: qualquer um]

GET /api/v1/complements/{id}/ - Obter um complemento específico [permissão: qualquer um]

DELETE /api/v1/complements/{id}/ - Deletar um complemento [permissão: apenas membros da equipe]

POST /api/v1/complements/ - Registrar um complemento [permissão: apenas membros da equipe]

PUT /api/v1/complements/{id}/ - Atualizar todos os dados de um complemento [permissão: apenas membros da equipe]

PATCH /api/v1/complements/{id}/ - Atualizar dados de um complemento parcialmente [permissão: apenas membros da equipe]

CAMPOS DE /api/v1/complements/ = [
    id[inteiro] <-- apenas GET
    name[texto] <-- obrigatório
    increase_value[decimal com duas cadas após vírgula] <-- não obrigatório
    image[imagem] <-- não obrigatório
    categories[lista de inteiros - ids Categorias] <-- obrigatório
    created[data] <-- apenas GET
    updated[data] <-- apenas GET
]
```

### Categorias [Ex.: açai, sorvete, bolo de pote, etc]

```
GET /api/v1/categories/ - Obter uma lista de todas as categorias [permissão: qualquer um]

GET /api/v1/categories/{id}/ - Obter uma categoria específica [permissão: qualquer um]

DELETE /api/v1/categories/{id}/ - Deletar uma categoria [permissão: apenas membros da equipe]

POST /api/v1/categories/ - Registrar uma categoria [permissão: apenas membros da equipe]

PUT /api/v1/categories/{id}/ - Atualizar todos os dados de uma categoria [permissão: apenas membros da equipe]

PATCH /api/v1/categories/{id}/ - Atualizar dados de uma categoria parcialmente [permissão: apenas membros da equipe]

CAMPOS DE /api/v1/categories/ = [
    id[inteiro] <-- apenas GET
    name[texto] <-- obrigatório
    created[data] <-- apenas GET
]
```

### Usuários (Membros e clientes)

```
GET /api/v1/users/ - Obter uma lista de todos os usuários [permissão: apenas superusuários]

GET /api/v1/users/{id}/ - Obter um usuário específico [permissão: apenas superusuários ou o próprio do da conta]

DELETE /api/v1/users/{id}/ - Deletar um usuário [permissão: apenas superusuários]

POST /api/v1/users/ - Registrar um usuário [permissão: qualquer um]

PUT /api/v1/users/{id}/ - Atualizar todos os dados de um usuário [permissão: apenas superusuários ou o próprio do da conta]

PATCH /api/v1/users/{id}/ - Atualizar dados de um usuário parcialmente [permissão: apenas superusuários ou o próprio do da conta]

CAMPOS DE /api/v1/users/ = [
    id[inteiro] <-- apenas GET
    email[texto] <-- obrigatório
    password[texto] <-- obrigatório
    first_name[texto] <-- não obrigatório
    last_name[texto] <-- não obrigatório
    is_staff[booleano] <-- não obrigatório
    is_active[booleano] <-- não obrigatório
    is_superuser[booleano] <-- não obrigatório
    last_login_date[data] <-- apenas GET
    joined"[data] <-- apenas GET
]
```

### Pedidos

```
GET /api/v1/orders/ - Obter uma lista de todos os pedidos [permissão: apenas membros da equipe]

GET /api/v1/orders/{id}/ - Obter um pedido específico [permissão: apenas membros da equipe]

DELETE /api/v1/orders/{id}/ - Deletar um pedido [permissão: apenas superusuários]

POST /api/v1/orders/ - Registrar um pedido [permissão: qualquer um autenticado]

PUT /api/v1/orders/{id}/ - Atualizar todos os dados de um pedido [permissão: apenas membros da equipe]

PATCH /api/v1/orders/{id}/ - Atualizar dados de um pedido parcialmente [permissão: apenas membros da equipe]

CAMPOS DE /api/v1/orders/ = [
    id[inteiro] <-- apenas GET
    comment[texto contendo os dados do pedido, ex.: 3x sorvetes 500ml - sabor: uva, morango - complementos: calda de morango | Pagamento no pix | obs.: Caprichar] <-- obrigatório
    delivery[booleano] <-- obrigatório
    location[texto] <-- obrigatório
    status[texto] <-- não obrigatório
    active[booleano] <-- não obrigatório
    created[data] <-- apenas GET
]
```