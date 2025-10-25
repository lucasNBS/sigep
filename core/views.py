from django.shortcuts import render

def home(request):
  return render(request, "pages/panel.html", {})

def user(request):
  return render(request, "pages/user.html", {})