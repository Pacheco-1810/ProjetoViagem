# ViajeMais

Site de agência de turismo desenvolvido em **Django**, com vitrine de pacotes, carrinho de compras, sistema de níveis com desconto, formulário de orçamento e painel administrativo (Django Admin).

## Funcionalidades

- **Início:** destaque promocional e carrossel com os destinos escolhidos no admin.
- **Pacotes:** listagem dos pacotes ativos e carrinho lateral (adicionar, remover e finalizar compra).
- **Cadastro e login:** autenticação nativa do Django, com login por e-mail.
- **Meu Perfil:** dashboard com nível atual, desconto, total gasto, progresso até o próximo nível e histórico de viagens.
- **Contato:** formulário de orçamento personalizado, salvo no banco de dados.
- **Sobre:** página institucional.
- **Admin:** gerenciamento de pacotes, compras, pedidos de orçamento e usuários.

## Tecnologias

- Python 3.10+
- Django 5+
- Pillow (upload de imagens)
- SQLite (padrão)
- Bootstrap 5.3 (via CDN)

## Estrutura do projeto

```
viajemais/
├── manage.py
├── requirements.txt
├── viajemais/            # configurações do projeto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                 # app principal
│   ├── models.py         # Pacote, Compra, Orcamento
│   ├── admin.py          # configuração do Django Admin
│   ├── views.py          # páginas, carrinho e compra
│   ├── forms.py          # login, cadastro e orçamento
│   ├── niveis.py         # regras de nível e desconto
│   ├── urls.py
│   └── migrations/
├── templates/
│   ├── base.html         # cabeçalho, menu e rodapé
│   ├── core/             # index, pacotes, sobre, contato, perfil
│   └── registration/     # login e cadastro
├── static/
│   ├── css/style.css
│   └── imgs/             # logo do site
└── media/                # imagens enviadas pelo admin (criado automaticamente)
```

## Instalação

```bash
# 1. (opcional) criar e ativar um ambiente virtual
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. instalar dependências
pip install -r requirements.txt

# 3. criar as tabelas do banco
python manage.py makemigrations core
python manage.py migrate

# 4. criar o usuário administrador
python manage.py createsuperuser

# 5. iniciar o servidor
python manage.py runserver
```

| Endereço | Descrição |
|---|---|
| http://127.0.0.1:8000/ | Site |
| http://127.0.0.1:8000/admin/ | Painel administrativo |

## Configuração inicial

1. Copie o logo para `static/imgs/logo.png.jpeg`.
2. Acesse `/admin/` e, em **Pacotes**, cadastre os destinos (nome, descrição, preço por viajante e imagem).
3. Marque **"Exibir no carrossel da página inicial"** nos pacotes que devem aparecer na home e preencha a legenda.
4. Use o campo **Ordem de exibição** para controlar a posição dos pacotes na listagem.

## Painel administrativo

| Seção | O que faz |
|---|---|
| **Pacotes** | Cria e edita pacotes. Preço, disponibilidade, carrossel e ordem podem ser alterados direto na listagem. |
| **Compras** | Histórico de todas as compras, com filtro por destino e data e busca por cliente. |
| **Pedidos de orçamento** | Mensagens recebidas pelo formulário de contato. Marque como "respondido" na listagem. |
| **Usuários** | Clientes cadastrados e administradores. |

## Rotas

| URL | Nome | Acesso |
|---|---|---|
| `/` | `index` | Público |
| `/pacotes/` | `pacotes` | Público |
| `/sobre/` | `sobre` | Público |
| `/contato/` | `contato` | Público |
| `/login/` | `login` | Público |
| `/cadastro/` | `cadastro` | Público |
| `/logout/` | `logout` | Logado (POST) |
| `/perfil/` | `perfil` | Logado |
| `/carrinho/adicionar/<id>/` | `adicionar_carrinho` | Logado (POST) |
| `/carrinho/remover/<id>/` | `remover_carrinho` | Público (POST) |
| `/carrinho/finalizar/` | `finalizar_compra` | Logado (POST) |

## Models

- **Pacote:** destino, descrição, preço por viajante, imagem, ativo, exibir no carrossel, legenda e ordem.
- **Compra:** cliente, pacote, destino, quantidade de viajantes, valor original, desconto aplicado e valor final.
- **Orcamento:** nome, e-mail, destino desejado, data prevista, número de viajantes, mensagem e status de resposta.

## Níveis e descontos

O nível depende da quantidade de viagens já compradas pelo cliente. O desconto é aplicado a cada nova compra, conforme o nível no momento da finalização.

| Nível | Viagens compradas | Desconto |
|---|---|---|
| Bronze | 0 a 2 | 5% |
| Prata | 3 a 5 | 10% |
| Ouro | 6 a 9 | 15% |
| Diamante | 10 ou mais | 20% |

As regras ficam em `core/niveis.py`.

## Observações

- O carrinho fica na sessão do usuário; só vira **Compra** ao finalizar.
- Para adicionar ao carrinho é preciso estar logado.
- O nome de usuário do Django é o próprio e-mail do cliente.
- Cada compra guarda o nome do destino e os valores da época, então alterar um pacote no admin não muda o histórico.

## Antes de publicar em produção

- Trocar o `SECRET_KEY` em `settings.py` (de preferência lendo de variável de ambiente).
- Definir `DEBUG = False` e configurar `ALLOWED_HOSTS`.
- Servir `static/` e `media/` pelo servidor web (ou usar WhiteNoise / storage externo).
- Considerar PostgreSQL no lugar do SQLite.
