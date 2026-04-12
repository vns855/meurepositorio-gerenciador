"""Formulários do app de gastos."""

from django import forms

from .models import Despesa


class DespesaForm(forms.ModelForm):
    """Formulário para criação e edição de despesas."""

    class Meta:
        model = Despesa
        fields = ["descricao", "valor", "categoria", "data"]
        widgets = {
            "descricao": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ex: Almoço, Ônibus..."}
            ),
            "valor": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "min": "0.01"}
            ),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "data": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }

    def clean_valor(self):
        valor = self.cleaned_data.get("valor")
        if valor is not None and valor <= 0:
            raise forms.ValidationError("O valor deve ser maior que zero.")
        return valor

    def clean_descricao(self):
        descricao = self.cleaned_data.get("descricao", "").strip()
        if not descricao:
            raise forms.ValidationError("A descrição não pode estar vazia.")
        return descricao
