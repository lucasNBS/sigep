from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from .models import Record

class ListRecordsView(ListView):
  model = Record
  template_name = "registration/record.html"
  context_object_name = "records"
  pk_url_kwarg = "institution_id"

  def get_paginate_by(self, queryset):
    page_size = self.request.GET.get("size")
    if page_size:
      return page_size
    return 10

  # def get_queryset(self):
  #   queryset = models.Inventory.objects.select_related(
  #     "institution", "responsible", "leader_consultor"
  #   ).prefetch_related("consultors")

  #   self.filterset = forms.InventoryFilter(self.request.GET, queryset=queryset)
  #   return self.filterset.qs.distinct()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["size"] = self.request.GET.get("size") if self.request.GET.get('size') else 10
    # context["institution"] = self.kwargs["institution_id"]
    #context["filter"] = self.filterset
    return context

def records_scan(request):
  return render(request, "pages/record-scan.html", {})
