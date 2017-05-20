from django import template

register = template.Library()


@register.simple_tag
def map_fields(fieldset):
    class FieldLineContainer:
        pass

    flc = FieldLineContainer()
    for fieldline in fieldset:
        field = next(iter(fieldline))
        setattr(flc, field.field.name, fieldline)
    return flc
