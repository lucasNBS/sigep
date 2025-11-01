from django.shortcuts import render

def home(request):
  return render(request, "pages/panel.html", {})

def user(request):
  return render(request, "pages/user.html", {})

def patrimony(request):
  return render(request, "pages/patrimony.html", {})

def profile(request):
  return render(request, "pages/profile.html", {})
