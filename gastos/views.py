"""Views do app de gastos."""

from decimal import Decimal

from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import DespesaForm
from .models import CATEGORIAS, Despesa


def index(request):
    """Lista todas as despesas com resumo por categoria."""
    despesas = Despesa.objects.all()

    # Filtro por categoria (opcional)
    categoria_filtro = request.GET.get("categoria", "")
    if categoria_filtro:
        despesas = despesas.filter(categoria=categoria_filtro)

    # Total geral
    total = despesas.aggregate(total=Sum("valor"))["total"] or Decimal("0.00")

    # Resumo por categoria
    resumo = []
    for cod, nome in CATEGORIAS:
        subtotal = (
            Despesa.objects.filter(categoria=cod).aggregate(s=Sum("valor"))["s"]
            or Decimal("0.00")
        )
        if subtotal > 0:
            resumo.append({"nome": nome, "total": subtotal})

    context = {
        "despesas": despesas,
        "total": total,
        "resumo": resumo,
        "categorias": CATEGORIAS,
        "categoria_filtro": categoria_filtro,
        "mes_atual": timezone.now().strftime("%B de %Y"),
    }
    return render(request, "gastos/index.html", context)


def adicionar(request):
    """Adiciona uma nova despesa."""
    if request.method == "POST":
        form = DespesaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Despesa adicionada com sucesso!")
            return redirect("gastos:index")
    else:
        form = DespesaForm(initial={"data": timezone.now().date()})

    return render(request, "gastos/despesa_form.html", {"form": form, "titulo": "Adicionar Despesa"})


def editar(request, pk):
    """Edita uma despesa existente."""
    despesa = get_object_or_404(Despesa, pk=pk)
    if request.method == "POST":
        form = DespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            messages.success(request, "Despesa atualizada com sucesso!")
            return redirect("gastos:index")
    else:
        form = DespesaForm(instance=despesa)

    return render(request, "gastos/despesa_form.html", {"form": form, "titulo": "Editar Despesa"})


def excluir(request, pk):
    """Exclui uma despesa."""
    despesa = get_object_or_404(Despesa, pk=pk)
    if request.method == "POST":
        despesa.delete()
        messages.success(request, "Despesa removida com sucesso!")
        return redirect("gastos:index")

    return render(request, "gastos/confirmar_exclusao.html", {"despesa": despesa})
