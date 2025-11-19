from django.shortcuts import render

def home(request):
  return render(request, "pages/dashboard.html", {})

def institution(request):
  return render(request, "pages/panel.html", {})

def login(request):
  return render(request, "pages/signin.html", {})

def signup(request):
  return render(request, "pages/signup.html", {})

def forgot_password(request):
  return render(request, "pages/forgot-password.html")

def reset_password(request):
  return render(request, "pages/reset-password.html")

def reset_password2(request):
  return render(request, "pages/reset-password2.html", {})

def new_password(request):
  return render(request, "pages/new-password.html", {})

def patrimony_form(request):
  return render(request, "pages/patrimony-form.html", {})

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

def user(request):
  return render(request, "pages/user.html", {})

def user_detail(request, id):
  return render(request, "pages/user-detail.html", {})

def patrimony(request):
  return render(request, "pages/patrimony.html", {})

def profile(request):
  return render(request, "pages/profile.html", {})
