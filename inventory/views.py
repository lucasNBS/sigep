from django.http import JsonResponse
from django.shortcuts import render

from . import models

def inventory_form(request):
  return render(request, "pages/inventory-form.html", {})

def inventory(request):
  return render(request, "pages/inventory.html", {})

def inventory_detail(request, id):
  return render(request, "pages/inventory-detail.html", {})

def autocomplete_rooms_view(request):
  search = request.GET.get("search")
  limit = 20

  found_rooms = models.Room.objects.filter(name__icontains=search)

  response = [
    {"name": room.name, "id": room.id} for room in found_rooms
  ][:limit]

  return JsonResponse(response, safe=False)
