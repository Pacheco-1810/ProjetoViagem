
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase

from core.models import Compra, Hotel, Pacote
from core.services import SemVaga, criar_reserva
from core.niveis import calcular_desconto


Usuario = get_user_model()


class RegrasDeDescontoTest(TestCase):

    def test_desconto_bronze(self):
        self.assertEqual(calcular_desconto(0), 5)

    def test_desconto_prata(self):
        self.assertEqual(calcular_desconto(3), 10)

    def test_desconto_ouro(self):
        self.assertEqual(calcular_desconto(6), 15)

    def test_desconto_diamante(self):
        self.assertEqual(calcular_desconto(10), 20)


class ReservaServiceTest(TestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username="cliente",
            password="123456"
        )

        self.pacote = Pacote.objects.create(
            nome="Gramado",
            descricao="Viagem para Gramado",
            preco=Decimal("100.00"),
            ativo=True
        )

        self.hotel = Hotel.objects.create(
            pacote=self.pacote,
            nome="Hotel Central",
            estrelas=4,
            vagas=5,
            acrescimo=Decimal("20.00")
        )

    def test_criar_reserva_com_sucesso(self):
        reserva = criar_reserva(
            self.usuario,
            self.pacote,
            2,
            hotel=self.hotel
        )

        self.assertEqual(reserva.quantidade, 2)
        self.assertEqual(reserva.valor_original, Decimal("240.00"))
        self.assertEqual(reserva.desconto_percentual, 5)
        self.assertEqual(reserva.valor_final, Decimal("228.0000"))
        self.assertEqual(reserva.status, Compra.CONFIRMADA)

    def test_nao_permitir_reserva_sem_vagas(self):
        with self.assertRaises(SemVaga):
            criar_reserva(
                self.usuario,
                self.pacote,
                6,
                hotel=self.hotel
            )

    def test_hotel_deve_pertencer_ao_pacote(self):
        outro_pacote = Pacote.objects.create(
            nome="Canela",
            descricao="Viagem para Canela",
            preco=Decimal("150.00")
        )

        outro_hotel = Hotel.objects.create(
            pacote=outro_pacote,
            nome="Hotel Canela",
            vagas=5
        )

        with self.assertRaises(ValueError):
            criar_reserva(
                self.usuario,
                self.pacote,
                1,
                hotel=outro_hotel
            )

    def test_cancelar_reserva(self):
        reserva = criar_reserva(
            self.usuario,
            self.pacote,
            1,
            hotel=self.hotel
        )

        reserva.cancelar()
        reserva.refresh_from_db()

        self.assertEqual(reserva.status, Compra.CANCELADA)

    def test_nao_cancelar_duas_vezes(self):
        reserva = criar_reserva(
            self.usuario,
            self.pacote,
            1,
            hotel=self.hotel
        )

        reserva.cancelar()

        with self.assertRaises(ValueError):
            reserva.cancelar()


class PacoteAPITest(APITestCase):

    def setUp(self):
        self.pacote = Pacote.objects.create(
            nome="Florianópolis",
            descricao="Viagem para Florianópolis",
            preco=Decimal("500.00"),
            ativo=True
        )

    def test_consultar_pacotes_sem_login(self):
        resposta = self.client.get("/api/pacotes/")

        self.assertEqual(resposta.status_code, 200)

    def test_cliente_nao_pode_cadastrar_pacote(self):
        usuario = Usuario.objects.create_user(
            username="cliente_api",
            password="123456"
        )

        self.client.force_authenticate(user=usuario)

        resposta = self.client.post(
            "/api/pacotes/",
            {
                "nome": "Rio de Janeiro",
                "descricao": "Viagem para o Rio",
                "preco": "800.00",
                "ativo": True
            }
        )

        self.assertEqual(resposta.status_code, 403)

    def test_administrador_pode_cadastrar_pacote(self):
        administrador = Usuario.objects.create_superuser(
            username="admin_api",
            email="admin@viajemais.com",
            password="123456"
        )

        self.client.force_authenticate(user=administrador)

        resposta = self.client.post(
            "/api/pacotes/",
            {
                "nome": "Rio de Janeiro",
                "descricao": "Viagem para o Rio",
                "preco": "800.00",
                "ativo": True
            }
        )

        self.assertEqual(resposta.status_code, 201)


class ReservaAPITest(APITestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username="cliente_reserva",
            password="123456"
        )

        self.outro_usuario = Usuario.objects.create_user(
            username="outro_cliente",
            password="123456"
        )

        self.pacote = Pacote.objects.create(
            nome="Porto Seguro",
            descricao="Viagem para Porto Seguro",
            preco=Decimal("200.00"),
            ativo=True
        )

        self.hotel = Hotel.objects.create(
            pacote=self.pacote,
            nome="Hotel Praia",
            estrelas=4,
            vagas=10,
            acrescimo=Decimal("30.00")
        )

    def test_cliente_pode_criar_reserva(self):
        self.client.force_authenticate(user=self.usuario)

        resposta = self.client.post(
            "/api/reservas/",
            {
                "pacote": self.pacote.pk,
                "hotel": self.hotel.pk,
                "quantidade": 2
            }
        )

        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(Compra.objects.count(), 1)

    def test_cliente_precisa_estar_autenticado(self):
        resposta = self.client.post(
            "/api/reservas/",
            {
                "pacote": self.pacote.pk,
                "hotel": self.hotel.pk,
                "quantidade": 1
            }
        )

        self.assertEqual(resposta.status_code, 403)

    def test_cliente_nao_pode_ver_reserva_de_outro(self):
        reserva = criar_reserva(
            self.outro_usuario,
            self.pacote,
            1,
            hotel=self.hotel
        )

        self.client.force_authenticate(user=self.usuario)

        resposta = self.client.get(
            f"/api/reservas/{reserva.pk}/"
        )

        self.assertEqual(resposta.status_code, 404)

    def test_nao_permitir_quantidade_acima_do_limite(self):
        self.client.force_authenticate(user=self.usuario)

        resposta = self.client.post(
            "/api/reservas/",
            {
                "pacote": self.pacote.pk,
                "hotel": self.hotel.pk,
                "quantidade": 21
            }
        )

        self.assertEqual(resposta.status_code, 400)
