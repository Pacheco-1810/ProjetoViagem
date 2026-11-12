import shutil
import tempfile
from decimal import Decimal
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image
from rest_framework.test import APITestCase

from core.forms import HotelForm
from core.models import Compra, Hotel, Pacote
from core.services import SemVaga, calcular_desconto, criar_reserva

User = get_user_model()
PASTA_MEDIA = tempfile.mkdtemp()


def criar_pacote(nome="Gramado", preco="100.00", vagas=5, acrescimo="20.00"):
    pacote = Pacote.objects.create(nome=nome, descricao="Viagem de teste", preco=Decimal(preco))
    hotel = Hotel.objects.create(pacote=pacote, nome=f"Hotel {nome}", vagas=vagas, acrescimo=Decimal(acrescimo))
    return pacote, hotel


def imagem_de_teste():
    arquivo = BytesIO()
    Image.new("RGB", (10, 10)).save(arquivo, "PNG")
    return SimpleUploadedFile("foto.png", arquivo.getvalue(), content_type="image/png")


class DescontoTest(TestCase):
    def test_desconto_por_nivel(self):
        self.assertEqual(calcular_desconto(0), 5)
        self.assertEqual(calcular_desconto(3), 10)
        self.assertEqual(calcular_desconto(6), 15)
        self.assertEqual(calcular_desconto(10), 20)


class ReservaServiceTest(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username="cliente", password="12345678")
        self.pacote, self.hotel = criar_pacote()

    def test_reserva_valida_calcula_valores(self):
        reserva = criar_reserva(self.usuario, self.pacote, 2, self.hotel)

        self.assertEqual(reserva.valor_original, Decimal("240.00"))
        self.assertEqual(reserva.desconto_percentual, 5)
        self.assertEqual(reserva.valor_final, Decimal("228.00"))
        self.assertEqual(reserva.status, Compra.CONFIRMADA)

    def test_reserva_sem_vagas_e_recusada(self):
        with self.assertRaises(SemVaga):
            criar_reserva(self.usuario, self.pacote, 6, self.hotel)
        self.assertEqual(Compra.objects.count(), 0)

    def test_hotel_de_outro_pacote_e_recusado(self):
        _, outro_hotel = criar_pacote("Canela")
        with self.assertRaises(ValueError):
            criar_reserva(self.usuario, self.pacote, 1, outro_hotel)

    def test_cancelar_libera_as_vagas(self):
        reserva = criar_reserva(self.usuario, self.pacote, 5, self.hotel)
        self.assertEqual(self.hotel.disponiveis(), 0)

        reserva.cancelar()
        self.assertEqual(self.hotel.disponiveis(), 5)

    def test_nao_cancela_duas_vezes(self):
        reserva = criar_reserva(self.usuario, self.pacote, 1, self.hotel)
        reserva.cancelar()
        with self.assertRaises(ValueError):
            reserva.cancelar()


class FluxoDoClienteTest(TestCase):
    """Cliente consulta o pacote, coloca no carrinho e reserva."""

    def setUp(self):
        self.cliente = User.objects.create_user(username="c@c.com", email="c@c.com", password="12345678")
        self.outro = User.objects.create_user(username="o@o.com", email="o@o.com", password="12345678")
        self.pacote, self.hotel = criar_pacote(vagas=4)

    def adicionar(self, quantidade):
        return self.client.post(
            reverse("adicionar_carrinho", args=[self.pacote.pk]),
            {"quantidade": quantidade, "hotel": self.hotel.pk},
            follow=True,
        )

    def test_fluxo_completo_de_reserva(self):
        self.client.force_login(self.cliente)
        self.assertContains(self.client.get(reverse("pacotes")), "Gramado")

        self.adicionar(3)
        resposta = self.client.post(reverse("finalizar_compra"), follow=True)

        self.assertContains(resposta, "Reserva confirmada")
        self.assertEqual(Compra.objects.filter(usuario=self.cliente).count(), 1)
        self.assertEqual(self.hotel.disponiveis(), 1)

    def test_quantidade_maior_que_as_vagas_e_recusada(self):
        self.client.force_login(self.cliente)
        resposta = self.adicionar(5)

        self.assertContains(resposta, "possui apenas 4 vaga(s)")
        self.assertNotIn("carrinho", self.client.session)

    def test_vaga_ocupada_depois_de_ir_ao_carrinho(self):
        self.client.force_login(self.cliente)
        self.adicionar(3)
        criar_reserva(self.outro, self.pacote, 3, self.hotel)  # outra pessoa reserva antes

        resposta = self.client.post(reverse("finalizar_compra"), follow=True)

        self.assertContains(resposta, "Não foi possível finalizar")
        self.assertEqual(Compra.objects.filter(usuario=self.cliente).count(), 0)

    def test_visitante_precisa_fazer_login(self):
        resposta = self.client.post(reverse("adicionar_carrinho", args=[self.pacote.pk]), {"quantidade": 1})
        self.assertRedirects(resposta, f"{reverse('login')}?next=/carrinho/adicionar/{self.pacote.pk}/")
        self.assertRedirects(self.client.get(reverse("perfil")), f"{reverse('login')}?next=/perfil/")

    def test_cliente_nao_cancela_reserva_de_outro(self):
        reserva = criar_reserva(self.outro, self.pacote, 1, self.hotel)
        self.client.force_login(self.cliente)

        resposta = self.client.post(reverse("cancelar_reserva", args=[reserva.pk]))

        self.assertEqual(resposta.status_code, 404)
        reserva.refresh_from_db()
        self.assertEqual(reserva.status, Compra.CONFIRMADA)

    def test_cliente_cancela_a_propria_reserva(self):
        reserva = criar_reserva(self.cliente, self.pacote, 1, self.hotel)
        self.client.force_login(self.cliente)

        self.client.post(reverse("cancelar_reserva", args=[reserva.pk]))

        reserva.refresh_from_db()
        self.assertEqual(reserva.status, Compra.CANCELADA)

    def test_filtro_por_destino(self):
        criar_pacote("Paris", preco="8000.00")
        resposta = self.client.get(reverse("pacotes"), {"q": "paris"})

        self.assertContains(resposta, "Paris")
        self.assertNotContains(resposta, "Gramado")

    def test_filtro_somente_com_vagas(self):
        criar_reserva(self.outro, self.pacote, 4, self.hotel)  # esgota o pacote
        resposta = self.client.get(reverse("pacotes"), {"so_disponiveis": "on"})

        self.assertNotContains(resposta, "Gramado")


@override_settings(MEDIA_ROOT=PASTA_MEDIA)
class GestaoTest(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(PASTA_MEDIA, ignore_errors=True)

    def setUp(self):
        self.admin = User.objects.create_user(username="a@a.com", password="12345678", is_staff=True)
        self.cliente = User.objects.create_user(username="c@c.com", password="12345678")
        self.dados = {"nome": "Bahia", "descricao": "Praias", "preco": "900.00", "ordem": 0, "imagem": None}

    def test_cliente_recebe_403_na_gestao(self):
        self.client.force_login(self.cliente)
        for nome in ["gestao_pacotes", "gestao_pacote_novo", "gestao_reservas"]:
            self.assertEqual(self.client.get(reverse(nome)).status_code, 403)

    def test_visitante_e_enviado_para_o_login(self):
        resposta = self.client.get(reverse("gestao_pacotes"))
        self.assertEqual(resposta.status_code, 302)
        self.assertIn(reverse("login"), resposta.url)

    def test_administrador_cria_pacote_e_hotel(self):
        self.client.force_login(self.admin)
        self.dados["imagem"] = imagem_de_teste()

        resposta = self.client.post(reverse("gestao_pacote_novo"), self.dados)
        pacote = Pacote.objects.get(nome="Bahia")
        self.assertRedirects(resposta, reverse("gestao_pacote_editar", args=[pacote.pk]))

        self.client.post(
            reverse("gestao_hotel_novo", args=[pacote.pk]),
            {"nome": "Hotel Mar", "estrelas": 4, "vagas": 8, "acrescimo": "50.00"},
        )
        self.assertEqual(pacote.hoteis.count(), 1)

    def test_preco_invalido_nao_salva(self):
        self.client.force_login(self.admin)
        self.dados.update(preco="0", imagem=imagem_de_teste())

        resposta = self.client.post(reverse("gestao_pacote_novo"), self.dados)

        self.assertContains(resposta, "O preço deve ser maior que zero.")
        self.assertEqual(Pacote.objects.count(), 0)

    def test_nome_de_pacote_repetido_nao_salva(self):
        criar_pacote("Bahia")
        self.client.force_login(self.admin)
        self.dados["imagem"] = imagem_de_teste()

        resposta = self.client.post(reverse("gestao_pacote_novo"), self.dados)

        self.assertContains(resposta, "Já existe um pacote com este destino.")

    def test_nao_exclui_pacote_com_reserva_confirmada(self):
        pacote, hotel = criar_pacote()
        criar_reserva(self.cliente, pacote, 1, hotel)
        self.client.force_login(self.admin)

        self.client.post(reverse("gestao_pacote_excluir", args=[pacote.pk]))

        self.assertTrue(Pacote.objects.filter(pk=pacote.pk).exists())

    def test_administrador_exclui_pacote_sem_reservas(self):
        pacote, _ = criar_pacote()
        self.client.force_login(self.admin)

        self.client.post(reverse("gestao_pacote_excluir", args=[pacote.pk]))

        self.assertFalse(Pacote.objects.filter(pk=pacote.pk).exists())

    def test_vagas_nao_podem_ficar_abaixo_das_reservas(self):
        pacote, hotel = criar_pacote(vagas=5)
        criar_reserva(self.cliente, pacote, 4, hotel)

        form = HotelForm({"nome": hotel.nome, "estrelas": 3, "vagas": 2, "acrescimo": "0"}, instance=hotel)

        self.assertFalse(form.is_valid())
        self.assertIn("vagas", form.errors)

    def test_paginas_de_gestao_abrem_para_o_administrador(self):
        pacote, hotel = criar_pacote()
        self.client.force_login(self.admin)
        urls = [
            reverse("gestao_pacotes"),
            reverse("gestao_pacote_editar", args=[pacote.pk]),
            reverse("gestao_pacote_excluir", args=[pacote.pk]),
            reverse("gestao_hotel_novo", args=[pacote.pk]),
            reverse("gestao_hotel_editar", args=[hotel.pk]),
            reverse("gestao_hotel_excluir", args=[hotel.pk]),
            reverse("gestao_reservas"),
        ]
        for url in urls:
            self.assertEqual(self.client.get(url).status_code, 200, url)


class LoginECadastroTest(TestCase):
    def test_cadastro_valido_cria_usuario_e_faz_login(self):
        resposta = self.client.post(
            reverse("cadastro"), {"nome": "Maria", "email": "Maria@Email.com", "senha": "senha-forte-123"}
        )

        self.assertRedirects(resposta, reverse("pacotes"))
        self.assertTrue(User.objects.filter(username="maria@email.com").exists())

    def test_cadastro_com_senha_curta_e_recusado(self):
        resposta = self.client.post(reverse("cadastro"), {"nome": "Maria", "email": "m@m.com", "senha": "123"})

        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(User.objects.filter(username="m@m.com").exists())

    def test_login_aceita_usuario_criado_pelo_createsuperuser(self):
        User.objects.create_superuser("admin", "admin@x.com", "12345678")
        resposta = self.client.post(reverse("login"), {"username": "admin", "password": "12345678"})

        self.assertEqual(resposta.status_code, 302)


class AdminTest(TestCase):
    def test_paginas_do_admin_abrem(self):
        User.objects.create_superuser("a", "a@a.com", "12345678")
        self.client.login(username="a", password="12345678")
        pacote, hotel = criar_pacote()

        for modelo in ["pacote", "hotel", "compra", "orcamento"]:
            self.assertEqual(self.client.get(f"/admin/core/{modelo}/").status_code, 200, modelo)
        self.assertEqual(self.client.get(f"/admin/core/pacote/{pacote.pk}/change/").status_code, 200)

    def test_cliente_nao_acessa_o_admin(self):
        User.objects.create_user("c", "c@c.com", "12345678")
        self.client.login(username="c", password="12345678")

        self.assertEqual(self.client.get("/admin/core/pacote/").status_code, 302)


class PacoteAPITest(APITestCase):
    def setUp(self):
        criar_pacote("Florianópolis")
        self.novo = {"nome": "Rio de Janeiro", "descricao": "Viagem para o Rio", "preco": "800.00"}

    def test_consulta_sem_login(self):
        resposta = self.client.get("/api/pacotes/")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.json()), 1)

    def test_cliente_nao_cadastra_pacote(self):
        self.client.force_authenticate(User.objects.create_user(username="c", password="12345678"))
        self.assertEqual(self.client.post("/api/pacotes/", self.novo).status_code, 403)

    def test_administrador_cadastra_pacote(self):
        self.client.force_authenticate(User.objects.create_superuser("a", "a@a.com", "12345678"))
        self.assertEqual(self.client.post("/api/pacotes/", self.novo).status_code, 201)

    def test_preco_invalido_e_recusado(self):
        self.client.force_authenticate(User.objects.create_superuser("a", "a@a.com", "12345678"))
        self.novo["preco"] = "-5"
        resposta = self.client.post("/api/pacotes/", self.novo)

        self.assertEqual(resposta.status_code, 400)
        self.assertIn("preco", resposta.json())

    def test_pacote_sem_imagem_nao_quebra_a_listagem(self):
        self.client.force_authenticate(User.objects.create_superuser("a", "a@a.com", "12345678"))
        self.client.post("/api/pacotes/", self.novo)

        self.assertEqual(self.client.get(reverse("pacotes")).status_code, 200)

    def test_swagger_abre(self):
        self.assertEqual(self.client.get("/api/docs/").status_code, 200)
        self.assertEqual(self.client.get("/api/schema/").status_code, 200)


class ReservaAPITest(APITestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username="cliente", password="12345678")
        self.outro = User.objects.create_user(username="outro", password="12345678")
        self.pacote, self.hotel = criar_pacote("Porto Seguro", vagas=10)

    def reservar(self, quantidade):
        return self.client.post(
            "/api/reservas/", {"pacote": self.pacote.pk, "hotel": self.hotel.pk, "quantidade": quantidade}
        )

    def test_cliente_cria_reserva(self):
        self.client.force_authenticate(self.usuario)
        self.assertEqual(self.reservar(2).status_code, 201)
        self.assertEqual(Compra.objects.get().usuario, self.usuario)

    def test_visitante_nao_cria_reserva(self):
        self.assertEqual(self.reservar(1).status_code, 403)

    def test_quantidade_acima_do_limite_e_recusada(self):
        self.client.force_authenticate(self.usuario)
        self.assertEqual(self.reservar(21).status_code, 400)

    def test_reserva_sem_vagas_e_recusada(self):
        self.client.force_authenticate(self.usuario)
        resposta = self.reservar(11)

        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(Compra.objects.count(), 0)

    def test_cliente_nao_ve_reserva_de_outro(self):
        reserva = criar_reserva(self.outro, self.pacote, 1, self.hotel)
        self.client.force_authenticate(self.usuario)

        self.assertEqual(self.client.get(f"/api/reservas/{reserva.pk}/").status_code, 404)
        self.assertEqual(self.client.get("/api/reservas/").json(), [])

    def test_cancelar_reserva_pela_api(self):
        reserva = criar_reserva(self.usuario, self.pacote, 1, self.hotel)
        self.client.force_authenticate(self.usuario)

        resposta = self.client.post(f"/api/reservas/{reserva.pk}/cancelar/")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["status"], Compra.CANCELADA)
