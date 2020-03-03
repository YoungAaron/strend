from django import forms
from stock.models import *

class StockListForm(forms.ModelForm):

    class Meta:
        model = StockList
        fields = '__all__'