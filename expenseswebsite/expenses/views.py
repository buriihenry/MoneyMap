from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@never_cache  # This will prevent caching of this view
@login_required(login_url='/authentication/login')
def index(request):
    return render(request, 'expenses/index.html')

@never_cache  # Prevent caching for this view as well
@login_required(login_url='/authentication/login')
def add_expense(request):
    return render(request, 'expenses/add_expense.html')