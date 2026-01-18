from institution import models
from item.models import Item

def handle_selected_element(model, element_id, element_name):
  if (element_id):
    element = model.objects.get(id=element_id)
    element.name = element_name
    element.save(update_fields=["name"])
    element.refresh_from_db()
  else:
    element = model(name=element_name, institution=models.Institution.objects.get(id=1))
    element.full_clean()
    element.save()
  return element


def validate_dataframe_column(df, column):
  errors = []
  if df[column].isna().any():
      for line in df[df[column].isna()].index.tolist():
        errors.append(f"Linha {line + 2}: {column} é um campo obrigatório")
  else:
    for line, item in df[column].items():
      if column == "Serial":
        institution = models.Institution.objects.get(id=1)
        if Item.objects.filter(serial=item, institution=institution).exists():
          errors.append(f"Linha {line + 2}: Já existe um item com este Serial")
      if column == "Nota Fiscal":
        institution = models.Institution.objects.get(id=1)
        if Item.objects.filter(invoice_key=item, institution=institution).exists():
          errors.append(f"Linha {line + 2}: Já existe um item com esta Nota Fiscal")
  return errors
