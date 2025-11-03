from django.shortcuts import render

def home(request):
  return render(request, "pages/panel.html", {})

def login(request):
  return render(request, "pages/signin.html", {})

def signup(request):
  return render(request, "pages/signup.html", {})

def forgot_password(request):
  return render(request, "pages/forgot-password.html")

def reset_password(request):
  return render(request, "pages/reset-password.html")

def reset_password2(request):
  return render(request, "pages/reset-password2.html", {})

def new_password(request):
  return render(request, "pages/new-password.html", {})