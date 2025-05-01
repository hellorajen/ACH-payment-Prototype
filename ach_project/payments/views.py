from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import authenticate, login  # ADDED
from .models import BankAccount, ACHEntry
from .forms import BankAccountForm, ACHEntryForm
from django.conf import settings
import requests
from django.http import JsonResponse, HttpResponse  # Added HttpResponse
from django.contrib.auth.models import User
import json
from .models import Transfer  # Assuming you have a Transfer model for tracking transfers

@login_required
def sensitive_action(request):
    response = HttpResponse()
    response['X-Frame-Options'] = 'DENY'
    response['Content-Security-Policy'] = "default-src 'self'"
    return response

@login_required
def login_view(request):
    if request.user.is_authenticated:  # Prevent logged-in users from accessing login page
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            remember = request.POST.get('remember')
            request.session.set_expiry(2592000 if remember else 0)
            next_url = request.GET.get('next', 'dashboard')  # Handle 'next' parameter
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'registration/login.html')

@login_required
def dashboard(request):
    accounts = BankAccount.objects.filter(user=request.user)
    transactions = ACHEntry.objects.filter(user=request.user).order_by('-created_at')[:10]
    return render(request, 'payments/dashboard.html', {
        'accounts': accounts,
        'transactions': transactions
    })

@login_required
def add_bank_account(request):
    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            
            # In a real app, we would verify with Plaid or similar service
            # For prototype, we'll just mark as verified after basic validation
            account.is_verified = True
            account.save()
            
            messages.success(request, "Bank account added successfully!")
            return redirect('dashboard')
    else:
        form = BankAccountForm()
    
    return render(request, 'payments/add_bank_account.html', {'form': form})

@login_required
@transaction.atomic  # Ensures all operations complete or none do
def initiate_transfer(request):
    if request.method == 'POST':
        form = ACHEntryForm(request.user, request.POST)
        if form.is_valid():
            source = form.cleaned_data['source_account']
            destination = form.cleaned_data['destination_account']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']

            # Validate sufficient funds
            if source.balance < amount:
                messages.error(request, "Insufficient funds in source account")
                return redirect('initiate_transfer')

            # Validate different accounts
            if source == destination:
                messages.error(request, "Cannot transfer to the same account")
                return redirect('initiate_transfer')

            try:
                # 1. Deduct from source
                source.balance -= amount
                source.save()

                # 2. Add to destination
                destination.balance += amount
                destination.save()

                # 3. Create transaction record
                ACHEntry.objects.create(
                    user=request.user,
                    source_account=source,
                    destination_account=destination,
                    amount=amount,
                    description=description,
                    status='processed'
                )

                messages.success(request, f"Successfully transferred ${amount:,.2f}")
                return redirect('dashboard')

            except Exception as e:
                messages.error(request, f"Transfer failed: {str(e)}")
                transaction.set_rollback(True)  # Rollback on error

    else:
        form = ACHEntryForm(request.user)

    return render(request, 'payments/initiate_transfer.html', {'form': form})

def mock_plaid_verification(request):
    """Mock endpoint to simulate Plaid verification webhook"""
    # In a real app, this would be handled by Plaid's webhooks
    # For prototype, we'll just verify all accounts
    if request.method == 'POST':
        data = json.loads(request.body)
        account_id = data.get('account_id')
        
        try:
            account = BankAccount.objects.get(id=account_id)
            account.is_verified = True
            account.save()
            return JsonResponse({'status': 'success'})
        except BankAccount.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Account not found'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400)


def transfer_details(request, transfer_id):
    transfer = Transfer.objects.get(id=transfer_id)
    logs = transfer.history.all()  # Query audit logs for this transfer
    return render(request, 'transfer_details.html', {'transfer': transfer, 'logs': logs})