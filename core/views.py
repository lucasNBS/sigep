from django.shortcuts import render

def home(request):
  return render(request, "pages/dashboard.html", {})

def reset_password2(request):
  return render(request, "pages/reset-password2.html", {})

def patrimony_create(request):
  return render(request, "pages/patrimony-form.html", { 'title': 'Cadastrar Item' })

def patrimony_edit(request, id):
  return render(request, "pages/patrimony-form.html", { 'title': 'Editar Item' })

def inventory_form(request):
  return render(request, "pages/inventory-form.html", {})

def patrimony_detail(request, id):
  return render(request, "pages/patrimony-detail.html", {})

def record_form(request, id):
  return render(request, "pages/record-form.html", {})

def inventory(request):
  return render(request, "pages/inventory.html", {})

def inventory_detail(request, id):
  return render(request, "pages/inventory-detail.html", {})

def records(request):
  return render(request, "pages/record.html", {})

def records_scan(request):
  return render(request, "pages/record-scan.html", {})

def patrimony(request):
  return render(request, "pages/patrimony.html", {})

def profile(request):
  return render(request, "pages/profile.html", {})
