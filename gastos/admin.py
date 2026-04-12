"""Configuração do admin para o app de gastos."""

from django.contrib import admin

from .models import Despesa


@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = ["descricao", "valor", "categoria", "data", "criado_em"]
    list_filter = ["categoria", "data"]
    search_fields = ["descricao"]
    date_hierarchy = "data"
