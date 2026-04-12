"""Modelos do app de gastos."""

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

CATEGORIAS = [
    ("alimentacao", "Alimentação"),
    ("transporte", "Transporte"),
    ("saude", "Saúde"),
    ("educacao", "Educação"),
    ("lazer", "Lazer"),
    ("moradia", "Moradia"),
    ("outros", "Outros"),
]


class Despesa(models.Model):
    """Representa uma despesa financeira pessoal."""

    descricao = models.CharField("Descrição", max_length=200)
    valor = models.DecimalField(
        "Valor (R$)",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    categoria = models.CharField(
        "Categoria",
        max_length=20,
        choices=CATEGORIAS,
        default="outros",
    )
    data = models.DateField("Data")
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        ordering = ["-data", "-criado_em"]
        verbose_name = "Despesa"
        verbose_name_plural = "Despesas"

    def __str__(self):
        return f"{self.descricao} — R$ {self.valor:.2f}"

    def get_categoria_display_label(self):
        return dict(CATEGORIAS).get(self.categoria, self.categoria)
