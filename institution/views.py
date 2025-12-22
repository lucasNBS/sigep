from django.http import JsonResponse
from django.shortcuts import render

from . import models

def institution(request):
  return render(request, "pages/panel.html", {})

def autocomplete_categories_view(request):
  search = request.GET.get("search")
  limit = 20

  found_categories = models.Category.objects.filter(name__icontains=search)

  response = [
    {"name": categorie.name, "id": categorie.id} for categorie in found_categories
  ][:limit]

  return JsonResponse(response, safe=False)
