# ViajeMais

Sistema web de agência de turismo desenvolvido com **Python e Django**, que permite consultar pacotes turísticos, realizar reservas, gerenciar hotéis e controlar a disponibilidade de vagas. O sistema também possui uma API REST documentada com Swagger.

## Integrantes

- Mauricio Miotto Martini
- Gabriel Silveira Pacheco

## Funcionalidades

- **Página inicial:** destaque promocional e carrossel de destinos selecionados no painel administrativo.
- **Pacotes:** listagem de pacotes turísticos ativos.
- **Hotéis:** gerenciamento de hotéis vinculados aos pacotes, com controle de vagas e disponibilidade.
- **Cadastro e login:** autenticação de usuários utilizando o sistema do Django.
- **Carrinho:** adicionar, remover e finalizar compras.
- **Reservas:** criação de reservas com validação de disponibilidade dos hotéis.
- **Meu perfil:** dashboard com nível do cliente, desconto, total gasto, progresso e histórico de viagens.
- **Contato:** formulário de orçamento personalizado, com armazenamento no banco de dados.
- **Sobre:** página institucional.
- **Painel administrativo:** gerenciamento de pacotes, hotéis, compras, orçamentos e usuários.
- **API REST:** consulta de pacotes e gerenciamento de reservas.
- **Swagger:** documentação interativa dos endpoints da API.

## Tecnologias

- Python
- Django
- Django REST Framework
- drf-spectacular (Swagger/OpenAPI)
- SQLite
- Pillow (upload de imagens)
- Bootstrap 5.3
- HTML e CSS

## Estrutura do projeto

```text
ProjetoViagem/
├── manage.py
├── requirements.txt
├── viajemais/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── models.py
│   ├── admin.py
│   ├── views.py
│   ├── forms.py
│   ├── services.py
│   ├── niveis.py
│   ├── Serializers.py
│   ├── api_views.py
│   ├── api_urls.py
│   ├── tests.py
│   ├── urls.py
│   └── migrations/
├── templates/
├── static/
└── media/
```

## Instalação e execução

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
cd ProjetoViagem
```

### 2. Criar e ativar o ambiente virtual

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Criar e atualizar o banco de dados

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Criar o usuário administrador

```bash
python manage.py createsuperuser
```

### 6. Iniciar o servidor

```bash
python manage.py runserver
```

O sistema ficará disponível em:

http://127.0.0.1:8000/

## Endereços do sistema

| Endereço | Descrição |
|---|---|
| `/` | Página inicial |
| `/pacotes/` | Consulta de pacotes |
| `/sobre/` | Página institucional |
| `/contato/` | Formulário de orçamento |
| `/login/` | Login |
| `/cadastro/` | Cadastro |
| `/perfil/` | Perfil do cliente |
| `/admin/` | Painel administrativo |
| `/api/pacotes/` | API de pacotes |
| `/api/reservas/` | API de reservas |
| `/api/schema/` | Esquema OpenAPI |
| `/api/docs/` | Documentação Swagger |

## Configuração inicial e dados de demonstração

Após iniciar o sistema:

1. Acesse `/admin/` com o usuário administrador.
2. Cadastre pacotes turísticos, informando nome, descrição, preço e imagem.
3. Cadastre hotéis vinculados aos respectivos pacotes.
4. Configure a quantidade de vagas disponíveis em cada hotel.
5. Cadastre usuários clientes para demonstrar o processo de compra.
6. Realize reservas para demonstrar o controle de disponibilidade e o cálculo de descontos.

Para a apresentação, recomenda-se cadastrar pelo menos três pacotes, dois hotéis e dois usuários clientes.

## Painel administrativo

| Seção | Funcionalidade |
|---|---|
| Pacotes | Cadastro e edição de destinos turísticos. |
| Hotéis | Gerenciamento de hotéis, preços adicionais e vagas. |
| Compras | Consulta do histórico de reservas e valores. |
| Orçamentos | Consulta e acompanhamento dos pedidos recebidos. |
| Usuários | Gerenciamento de clientes e administradores. |

## API REST

A API foi desenvolvida utilizando Django REST Framework.

Principais recursos:

- Consulta de pacotes turísticos.
- Criação de reservas.
- Consulta de reservas do usuário autenticado.
- Cancelamento de reservas, conforme as permissões.
- Restrição de operações administrativas para usuários autorizados.

### Documentação Swagger

A documentação interativa está disponível em:

`http://127.0.0.1:8000/api/docs/`

O esquema OpenAPI está disponível em:

`http://127.0.0.1:8000/api/schema/`

## Modelos do sistema

- **Pacote:** nome, descrição, preço, imagem, status de ativação e informações de exibição.
- **Hotel:** nome, pacote relacionado, classificação, quantidade de vagas e acréscimo de preço.
- **Compra:** usuário, pacote, hotel, quantidade de viajantes, valores, desconto, status e data.
- **Orcamento:** nome, e-mail, destino desejado, data prevista, quantidade de viajantes, mensagem e status de resposta.

## Níveis e descontos

O nível do cliente é calculado conforme a quantidade de viagens confirmadas.

| Nível | Viagens confirmadas | Desconto |
|---|---:|---:|
| Bronze | 0 a 2 | 5% |
| Prata | 3 a 5 | 10% |
| Ouro | 6 a 9 | 15% |
| Diamante | 10 ou mais | 20% |

As regras de cálculo estão implementadas em `core/niveis.py`.

## Regras de negócio

- O cliente precisa estar autenticado para realizar uma reserva.
- A quantidade de viajantes deve respeitar o limite estabelecido pelo sistema.
- A reserva depende da disponibilidade de vagas no hotel.
- O sistema calcula automaticamente o valor original e o desconto aplicado.
- Reservas canceladas não devem consumir vagas disponíveis.
- Clientes podem consultar somente suas próprias reservas.
- Administradores possuem permissões adicionais de gerenciamento.

## Testes automatizados

O projeto possui testes automatizados utilizando o framework de testes do Django e o Django REST Framework.

Para executar os testes:

```bash
python manage.py test core
```

**Resultado obtido durante o desenvolvimento:** 16 testes executados com sucesso.

Os testes abrangem regras de desconto, criação de reservas, disponibilidade, cancelamento, autenticação e permissões da API.

## Limitações e melhorias futuras

- Implementação de integração com meios de pagamento.
- Envio de e-mails reais para confirmação de reservas.
- Melhorias na geração de relatórios administrativos.
- Possibilidade de utilização de PostgreSQL em ambiente de produção.
- Implantação em servidor de produção.

## Segurança e produção

Antes de publicar o sistema:

- Armazenar a `SECRET_KEY` em variável de ambiente.
- Desativar `DEBUG`.
- Configurar `ALLOWED_HOSTS`.
- Não publicar senhas ou credenciais no repositório.
- Configurar corretamente arquivos estáticos e mídias.
- Avaliar a utilização de PostgreSQL em produção.