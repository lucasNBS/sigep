from django.shortcuts import render

def home(request):
  return render(request, "pages/panel.html", {})

def inventory(request):
  return render(request, "pages/inventory.html", {})

def inventory_detail(request, id):
  return render(request, "pages/inventory-detail.html", {})
