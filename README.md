# ViajeMais

<<<<<<< HEAD
Sistema web de uma agência de viagens feito com **Python e Django**. O administrador cadastra pacotes e hotéis (com limite de vagas) e o cliente consulta os pacotes e faz a reserva, respeitando as vagas disponíveis. O sistema também tem uma API REST documentada no Swagger.
=======
Sistema web de agência de turismo desenvolvido com **Python e Django**, que permite consultar pacotes turísticos, realizar reservas, gerenciar hotéis e controlar a disponibilidade de vagas. O sistema também possui uma API REST documentada com Swagger.

## Integrantes

- Mauricio Miotto Martini
- Gabriel Silveira Pacheco
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7

Trabalho Final de Programação Web II.

<<<<<<< HEAD
## Integrantes

- Mauricio Miotto Martini
- Gabriel Silveira Pacheco

## Perfis de usuário

| Perfil | Como é criado | O que pode fazer |
|---|---|---|
| Visitante | não precisa de conta | ver a página inicial, consultar e filtrar pacotes, enviar pedido de orçamento, ver o Swagger |
| Cliente | pela página `/cadastro/` | tudo do visitante, mais: carrinho, reservar, ver o perfil e o histórico, cancelar **as próprias** reservas, usar a API de reservas |
| Administrador | `createsuperuser` ou `popular_dados.py` | tudo do cliente, mais: área de **Gestão** (pacotes, hotéis e reservas), Django Admin e escrita na API de pacotes |

As permissões são verificadas no servidor (decorators nas views e permissions na API), não só escondendo botões.

## Tecnologias

Python, Django, Django REST Framework, drf-spectacular (Swagger/OpenAPI), django-jazzmin (tema do Django Admin), SQLite, Pillow (upload de imagens) e Bootstrap 5.
=======
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
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7

## Estrutura

```text
ProjetoViagem/
├── manage.py
├── popular_dados.py      # cria usuários e pacotes de demonstração
├── requirements.txt
<<<<<<< HEAD
├── viajemais/            # configurações do projeto (settings, urls, wsgi)
├── core/                 # aplicação: models, views, forms, services, api, admin, tests
│   └── migrations/
├── templates/            # páginas HTML
└── static/               # css e imagens
```

- `models.py`: Pacote, Hotel, Compra (reserva) e Orcamento.
- `services.py`: regras de negócio (reserva com controle de vagas, níveis e descontos).
- `views.py`: páginas do site e da área de gestão.
- `api.py`: serializers e viewsets da API.

## Instalação e execução

Requer Python 3.10 ou superior.

```bash
git clone https://github.com/Pacheco-1810/ProjetoViagem.git
cd ProjetoViagem

python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

pip install -r requirements.txt
python manage.py migrate
python popular_dados.py        # dados de demonstração (opcional)
python manage.py runserver
```

O sistema abre em http://127.0.0.1:8000/

As migrations já estão no repositório, então só é preciso rodar `migrate`.

## Dados de demonstração

O comando `python popular_dados.py` cria 3 usuários e 4 pacotes (Gramado, Rio de Janeiro, Paris e Londres), cada um com hotéis e vagas. Pode ser executado mais de uma vez sem duplicar nada.

| Perfil | E-mail | Senha |
|---|---|---|
| Administrador | admin@viajemais.com | admin12345 |
| Cliente | cliente1@viajemais.com | cliente12345 |
| Cliente | cliente2@viajemais.com | cliente12345 |

São senhas apenas de demonstração. Para criar o seu próprio administrador use `python manage.py createsuperuser`; o login do site aceita tanto e-mail quanto nome de usuário.

## Roteiro de demonstração

1. Entrar como **administrador** em `/login/` e abrir **Gestão**.
2. Criar um pacote novo, depois cadastrar um hotel com poucas vagas (ex.: 3).
3. Tentar salvar um pacote com preço `0` ou com nome repetido: o formulário mostra o erro (**validação**).
4. Sair e entrar como **cliente**. Em `/pacotes/`, filtrar por destino e adicionar o pacote ao carrinho.
5. Tentar adicionar mais viajantes do que as vagas do hotel: o sistema recusa. Depois adicionar uma quantidade válida e **finalizar a compra**.
6. Abrir **Meu Perfil**: reserva, nível, desconto e total gasto. Cancelar a reserva libera as vagas.
7. Ainda como cliente, abrir `/gestao/`: erro 403 (**restrição de acesso**).
8. Abrir `/api/docs/` (Swagger): consultar `GET /api/pacotes/`. Para `POST /api/reservas/`, clicar em **Authorize** e informar e-mail e senha do cliente (Basic auth), ou estar logado no site na mesma janela.

## Endereços
=======
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
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7

| Endereço | Descrição |
|---|---|
| `/` | Página inicial |
<<<<<<< HEAD
| `/pacotes/` | Pacotes, filtros e carrinho |
| `/perfil/` | Perfil, histórico e cancelamento de reservas (cliente) |
| `/contato/` | Pedido de orçamento |
| `/sobre/` | Página institucional |
| `/login/`, `/cadastro/` | Autenticação |
| `/gestao/` | Gestão de pacotes e hotéis (administrador) |
| `/gestao/reservas/` | Consulta de todas as reservas (administrador) |
| `/admin/` | Django Admin |
| `/api/docs/` | Swagger |
| `/api/schema/` | Esquema OpenAPI |

## API REST

| Método e rota | Quem pode | O que faz |
|---|---|---|
| `GET /api/pacotes/` e `/api/pacotes/{id}/` | todos | lista e consulta pacotes ativos (aceita `?search=`) |
| `POST /api/pacotes/` | administrador | cadastra pacote |
| `PUT/PATCH/DELETE /api/pacotes/{id}/` | administrador | edita ou exclui (não exclui se houver reservas confirmadas) |
| `GET /api/reservas/` | autenticado | lista as próprias reservas (administrador vê todas) |
| `POST /api/reservas/` | autenticado | cria reserva, validando vagas e limite de viajantes |
| `POST /api/reservas/{id}/cancelar/` | dono da reserva ou administrador | cancela a reserva |
=======
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
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7

## Regras de negócio

<<<<<<< HEAD
- A reserva só é criada se o hotel tiver vagas livres. A verificação é feita dentro de uma transação, com os hotéis travados, para duas pessoas não ficarem com a mesma vaga.
- Reservas canceladas não ocupam vagas.
- Limite de 20 viajantes por reserva.
- Valor da reserva = (preço do pacote + acréscimo do hotel) x viajantes, menos o desconto do nível do cliente.
- Níveis por viagens confirmadas: Bronze (0 a 2) 5%, Prata (3 a 5) 10%, Ouro (6 a 9) 15%, Diamante (10 ou mais) 20%.
- O desconto é calculado uma vez por compra, antes de criar as reservas do carrinho.
- Não é possível reduzir as vagas de um hotel abaixo do número de vagas já reservadas.
- Pacote com reserva confirmada e hotel com vagas reservadas não podem ser excluídos.
- Cliente só consulta e cancela as próprias reservas.

## Testes

```bash
python manage.py test core
```

São 40 testes, cobrindo operações válidas, dados inválidos e acesso sem permissão: reserva e cálculo de valores, falta de vagas, fluxo completo do carrinho, cancelamento, filtros, área de gestão (403 para cliente, redirecionamento para visitante), cadastro, login e API.

## Funcionalidades

**Concluídas**

- Cadastro, login e logout.
- CRUD de pacotes e de hotéis (páginas próprias da área de Gestão).
- Reserva com controle de vagas por hotel, carrinho, perfil com nível e desconto e cancelamento de reserva.
- Busca e filtros: pacotes (destino, preço máximo e somente com vagas), gestão de pacotes e gestão de reservas (e-mail, destino e status).
- Pedido de orçamento (formulário salvo no banco).
- API REST de pacotes e reservas, com permissões e Swagger.
- Django Admin com tema Jazzmin (menu, ícones e links para o site, a Gestão e o Swagger) para apoio à administração.

**Parciais e limitações conhecidas**

- A reserva não é editada, só cancelada (cancelamento no lugar de exclusão, para manter o histórico).
- O administrador consulta todas as reservas na Gestão, mas cancelar a reserva de outro cliente só é possível pelo Django Admin ou pela API.
- Não há pagamento nem envio de e-mail. O pedido de orçamento só é registrado, e o administrador o marca como respondido pelo Django Admin.
- O carrinho fica na sessão do navegador.
- Os pacotes não têm data de viagem.
- Banco SQLite, indicado só para desenvolvimento.

## Contribuições

Histórico completo: `git log --format='%an %s'` ou a aba *Commits* do GitHub.

| Integrante | Atividades |
|---|---|
| Mauricio Miotto Martini | (preencher) |
| Gabriel Silveira Pacheco | (preencher) |

## Uso de bibliotecas e ferramentas de IA

Bibliotecas: Django, Django REST Framework, drf-spectacular, django-jazzmin, Pillow e Bootstrap.

Ferramentas de IA: o Claude (Anthropic) foi usado como apoio na revisão e correção do código, na organização da estrutura do projeto, na criação dos testes automatizados, na configuração do painel administrativo e na redação deste README.

## Segurança

Não há credenciais reais no repositório. A `SECRET_KEY` do `settings.py` é apenas de desenvolvimento e pode ser trocada pela variável de ambiente `SECRET_KEY`. Em produção, desative o `DEBUG` e configure o `ALLOWED_HOSTS`.
=======
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
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7
