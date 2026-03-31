"""
test_frete.py
Feature: Cálculo de frete com base no CEP
Baseado nos 6 cenários BDD escritos para o MiniCommerce.
"""

import pytest
from test_checkout_system import (
    Cart, FreightService,
    InvalidCEPError, InternationalCEPError,
)


@pytest.fixture
def cart_com_itens():
    """Carrinho com pelo menos um item — pré-condição de todos os cenários."""
    return Cart([{"name": "Camiseta", "price": 89.90}])


@pytest.fixture
def freight():
    return FreightService()


# ─────────────────────────────────────────────
# Cenário 1 — CEP nacional válido com hífen
# ─────────────────────────────────────────────

class TestCepNacionalValido:
    """
    Scenario: Calcular frete com CEP nacional válido
      Given que o usuário possui itens no carrinho
      And informa um CEP nacional válido "01001-000"
      When solicita o cálculo de frete
      Then o sistema deve calcular o frete com sucesso
      And deve exibir as opções de entrega disponíveis
    """

    def test_retorna_opcoes_de_entrega(self, cart_com_itens, freight):
        # When
        opcoes = freight.calculate(cart_com_itens, "01001-000")

        # Then
        assert isinstance(opcoes, list)
        assert len(opcoes) > 0
        assert all("type" in o and "price" in o for o in opcoes)


# ─────────────────────────────────────────────
# Cenário 2 — CEP com formato incorreto (curto)
# ─────────────────────────────────────────────

class TestCepFormatoIncorreto:
    """
    Scenario: Não calcular frete com CEP inválido (formato incorreto)
      Given que o usuário possui itens no carrinho
      And informa um CEP inválido "123"
      When solicita o cálculo de frete
      Then o sistema não deve calcular o frete
      And deve exibir a mensagem "CEP inválido"
    """

    def test_levanta_erro_cep_invalido(self, cart_com_itens, freight):
        with pytest.raises(InvalidCEPError) as exc:
            freight.calculate(cart_com_itens, "123")

        assert "CEP inválido" in str(exc.value)

    def test_nao_retorna_opcoes_de_entrega(self, cart_com_itens, freight):
        with pytest.raises(InvalidCEPError):
            freight.calculate(cart_com_itens, "123")


# ─────────────────────────────────────────────
# Cenário 3 — CEP internacional (5 dígitos, padrão US ZIP)
# ─────────────────────────────────────────────

class TestCepInternacional:
    """
    Scenario: Não calcular frete com CEP internacional
      Given que o usuário possui itens no carrinho
      And informa um CEP internacional "90210"
      When solicita o cálculo de frete
      Then o sistema não deve calcular o frete
      And deve exibir a mensagem "Frete disponível apenas para CEP nacional"
    """

    def test_levanta_erro_cep_internacional(self, cart_com_itens, freight):
        with pytest.raises(InternationalCEPError) as exc:
            freight.calculate(cart_com_itens, "90210")

        assert "Frete disponível apenas para CEP nacional" in str(exc.value)


# ─────────────────────────────────────────────
# Cenário 4 — CEP vazio / não informado
# ─────────────────────────────────────────────

class TestCepVazio:
    """
    Scenario: Não calcular frete com CEP vazio
      Given que o usuário possui itens no carrinho
      And não informa nenhum CEP
      When solicita o cálculo de frete
      Then o sistema não deve calcular o frete
      And deve exibir a mensagem "CEP obrigatório"
    """

    @pytest.mark.parametrize("cep_vazio", ["", "   ", None])
    def test_levanta_erro_cep_obrigatorio(self, cart_com_itens, freight, cep_vazio):
        with pytest.raises(InvalidCEPError) as exc:
            freight.calculate(cart_com_itens, cep_vazio or "")

        assert "CEP obrigatório" in str(exc.value)


# ─────────────────────────────────────────────
# Cenário 5 — CEP contendo letras
# ─────────────────────────────────────────────

class TestCepComLetras:
    """
    Scenario: Não calcular frete com CEP contendo letras
      Given que o usuário possui itens no carrinho
      And informa um CEP "ABCDE-123"
      When solicita o cálculo de frete
      Then o sistema não deve calcular o frete
      And deve exibir a mensagem "CEP inválido"
    """

    @pytest.mark.parametrize("cep_com_letra", ["ABCDE-123", "1234A-567", "abc"])
    def test_levanta_erro_para_cep_com_letras(self, cart_com_itens, freight, cep_com_letra):
        with pytest.raises(InvalidCEPError) as exc:
            freight.calculate(cart_com_itens, cep_com_letra)

        assert "CEP inválido" in str(exc.value)


# ─────────────────────────────────────────────
# Cenário 6 — CEP válido sem hífen
# ─────────────────────────────────────────────

class TestCepSemHifen:
    """
    Scenario: Calcular frete com CEP válido sem hífen
      Given que o usuário possui itens no carrinho
      And informa um CEP nacional válido "01001000"
      When solicita o cálculo de frete
      Then o sistema deve calcular o frete com sucesso
      And deve exibir as opções de entrega disponíveis
    """

    def test_aceita_cep_sem_hifen(self, cart_com_itens, freight):
        opcoes = freight.calculate(cart_com_itens, "01001000")

        assert isinstance(opcoes, list)
        assert len(opcoes) > 0
