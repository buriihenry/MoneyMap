from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
import json
from django.http import JsonResponse


def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(
            amount__starts_with=search_str, owner= request.user) | Expense.objects.filter(
            date__starts_with=search_str, owner= request.user) | Expense.objects.filter(
            description__icontains=search_str, owner= request.user) | Expense.objects.filter(
            category__icontains=search_str, owner= request.user)
        
        data = expenses.values()

        return JsonResponse(list(data), safe=False)



@login_required(login_url='/authentication/login')
def index(request):
    expenses = Expense.objects.filter(owner=request.user)
    
    # Pagination
    paginator = Paginator(expenses, 5)  # Show 5 expenses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get user currency preference safely
    try:
        user_preference = UserPreference.objects.get(user=request.user)
        currency = user_preference.currency
    except UserPreference.DoesNotExist:
        currency = 'USD'  # Default fallback
        UserPreference.objects.create(user=request.user, currency=currency)
    
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('expense_date')
        category = request.POST.get('category')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', context)

        try:
            amount = float(amount)
        except ValueError:
            messages.error(request, 'Invalid amount format')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(
            owner=request.user,
            amount=amount,
            date=date,
            category=category,
            description=description
        )
        messages.success(request, 'Expense saved successfully')
        return redirect('expenses')


@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    try:
        expense = Expense.objects.get(pk=id, owner=request.user)
        categories = Category.objects.all()
        context = {
            'expense': expense,
            'values': expense,
            'categories': categories
        }

        if request.method == 'GET':
            return render(request, 'expenses/edit-expense.html', context)

        if request.method == 'POST':
            amount = request.POST.get('amount')
            description = request.POST.get('description')
            date = request.POST.get('expense_date')
            category = request.POST.get('category')

            if not amount:
                messages.error(request, 'Amount is required')
                return render(request, 'expenses/edit-expense.html', context)

            if not description:
                messages.error(request, 'Description is required')
                return render(request, 'expenses/edit-expense.html', context)

            try:
                amount = float(amount)
            except ValueError:
                messages.error(request, 'Invalid amount format')
                return render(request, 'expenses/edit-expense.html', context)

            expense.amount = amount
            expense.date = date
            expense.category = category
            expense.description = description
            expense.save()
            
            messages.success(request, 'Expense updated successfully')
            return redirect('expenses')

    except Expense.DoesNotExist:
        messages.error(request, 'Expense not found')
        return redirect('expenses')
    
def delete_expense(request,id):
    expense = Expense.objects.get(pk=id, owner=request.user)
    expense.delete()
    messages.success(request, 'Expense Removed')
    return redirect('expenses')