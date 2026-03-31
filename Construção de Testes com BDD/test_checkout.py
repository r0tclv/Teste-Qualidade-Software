"""
checkout_system.py
Lógica de negócio simulada do MiniCommerce (stubs para testes).
"""
import re
from enum import Enum

class PaymentStatus(Enum):
    APPROVED = "approved"
    REFUSED  = "refused"
    PENDING  = "pending"
    ERROR    = "error"


class GatewayStatus(Enum):
    AVAILABLE   = "available"
    UNAVAILABLE = "unavailable"

INSTALLMENT_MIN_VALUE = 100.00   # R$ mínimo para parcelamento


# ─────────────────────────────────────────────
# Exceções de domínio
# ─────────────────────────────────────────────

class EmptyCartError(Exception):
    pass

class InvalidCEPError(Exception):
    pass

class InternationalCEPError(Exception):
    pass

class PaymentNotApprovedError(Exception):
    pass

class PaymentProcessingError(Exception):
    pass

class PaymentPendingError(Exception):
    pass

class GatewayUnavailableError(Exception):
    pass

class OrderAlreadyCreatedError(Exception):
    pass

class CouponExpiredError(Exception):
    pass

class CouponInvalidError(Exception):
    pass

class CouponNotFoundError(Exception):
    pass

class MultipleCouponsError(Exception):
    pass


# ─────────────────────────────────────────────
# Carrinho
# ─────────────────────────────────────────────

class Cart:
    def __init__(self, items: list[dict]):
        """
        items: lista de dicts com 'name' e 'price'
        ex.: [{"name": "Camisa", "price": 80.00}]
        """
        self.items = items

    @property
    def total(self) -> float:
        return sum(i["price"] for i in self.items)

    @property
    def is_empty(self) -> bool:
        return len(self.items) == 0


# ─────────────────────────────────────────────
# Serviço de frete
# ─────────────────────────────────────────────

# Padrão aceito: NNNNNNNN ou NNNNN-NNN  (somente dígitos nacionais)
_CEP_REGEX = re.compile(r"^\d{5}-?\d{3}$")

# Prefixos de CEP internacional conhecidos (ex.: ZIP codes dos EUA = 5 dígitos sem hífen)
# Regra simples: CEP internacional é qualquer coisa que não bate no padrão nacional
# Para fins de teste, qualquer string com 5 dígitos sem hífen é tratada como internacional
_INTL_CEP_REGEX = re.compile(r"^\d{5}$")


class FreightService:
    @staticmethod
    def calculate(cart: Cart, cep: str) -> list[dict]:
        """
        Retorna lista de opções de entrega ou lança exceção.
        """
        if cart.is_empty:
            raise EmptyCartError("Carrinho vazio")

        if not cep or cep.strip() == "":
            raise InvalidCEPError("CEP obrigatório")

        # CEP com letras → inválido
        if re.search(r"[a-zA-Z]", cep):
            raise InvalidCEPError("CEP inválido")

        # CEP internacional (5 dígitos sem hífen)
        if _INTL_CEP_REGEX.match(cep):
            raise InternationalCEPError("Frete disponível apenas para CEP nacional")

        # CEP fora do formato nacional
        if not _CEP_REGEX.match(cep):
            raise InvalidCEPError("CEP inválido")

        # Sucesso: retorna opções fictícias
        return [
            {"type": "PAC",    "days": 7,  "price": 15.90},
            {"type": "SEDEX",  "days": 2,  "price": 32.50},
        ]


# ─────────────────────────────────────────────
# Serviço de parcelamento
# ─────────────────────────────────────────────

class InstallmentService:
    @staticmethod
    def get_options(cart: Cart) -> list[dict] | None:
        """
        Retorna opções de parcelamento ou None se não elegível.
        """
        if cart.total < INSTALLMENT_MIN_VALUE:
            return None

        # Gera até 12x sem juros (simplificado)
        options = []
        for n in range(1, 13):
            options.append({"installments": n, "value": round(cart.total / n, 2)})
        return options


# ─────────────────────────────────────────────
# Gateway de pagamento (stub configurável)
# ─────────────────────────────────────────────

class PaymentGateway:
    def __init__(self, status: GatewayStatus = GatewayStatus.AVAILABLE,
                 payment_result: PaymentStatus = PaymentStatus.APPROVED):
        self.status         = status
        self.payment_result = payment_result
        self._attempt       = 0

    def process(self, payment_data: dict) -> PaymentStatus:
        if self.status == GatewayStatus.UNAVAILABLE:
            raise GatewayUnavailableError("Falha de comunicação com o gateway")

        self._attempt += 1
        return self.payment_result

    def set_result_for_attempt(self, attempt: int, result: PaymentStatus):
        """Permite configurar resultado diferente por tentativa (para cenário retry)."""
        self._results_by_attempt = getattr(self, "_results_by_attempt", {})
        self._results_by_attempt[attempt] = result

    def process_with_retry_support(self, payment_data: dict) -> PaymentStatus:
        if self.status == GatewayStatus.UNAVAILABLE:
            raise GatewayUnavailableError("Falha de comunicação com o gateway")
        self._attempt += 1
        results = getattr(self, "_results_by_attempt", {})
        return results.get(self._attempt, self.payment_result)


# ─────────────────────────────────────────────
# Serviço de pedidos
# ─────────────────────────────────────────────

class OrderService:
    def __init__(self, gateway: PaymentGateway):
        self.gateway        = gateway
        self._created_order = None    # simula persistência simples

    def checkout(self, cart: Cart, payment_data: dict) -> dict:
        if cart.is_empty:
            raise EmptyCartError("Carrinho vazio não pode seguir para pagamento")

        # Verifica se pedido já existe (evita duplicação)
        if self._created_order is not None:
            raise OrderAlreadyCreatedError("Pedido já foi criado")

        # Processa pagamento
        try:
            result = self.gateway.process(payment_data)
        except GatewayUnavailableError:
            raise  # propaga

        if result == PaymentStatus.REFUSED:
            raise PaymentNotApprovedError("Pagamento não aprovado")
        if result == PaymentStatus.ERROR:
            raise PaymentProcessingError("Erro ao processar pagamento")
        if result == PaymentStatus.PENDING:
            raise PaymentPendingError("Pagamento ainda não foi aprovado")

        # Cria pedido
        self._created_order = {
            "id":    "ORD-0001",
            "total": cart.total,
            "status": "confirmed",
        }
        return self._created_order

    def checkout_with_retry(self, cart: Cart, payment_data: dict) -> dict:
        """Versão que usa gateway com suporte a retry."""
        if cart.is_empty:
            raise EmptyCartError("Carrinho vazio")
        if self._created_order is not None:
            raise OrderAlreadyCreatedError("Pedido já foi criado")

        result = self.gateway.process_with_retry_support(payment_data)

        if result == PaymentStatus.REFUSED:
            raise PaymentNotApprovedError("Pagamento não aprovado")
        if result == PaymentStatus.ERROR:
            raise PaymentProcessingError("Erro ao processar pagamento")
        if result == PaymentStatus.PENDING:
            raise PaymentPendingError("Pagamento ainda não foi aprovado")

        self._created_order = {"id": "ORD-0001", "total": cart.total, "status": "confirmed"}
        return self._created_order


# ─────────────────────────────────────────────
# Serviço de cupons
# ─────────────────────────────────────────────

from datetime import date

VALID_COUPONS = {
    "DESCONTO10": {"discount": 0.10, "expires": date(2099, 12, 31)},
    "PROMO20":    {"discount": 0.20, "expires": date(2099, 12, 31)},
}

EXPIRED_COUPONS = {
    "DESCONTO10_OLD": {"discount": 0.10, "expires": date(2000, 1, 1)},
}


class CouponService:
    def __init__(self):
        self._applied_coupon: str | None = None

    def apply(self, cart: Cart, code: str, reference_date: date = None) -> float:
        """
        Aplica cupom e retorna novo total.
        reference_date permite simular expiração durante sessão.
        """
        ref = reference_date or date.today()

        # Checa se já tem cupom aplicado
        if self._applied_coupon is not None:
            raise MultipleCouponsError("Apenas um cupom pode ser utilizado por pedido")

        # Busca o cupom
        if code in VALID_COUPONS:
            coupon = VALID_COUPONS[code]
            if coupon["expires"] < ref:
                raise CouponExpiredError("Cupom expirado")
            self._applied_coupon = code
            return round(cart.total * (1 - coupon["discount"]), 2)

        if code in EXPIRED_COUPONS:
            raise CouponExpiredError("Cupom expirado")

        # Formato válido mas não existe
        if re.match(r"^[A-Z0-9]{3,20}$", code):
            raise CouponNotFoundError("Cupom não encontrado")

        raise CouponInvalidError("Cupom inválido")

    def expire_applied_coupon(self, cart: Cart) -> float:
        """Simula expiração do cupom durante a sessão."""
        self._applied_coupon = None
        return cart.total   # volta ao total original

    @property
    def has_coupon(self) -> bool:
        return self._applied_coupon is not None