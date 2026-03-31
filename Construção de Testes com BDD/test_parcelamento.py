"""
test_parcelamento.py
Feature: Oferta de parcelamento no checkout
Baseado nos 6 cenários BDD escritos para o MiniCommerce.
"""

import pytest
from test_checkout_system import Cart, InstallmentService


@pytest.fixture
def service():
    return InstallmentService()


def make_cart(total: float) -> Cart:
    """Cria um carrinho com exatamente o valor informado."""
    return Cart([{"name": "Produto", "price": total}])


# ─────────────────────────────────────────────
# Cenário 1 — Valor exatamente igual ao mínimo (R$ 100,00)
# ─────────────────────────────────────────────

class TestParcelamentoValorMinimo:
    """
    Scenario: Oferecer parcelamento para pedido com valor igual a R$ 100,00
      Given que o usuário possui itens no carrinho totalizando R$ 100,00
      When acessa a etapa de pagamento
      Then o sistema deve oferecer opções de parcelamento
      And deve exibir as condições de parcelas disponíveis
    """

    def test_oferece_parcelamento_no_valor_minimo(self, service):
        cart = make_cart(100.00)
        opcoes = service.get_options(cart)

        assert opcoes is not None
        assert len(opcoes) > 0
        assert all("installments" in o and "value" in o for o in opcoes)


# ─────────────────────────────────────────────
# Cenário 2 — Valor acima do mínimo (R$ 250,00)
# ─────────────────────────────────────────────

class TestParcelamentoAcimaDoMinimo:
    """
    Scenario: Oferecer parcelamento para pedido com valor maior que R$ 100,00
      Given que o usuário possui itens no carrinho totalizando R$ 250,00
      When acessa a etapa de pagamento
      Then o sistema deve oferecer opções de parcelamento
      And deve exibir as condições de parcelas disponíveis
    """

    def test_oferece_parcelamento_para_valor_alto(self, service):
        cart = make_cart(250.00)
        opcoes = service.get_options(cart)

        assert opcoes is not None
        assert len(opcoes) >= 1


# ─────────────────────────────────────────────
# Cenário 3 — Valor abaixo do mínimo (R$ 99,99)
# ─────────────────────────────────────────────

class TestSemParcelamentoAbaixoDoMinimo:
    """
    Scenario: Não oferecer parcelamento para pedido com valor menor que R$ 100,00
      Given que o usuário possui itens no carrinho totalizando R$ 99,99
      When acessa a etapa de pagamento
      Then o sistema não deve oferecer parcelamento
      And deve permitir apenas pagamento à vista
    """

    def test_nao_oferece_parcelamento_abaixo_do_minimo(self, service):
        cart = make_cart(99.99)
        opcoes = service.get_options(cart)

        assert opcoes is None  # None = apenas à vista disponível


# ─────────────────────────────────────────────
# Cenário 4 — Valor zero
# ─────────────────────────────────────────────

class TestSemParcelamentoValorZero:
    """
    Scenario: Não oferecer parcelamento para pedido com valor zero
      Given que o usuário possui itens no carrinho totalizando R$ 0,00
      When acessa a etapa de pagamento
      Then o sistema não deve oferecer parcelamento
      And deve exibir apenas opções de pagamento à vista
    """

    def test_nao_oferece_parcelamento_para_valor_zero(self, service):
        cart = make_cart(0.00)
        opcoes = service.get_options(cart)

        assert opcoes is None


# ─────────────────────────────────────────────
# Cenário 5 — Remoção do parcelamento ao baixar valor
# ─────────────────────────────────────────────

class TestRemoveParcelamentoAoReduzirCarrinho:
    """
    Scenario: Atualizar opções de parcelamento ao alterar valor do carrinho
      Given que o usuário possui itens no carrinho totalizando R$ 120,00
      And o sistema está exibindo opções de parcelamento
      When o usuário remove itens e o valor total passa a ser R$ 80,00
      Then o sistema deve remover as opções de parcelamento
      And deve exibir apenas pagamento à vista
    """

    def test_remove_parcelamento_ao_reduzir_valor(self, service):
        # Given — carrinho inicial elegível
        cart_inicial = make_cart(120.00)
        assert service.get_options(cart_inicial) is not None

        # When — carrinho atualizado (valor menor)
        cart_atualizado = make_cart(80.00)
        opcoes = service.get_options(cart_atualizado)

        # Then
        assert opcoes is None


# ─────────────────────────────────────────────
# Cenário 6 — Parcelamento surge ao atingir valor mínimo
# ─────────────────────────────────────────────

class TestExibeParcelamentoAoAtingirMinimo:
    """
    Scenario: Exibir parcelamento após atingir valor mínimo
      Given que o usuário possui itens no carrinho totalizando R$ 90,00
      And não há opção de parcelamento disponível
      When o usuário adiciona itens e o valor total passa a ser R$ 150,00
      Then o sistema deve passar a oferecer opções de parcelamento
      And deve exibir as condições de parcelas disponíveis
    """

    def test_exibe_parcelamento_apos_atingir_minimo(self, service):
        # Given — carrinho ainda não elegível
        cart_antes = make_cart(90.00)
        assert service.get_options(cart_antes) is None

        # When — carrinho atualizado
        cart_depois = make_cart(150.00)
        opcoes = service.get_options(cart_depois)

        # Then
        assert opcoes is not None
        assert len(opcoes) > 0
