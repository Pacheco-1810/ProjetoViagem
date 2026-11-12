# ViajeMais

Sistema web de uma agência de viagens feito com **Python e Django**. O administrador cadastra pacotes e hotéis (com limite de vagas) e o cliente consulta os pacotes e faz a reserva, respeitando as vagas disponíveis. O sistema também tem uma API REST documentada no Swagger.

Trabalho Final de Programação Web II.

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

## Estrutura

```text
ProjetoViagem/
├── manage.py
├── popular_dados.py      # cria usuários e pacotes de demonstração
├── requirements.txt
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

| Endereço | Descrição |
|---|---|
| `/` | Página inicial |
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

## Regras de negócio

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
