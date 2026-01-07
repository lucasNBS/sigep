from django import forms

class InputField(forms.TextInput):
  template_name = "widgets/input.html"

  def __init__(self, label, type,input_class, label_class, placeholder = '', **kwargs):
    super().__init__(**kwargs)
    self.label = label
    self.type = type
    self.placeholder = placeholder
    self.input_class = input_class
    self.label_class = label_class

  def get_context(self, name, value, attrs):
    context = super().get_context(name, value, attrs)
    context["widget"]["label"] = self.label
    context["widget"]["type"] = self.type
    context["widget"]["placeholder"] = self.placeholder
    context["widget"]["label_class"] = self.label_class
    context["widget"]["input_class"] = self.input_class
    context["widget"]["value"] = '' if value is None else value
    return context
  
class Textarea(forms.Textarea):
  template_name = "widgets/textarea.html"

  def __init__(self, label, input_class, label_class, placeholder, **kwargs):
    super().__init__(**kwargs)
    self.label = label
    self.placeholder = placeholder
    self.input_class = input_class
    self.label_class = label_class

  def get_context(self, name, value, attrs):
    context = super().get_context(name, value, attrs)
    context["widget"]["label"] = self.label
    context["widget"]["placeholder"] = self.placeholder
    context["widget"]["label_class"] = self.label_class
    context["widget"]["input_class"] = self.input_class
    context["widget"]["value"] = '' if value is None else value
    return context
  
class Autocomplete(forms.Select):
  template_name = "widgets/autocomplete.html"

  def __init__(self, label, autocomplete, input_class, label_class, editable = False, value='', **kwargs ):
    super().__init__(**kwargs)
    self.label = label
    self.value = value
    self.autocomplete = autocomplete
    self.editable = editable
    self.input_class = input_class
    self.label_class = label_class


  def get_context(self, name, value, attrs):
    context = super().get_context(name, value, attrs)
    context["widget"]["label"] = self.label
    context["widget"]["value"] = self.value
    context["widget"]["autocomplete"] = self.autocomplete
    context["widget"]["editable"] = self.editable
    context["widget"]["label_class"] = self.label_class
    context["widget"]["input_class"] = self.input_class
    return context

class Select(forms.Select):
  template_name = "widgets/select.html"

  def __init__(self, label, input_class, label_class, **kwargs):
    super().__init__(**kwargs)
    self.label = label
    self.input_class = input_class
    self.label_class = label_class
  
  def get_context(self, name, value, attrs):
    context = super().get_context(name, value, attrs)
    context["widget"]["label"] = self.label
    context["widget"]["label_class"] = self.label_class
    context["widget"]["input_class"] = self.input_class
    return context