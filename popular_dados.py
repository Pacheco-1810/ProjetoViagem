"""Cria usuários e pacotes de demonstração.

Uso (depois de rodar o migrate):  python popular_dados.py
Pode ser executado mais de uma vez, não duplica os dados.
"""
import os
from decimal import Decimal
from pathlib import Path

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "viajemais.settings")
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from django.core.files import File  # noqa: E402

from core.models import Hotel, Pacote  # noqa: E402

User = get_user_model()
IMAGENS = Path(__file__).resolve().parent / "static" / "imgs"

# e-mail, senha, nome, administrador?
USUARIOS = [
    ("admin@viajemais.com", "admin12345", "Administrador", True),
    ("cliente1@viajemais.com", "cliente12345", "Cliente Um", False),
    ("cliente2@viajemais.com", "cliente12345", "Cliente Dois", False),
]

# nome, descrição, preço, imagem, hotéis (nome, estrelas, vagas, acréscimo)
PACOTES = [
    ("Gramado", "Serra gaúcha com chocolate quente e muito frio.", "1500.00", "gramado.jpg",
     [("Hotel Serra Azul", 4, 10, "200.00"), ("Pousada Colina", 3, 4, "0.00")]),
    ("Rio de Janeiro", "Praias, Pão de Açúcar e Cristo Redentor.", "2200.00", "rjinicial.jpg",
     [("Copacabana Palace Inn", 5, 6, "450.00"), ("Hotel Lapa", 3, 12, "0.00")]),
    ("Paris", "A cidade luz com direito a Torre Eiffel.", "8500.00", "paris.jpg",
     [("Hotel Louvre", 4, 3, "600.00")]),
    ("Londres", "História, museus e chá das cinco.", "9000.00", "Londres.jpeg",
     [("Thames Hotel", 4, 5, "500.00")]),
]

for email, senha, nome, admin in USUARIOS:
    usuario, criado = User.objects.get_or_create(
        username=email, defaults={"email": email, "first_name": nome, "is_staff": admin, "is_superuser": admin}
    )
    if criado:
        usuario.set_password(senha)
        usuario.save()
        print(f"Usuário criado: {email}")

for ordem, (nome, descricao, preco, arquivo, hoteis) in enumerate(PACOTES):
    pacote, criado = Pacote.objects.get_or_create(
        nome=nome,
        defaults={
            "descricao": descricao,
            "preco": Decimal(preco),
            "no_carrossel": True,
            "legenda_carrossel": descricao,
            "ordem": ordem,
        },
    )
    if criado:
        with open(IMAGENS / arquivo, "rb") as imagem:
            pacote.imagem.save(arquivo, File(imagem))
        for hotel_nome, estrelas, vagas, acrescimo in hoteis:
            Hotel.objects.create(
                pacote=pacote, nome=hotel_nome, estrelas=estrelas, vagas=vagas, acrescimo=Decimal(acrescimo)
            )
        print(f"Pacote criado: {nome}")

print("Pronto.")
