from django.shortcuts import render

def home(request):
  return render(request, "pages/panel.html", {})

def records(request):
  return render(request, "pages/record.html", {})

def patrimony(request):
  return render(request, "pages/patrimony.html", {})

def profile(request):
  return render(request, "pages/profile.html", {})
