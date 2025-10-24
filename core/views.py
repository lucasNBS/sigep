from django.shortcuts import render

def home(request):
  return render(request, "pages/panel.html", {})

def patrimony(request):
  return render(request, "pages/patrimony.html", {})