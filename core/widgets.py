from django import forms

class InputField(forms.TextInput):
  template_name = "widgets/input.html"

  def __init__(self, label, type, placeholder = '', **kwargs):
    super().__init__(**kwargs)
    self.label = label
    self.type = type
    self.placeholder = placeholder

  def get_context(self, name, value, attrs):
    context = super().get_context(name, value, attrs)
    context["widget"]["label"] = self.label
    context["widget"]["type"] = self.type
    context["widget"]["placeholder"] = self.placeholder
    context["widget"]["value"] = '' if value is None else value
    return context
  
class Textarea(forms.Textarea):
  template_name = "widgets/textarea.html"

  def __init__(self, label, placeholder, **kwargs):
    super().__init__(**kwargs)
    self.label = label
    self.placeholder = placeholder

  def get_context(self, name, value, attrs):
    context = super().get_context(name, value, attrs)
    context["widget"]["label"] = self.label
    context["widget"]["placeholder"] = self.placeholder
    context["widget"]["value"] = '' if value is None else value
    return context
  
class Autocomplete(forms.Select):
  template_name = "widgets/autocomplete.html"

  def __init__(self, label, autocomplete, editable = False, value='', **kwargs):
    super().__init__(**kwargs)
    self.label = label
    self.value = value
    self.autocomplete = autocomplete
    self.editable = editable

  def get_context(self, name, value, attrs):
    context = super().get_context(name, value, attrs)
    context["widget"]["label"] = self.label
    context["widget"]["value"] = self.value
    context["widget"]["autocomplete"] = self.autocomplete
    context["widget"]["editable"] = self.editable
    return context

class Select(forms.Select):
  template_name = "widgets/select.html"

  def __init__(self, label, **kwargs):
    super().__init__(**kwargs)
    self.label = label
  
  def get_context(self, name, value, attrs):
    context = super().get_context(name, value, attrs)
    context["widget"]["label"] = self.label
    return context
