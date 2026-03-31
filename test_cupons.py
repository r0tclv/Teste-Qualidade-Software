"""
test_cupons.py
Feature: Aplicação de cupons de desconto
Baseado nos 6 cenários BDD escritos para o MiniCommerce.
"""
import pytest
from datetime import date
from test_checkout_system import (
    Cart, CouponService,
    CouponExpiredError, CouponInvalidError,
    CouponNotFoundError, MultipleCouponsError,
)

@pytest.fixture
def cart():
    return Cart([{"name": "Tênis", "price": 200.00}])


@pytest.fixture
def coupon_service():
    return CouponService()


# ─────────────────────────────────────────────
# Cenário 1 — Cupom válido dentro do prazo
# ─────────────────────────────────────────────

class TestCupomValidoDentroDoPrazo:
    """
    Scenario: Aplicar cupom válido dentro do prazo
      Given que o usuário possui itens no carrinho
      And informa um cupom válido "DESCONTO10"
      And o cupom está dentro do prazo de validade
      When aplica o cupom
      Then o sistema deve aplicar o desconto ao total do pedido
      And deve exibir o valor atualizado
    """

    def test_aplica_desconto_para_cupom_valido(self, cart, coupon_service):
        total_original = cart.total  # 200.00

        novo_total = coupon_service.apply(cart, "DESCONTO10")

        # 10% de desconto sobre 200 = 180.00
        assert novo_total == pytest.approx(180.00, rel=1e-2)
        assert novo_total < total_original

    def test_cupom_e_registrado_como_aplicado(self, cart, coupon_service):
        coupon_service.apply(cart, "DESCONTO10")

        assert coupon_service.has_coupon is True


# ─────────────────────────────────────────────
# Cenário 2 — Cupom expirado
# ─────────────────────────────────────────────

class TestCupomExpirado:
    """
    Scenario: Não aplicar cupom expirado
      Given que o usuário possui itens no carrinho
      And informa um cupom "DESCONTO10"
      And o cupom está fora do prazo de validade
      When tenta aplicar o cupom
      Then o sistema não deve aplicar o desconto
      And deve exibir a mensagem "Cupom expirado"
    """

    def test_nao_aplica_cupom_expirado_pelo_banco(self, cart, coupon_service):
        """Testa cupom que existe no banco mas já está expirado."""
        with pytest.raises(CouponExpiredError) as exc:
            coupon_service.apply(cart, "DESCONTO10_OLD")

        assert "Cupom expirado" in str(exc.value)
        assert coupon_service.has_coupon is False

    def test_nao_aplica_cupom_valido_com_data_passada(self, cart, coupon_service):
        """Simula que hoje já passou da validade do cupom DESCONTO10."""
        data_futura = date(2100, 1, 1)  # Cupom expira em 2099

        with pytest.raises(CouponExpiredError) as exc:
            coupon_service.apply(cart, "DESCONTO10", reference_date=data_futura)

        assert "Cupom expirado" in str(exc.value)


# ─────────────────────────────────────────────
# Cenário 3 — Cupom inválido (formato errado)
# ─────────────────────────────────────────────

class TestCupomInvalido:
    """
    Scenario: Não aplicar cupom inválido
      Given que o usuário possui itens no carrinho
      And informa um cupom inválido "ABC123"  (existe no banco mas formato é inválido / não existe)
      When tenta aplicar o cupom
      Then o sistema não deve aplicar o desconto
      And deve exibir a mensagem "Cupom inválido"
    """

    @pytest.mark.parametrize("codigo_invalido", [
        "ab",          # muito curto / minúsculas
        "!!@@##",      # caracteres especiais
        "A B C",       # espaços
    ])
    def test_nao_aplica_cupom_com_formato_invalido(self, cart, coupon_service, codigo_invalido):
        with pytest.raises(CouponInvalidError) as exc:
            coupon_service.apply(cart, codigo_invalido)

        assert "Cupom inválido" in str(exc.value)


# ─────────────────────────────────────────────
# Cenário 4 — Cupom inexistente
# ─────────────────────────────────────────────

class TestCupomInexistente:
    """
    Scenario: Não aplicar cupom inexistente
      Given que o usuário possui itens no carrinho
      And informa um cupom inexistente "NAOEXISTE"
      When tenta aplicar o cupom
      Then o sistema não deve aplicar o desconto
      And deve exibir a mensagem "Cupom não encontrado"
    """

    def test_nao_aplica_cupom_inexistente(self, cart, coupon_service):
        with pytest.raises(CouponNotFoundError) as exc:
            coupon_service.apply(cart, "NAOEXISTE")

        assert "Cupom não encontrado" in str(exc.value)
        assert coupon_service.has_coupon is False


# ─────────────────────────────────────────────
# Cenário 5 — Cupom expira durante a sessão
# ─────────────────────────────────────────────

class TestCupomExpiraDuranteASessao:
    """
    Scenario: Remover desconto ao expirar durante a sessão
      Given que o usuário possui itens no carrinho
      And aplica um cupom válido
      When o cupom expira antes da finalização da compra
      Then o sistema deve remover o desconto aplicado
      And deve atualizar o valor total do pedido
    """

    def test_remove_desconto_quando_cupom_expira_na_sessao(self, cart, coupon_service):
        total_original = cart.total  # 200.00

        # Aplica cupom com sucesso
        total_com_desconto = coupon_service.apply(cart, "DESCONTO10")
        assert total_com_desconto < total_original
        assert coupon_service.has_coupon is True

        # Cupom expira durante a sessão
        total_atualizado = coupon_service.expire_applied_coupon(cart)

        # Total volta ao original
        assert total_atualizado == pytest.approx(total_original, rel=1e-2)
        assert coupon_service.has_coupon is False


# ─────────────────────────────────────────────
# Cenário 6 — Apenas um cupom por pedido
# ─────────────────────────────────────────────

class TestApenasUmCupomPorPedido:
    """
    Scenario: Aplicar apenas um cupom válido por vez
      Given que o usuário possui itens no carrinho
      And aplica um cupom válido "DESCONTO10"
      When tenta aplicar outro cupom válido "PROMO20"
      Then o sistema deve manter apenas um cupom aplicado
      And deve exibir a mensagem "Apenas um cupom pode ser utilizado por pedido"
    """

    def test_bloqueia_segundo_cupom(self, cart, coupon_service):
        # Aplica o primeiro cupom
        coupon_service.apply(cart, "DESCONTO10")
        assert coupon_service.has_coupon is True

        # Tenta aplicar segundo cupom
        with pytest.raises(MultipleCouponsError) as exc:
            coupon_service.apply(cart, "PROMO20")

        assert "Apenas um cupom pode ser utilizado por pedido" in str(exc.value)

    def test_apenas_o_primeiro_cupom_permanece(self, cart, coupon_service):
        total_esperado = pytest.approx(180.00, rel=1e-2)  # 10% de 200

        coupon_service.apply(cart, "DESCONTO10")

        try:
            coupon_service.apply(cart, "PROMO20")
        except MultipleCouponsError:
            pass  # esperado

        # Confirma que o desconto aplicado é ainda o do primeiro cupom (10%)
        # Verificamos pelo estado do serviço
        assert coupon_service._applied_coupon == "DESCONTO10"
