from django.shortcuts import render

def home(request):
  return render(request, "pages/panel.html", {})

def patrimony_form(request):
  return render(request, "pages/patrimony-form.html", {})

def inventory_form(request):
  return render(request, "pages/inventory-form.html", {})

def patrimony_detail(request, id):
  return render(request, "pages/patrimony-detail.html", {})

def record_form(request, id):
  return render(request, "pages/record-form.html", {})
