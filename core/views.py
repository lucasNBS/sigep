from django.shortcuts import render

def home(request):
  return render(request, "pages/dashboard.html", {})

def reset_password2(request):
  return render(request, "pages/reset-password2.html", {})

def records(request):
  return render(request, "pages/record.html", {})

def records_scan(request):
  return render(request, "pages/record-scan.html", {})

def profile(request):
  return render(request, "pages/profile.html", {})
