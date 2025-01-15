
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'homepage.html')


def login_view(request):
    """
    Handles user authentication and login functionality.

    This view processes both GET and POST requests:
    - GET: Renders the login form
    - POST: Authenticates user credentials and logs in valid superusers

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: Renders login.html template for GET requests and invalid logins
        HttpResponseRedirect: Redirects to index page on successful login
    """
    from django.shortcuts import redirect
    from django.contrib.auth import authenticate, login as auth_login
    from django.contrib import messages

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid login credentials or insufficient permissions.')
            return render(request, 'login.html')
    
    return render(request, 'login.html')

@login_required()
def logout_view(request):
    """
    Simple Logout View
    """
    logout(request)
    return HttpResponseRedirect('/')
