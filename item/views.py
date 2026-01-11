from django.shortcuts import render

def patrimony(request):
  return render(request, "pages/patrimony.html", {})

def patrimony_create(request):
  return render(request, "pages/patrimony-form.html", { 'title': 'Cadastrar Item' })

def patrimony_edit(request, id):
  return render(request, "pages/patrimony-form.html", { 'title': 'Editar Item' })

def patrimony_detail(request, id):
  return render(request, "pages/patrimony-detail.html", {})

