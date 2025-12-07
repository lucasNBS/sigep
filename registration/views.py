from django.shortcuts import render

def records(request):
  return render(request, "pages/record.html", {})

def records_scan(request):
  return render(request, "pages/record-scan.html", {})
