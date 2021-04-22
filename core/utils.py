import re
from django import template

class FormFieldNode(template.Node):
    """"
    Add the widget type to a BoundField. Until 3.1, Django did not make this available by default.
    Used by `oscar.templatetags.form_tags.annotate_form_field`
    """
    def __init__(self, field_str):
        self.field = template.Variable(field_str)

    def render(self, context):
        field = self.field.resolve(context)
        if not hasattr(field, 'widget_type') and hasattr(field, 'field'):
            field.widget_type = re.sub(r'widget$|input$', '', field.field.widget.__class__.__name__.lower())
        return ''