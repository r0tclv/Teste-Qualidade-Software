"""
test_pedido.py
Feature: Criação de pedido condicionada à aprovação do pagamento
Baseado nos 6 cenários BDD escritos para o MiniCommerce.
"""

import pytest
from test_checkout_system import (
    Cart, OrderService, PaymentGateway,
    PaymentStatus, GatewayStatus,
    PaymentNotApprovedError, PaymentProcessingError,
    PaymentPendingError, GatewayUnavailableError,
    OrderAlreadyCreatedError, EmptyCartError,
)

@pytest.fixture
def cart_com_itens():
    return Cart([{"name": "Notebook", "price": 3500.00}])


@pytest.fixture
def payment_data():
    return {"card": "4111111111111111", "cvv": "123", "expiry": "12/28"}


def make_service(gateway_status=GatewayStatus.AVAILABLE,
                 payment_result=PaymentStatus.APPROVED) -> OrderService:
    gw = PaymentGateway(status=gateway_status, payment_result=payment_result)
    return OrderService(gw)


# ─────────────────────────────────────────────
# Cenário 1 — Pagamento aprovado → pedido criado
# ─────────────────────────────────────────────

class TestPedidoCriadoComPagamentoAprovado:
    """
    Scenario: Criar pedido com pagamento aprovado
      Given que o usuário possui itens no carrinho
      And informa dados de pagamento válidos
      And o pagamento é aprovado pelo gateway
      When confirma a compra
      Then o sistema deve criar o pedido
      And deve exibir a confirmação de pedido realizado
    """

    def test_cria_pedido_quando_pagamento_aprovado(self, cart_com_itens, payment_data):
        service = make_service(payment_result=PaymentStatus.APPROVED)

        pedido = service.checkout(cart_com_itens, payment_data)

        assert pedido is not None
        assert pedido["status"] == "confirmed"
        assert "id" in pedido


# ─────────────────────────────────────────────
# Cenário 2 — Pagamento recusado → pedido NÃO criado
# ─────────────────────────────────────────────

class TestPedidoNaoCriadoComPagamentoRecusado:
    """
    Scenario: Não criar pedido com pagamento recusado
      Given que o usuário possui itens no carrinho
      And informa dados de pagamento válidos
      And o pagamento é recusado pelo gateway
      When confirma a compra
      Then o sistema não deve criar o pedido
      And deve exibir a mensagem "Pagamento não aprovado"
    """

    def test_nao_cria_pedido_quando_pagamento_recusado(self, cart_com_itens, payment_data):
        service = make_service(payment_result=PaymentStatus.REFUSED)

        with pytest.raises(PaymentNotApprovedError) as exc:
            service.checkout(cart_com_itens, payment_data)

        assert "Pagamento não aprovado" in str(exc.value)
        assert service._created_order is None


# ─────────────────────────────────────────────
# Cenário 3 — Erro no processamento
# ─────────────────────────────────────────────

class TestPedidoNaoCriadoComErroDePagamento:
    """
    Scenario: Não criar pedido com erro no processamento do pagamento
      Given que o usuário possui itens no carrinho
      And ocorre um erro no processamento do pagamento
      When confirma a compra
      Then o sistema não deve criar o pedido
      And deve exibir a mensagem "Erro ao processar pagamento"
    """

    def test_nao_cria_pedido_quando_erro_de_pagamento(self, cart_com_itens, payment_data):
        service = make_service(payment_result=PaymentStatus.ERROR)

        with pytest.raises(PaymentProcessingError) as exc:
            service.checkout(cart_com_itens, payment_data)

        assert "Erro ao processar pagamento" in str(exc.value)
        assert service._created_order is None


# ─────────────────────────────────────────────
# Cenário 4 — Pagamento pendente → pedido NÃO criado
# ─────────────────────────────────────────────

class TestPedidoNaoCriadoComPagamentoPendente:
    """
    Scenario: Não criar pedido com pagamento pendente
      Given que o usuário possui itens no carrinho
      And o pagamento está com status "pendente"
      When confirma a compra
      Then o sistema não deve criar o pedido
      And deve informar que o pagamento ainda não foi aprovado
    """

    def test_nao_cria_pedido_com_pagamento_pendente(self, cart_com_itens, payment_data):
        service = make_service(payment_result=PaymentStatus.PENDING)

        with pytest.raises(PaymentPendingError) as exc:
            service.checkout(cart_com_itens, payment_data)

        assert "ainda não foi aprovado" in str(exc.value)
        assert service._created_order is None


# ─────────────────────────────────────────────
# Cenário 5 — Nova tentativa após recusa → pedido criado
# ─────────────────────────────────────────────

class TestPedidoCriadoAposRetentativa:
    """
    Scenario: Criar pedido após nova tentativa de pagamento aprovado
      Given que o usuário possui itens no carrinho
      And uma primeira tentativa de pagamento foi recusada
      When o usuário realiza uma nova tentativa de pagamento
      And o pagamento é aprovado
      Then o sistema deve criar o pedido
      And deve exibir a confirmação de pedido realizado
    """

    def test_cria_pedido_na_segunda_tentativa(self, cart_com_itens, payment_data):
        gw = PaymentGateway(status=GatewayStatus.AVAILABLE)
        gw.set_result_for_attempt(1, PaymentStatus.REFUSED)
        gw.set_result_for_attempt(2, PaymentStatus.APPROVED)
        service = OrderService(gw)

        # Primeira tentativa — recusada
        with pytest.raises(PaymentNotApprovedError):
            service.checkout_with_retry(cart_com_itens, payment_data)

        assert service._created_order is None

        # Segunda tentativa — aprovada
        pedido = service.checkout_with_retry(cart_com_itens, payment_data)

        assert pedido is not None
        assert pedido["status"] == "confirmed"


# ─────────────────────────────────────────────
# Cenário 6 — Pedido já criado → sem duplicação
# ─────────────────────────────────────────────

class TestPedidoNaoDuplicado:
    """
    Scenario: Garantir que pedido não seja duplicado após aprovação
      Given que o usuário possui itens no carrinho
      And o pagamento foi aprovado
      And o pedido já foi criado com sucesso
      When o usuário tenta confirmar a compra novamente
      Then o sistema não deve criar um novo pedido
      And deve manter apenas o pedido já existente
    """

    def test_nao_duplica_pedido_ja_criado(self, cart_com_itens, payment_data):
        service = make_service(payment_result=PaymentStatus.APPROVED)

        # Primeiro checkout — sucesso
        pedido_original = service.checkout(cart_com_itens, payment_data)
        assert pedido_original is not None

        # Segunda tentativa — deve bloquear
        with pytest.raises(OrderAlreadyCreatedError):
            service.checkout(cart_com_itens, payment_data)

        # Pedido original permanece intacto
        assert service._created_order == pedido_original


# ─────────────────────────────────────────────
# Bônus — Gateway indisponível (regra de negócio extra)
# ─────────────────────────────────────────────

class TestGatewayIndisponivel:
    """
    Regra: Se o gateway estiver indisponível, o sistema não deve criar
    pedido e deve informar falha de comunicação.
    """

    def test_nao_cria_pedido_com_gateway_indisponivel(self, cart_com_itens, payment_data):
        service = make_service(gateway_status=GatewayStatus.UNAVAILABLE)

        with pytest.raises(GatewayUnavailableError) as exc:
            service.checkout(cart_com_itens, payment_data)

        assert "Falha de comunicação" in str(exc.value)
        assert service._created_order is None


class TestCarrinhoVazioNaoFinalizaCompra:
    """
    Regra: Carrinho vazio não pode seguir para pagamento.
    """

    def test_nao_finaliza_compra_com_carrinho_vazio(self, payment_data):
        service = make_service(payment_result=PaymentStatus.APPROVED)
        cart_vazio = Cart([])

        with pytest.raises(EmptyCartError):
            service.checkout(cart_vazio, payment_data)
