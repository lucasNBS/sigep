from django.shortcuts import render

def home(request):
  return render(request, "pages/dashboard.html", {})

def profile(request):
  return render(request, "pages/profile.html", {})
