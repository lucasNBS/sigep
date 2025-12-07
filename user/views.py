from django.shortcuts import render

def user(request):
  return render(request, "pages/user.html", {})

def user_detail(request, id):
  return render(request, "pages/user-detail.html", {})

def login(request):
  return render(request, "pages/signin.html", {})

def signup(request):
  return render(request, "pages/signup.html", {})

def forgot_password(request):
  return render(request, "pages/forgot-password.html")

def reset_password(request):
  return render(request, "pages/reset-password.html")

def new_password(request):
  return render(request, "pages/new-password.html", {})