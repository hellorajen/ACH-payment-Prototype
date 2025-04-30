from django import forms
from .models import BankAccount, ACHEntry
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_holder_name', 'account_type', 'routing_number', 'account_number', 'institution_name']
        widgets = {
            'account_number': forms.PasswordInput(render_value=True),
            'routing_number': forms.PasswordInput(render_value=True),
        }

    def clean_routing_number(self):
        routing_number = self.cleaned_data['routing_number']
        if not routing_number.isdigit() or len(routing_number) != 9:
            raise forms.ValidationError("Routing number must be 9 digits")
        return routing_number

    def clean_account_number(self):
        account_number = self.cleaned_data['account_number']
        if not account_number.isdigit() or len(account_number) < 5 or len(account_number) > 17:
            raise forms.ValidationError("Account number must be between 5-17 digits")
        return account_number

class ACHEntryForm(forms.ModelForm):
    class Meta:
        model = ACHEntry
        fields = ['source_account', 'destination_account', 'amount', 'description']
        
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source_account'].queryset = BankAccount.objects.filter(user=user, is_verified=True)
        self.fields['destination_account'].queryset = BankAccount.objects.filter(user=user, is_verified=True)
        
        # Add proper amount field validation
        self.fields['amount'] = forms.DecimalField(
            max_digits=10,
            decimal_places=2,
            validators=[MinValueValidator(0.01)],
            widget=forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0.01'
            })
        )