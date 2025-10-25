from django.shortcuts import render

def home(request):
  return render(request, "pages/panel.html", {})

def records(request):
  return render(request, "pages/record.html", {})