from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_http_methods
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm



@require_http_methods(["POST", "GET"])
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            # return redirect('index')
        
    else:
        form = CustomUserCreationForm()
    
    context = {"form": form}
    return render(request, "accounts/signup.html", context)


@require_http_methods(["POST", "GET"])
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # return redirect("index")
    
    else:
        form = AuthenticationForm()
        context = {"form": form}
        return render(request, "accounts/login.html", context)


@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    # return redirect("index")













