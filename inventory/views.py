from django.shortcuts import render

def inventory_form(request):
  return render(request, "pages/inventory-form.html", {})

def inventory(request):
  return render(request, "pages/inventory.html", {})

def inventory_detail(request, id):
  return render(request, "pages/inventory-detail.html", {})
