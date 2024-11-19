from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
import re
from django.core.validators import validate_email

# Create your views here.
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        
        # More robust email validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use, choose another one'}, status=409)
        
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': ' sorry username in use, choose another one'}, status=409)

        return JsonResponse({'username_valid': True})  # return a json response


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')    
