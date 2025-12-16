from django.shortcuts import render

def institution(request):
  return render(request, "pages/panel.html", {})
