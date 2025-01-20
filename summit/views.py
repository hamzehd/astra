
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, ListView

from django.shortcuts import redirect

from summit.forms import SummarizeForm
from summit.models import Song


class HomepageView(TemplateView):
    template_name = 'homepage.html'


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

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
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


class SummarizeView(FormView):
    template_name = 'summarize.html'
    form_class = SummarizeForm
    success_url = reverse_lazy('inquiries_list')

    def form_valid(self, form):
        data = form.save(self.request.user)
        response = super().form_valid(form)
        return response
    
    def form_invalid(self, form):
        for error in form.errors:
            messages.error(self.request, form.errors[error])
            return redirect(self.request.path)
        return super().form_invalid(form)


class InquiriesView(ListView):
    template_name = 'inquiry_list.html'
    model = Song

    def get_queryset(self):
        queryset = Song.objects.filter(requested_by=self.request.user).all()
        return queryset
