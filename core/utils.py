from institution import models
from item.models import Item

def handle_selected_element(model, element_id, element_name, institution_id):
  if (element_id):
    element = model.objects.get(id=element_id)
    element.name = element_name
    element.save(update_fields=["name"])
    element.refresh_from_db()
  else:
    element = model(
      name=element_name, institution=models.Institution.objects.get(id=institution_id)
    )
    element.full_clean()
    element.save()
  return element


def validate_serial(item, line, errors):
  institution = models.Institution.objects.get(id=1)
  if Item.objects.filter(serial=item, institution=institution).exists():
    errors.append(f"Linha {line + 2}: Já existe um item com este Serial")

def validate_invoice_key(item, line, errors):
  institution = models.Institution.objects.get(id=1)
  if Item.objects.filter(invoice_key=item, institution=institution).exists():
    errors.append(f"Linha {line + 2}: Já existe um item com esta Nota Fiscal")

COLUMN_VALIDATORS = {
  "Serial": validate_serial,
  "Nota Fiscal": validate_invoice_key,
}

def validate_dataframe_column(df, column):
  errors = []
  if df[column].isna().any():
      for line in df[df[column].isna()].index.tolist():
        errors.append(f"Linha {line + 2}: {column} é um campo obrigatório")
  else:
    for line, item in df[column].items():
      validate = COLUMN_VALIDATORS.get(column)
      if validate is not None:
        validate(item, line, errors)
  return errors
