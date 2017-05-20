import six
from django.forms import widgets
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class ColorWidget(widgets.Widget):

    class Media:
        js = ('js/spectrum.js',)
        css = {
            'all': ('css/spectrum.css',)
        }

    def render(self, name, value, attrs=None):
        extended_attrs = {}
        extended_attrs.update(attrs)

        if not 'options' in extended_attrs:
            extended_attrs['options'] = {}
        if self.attrs and 'options' in self.attrs:
            for k, v in self.attrs['options'].items():
                if isinstance(v, six.string_types):
                    extended_attrs['options'][k] = mark_safe('"' + v + '"')
                elif isinstance(v, bool):
                    extended_attrs['options'][k] = mark_safe(str(v).lower())
                else:
                    extended_attrs['options'][k] = mark_safe(v)

        return render_to_string('chart/colorfield.html', {'attrs': extended_attrs, 'name': name, 'value': value})


class FormFieldWidget(widgets.MultiWidget):
    """
    This widget will render each field found in the supplied form.
    """

    def __init__(self, fields, attrs=None):
        self.fields = fields
        # Retreive each field widget for the form
        widgets = [f.field.widget for f in self.fields]

        super(FormFieldWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        """
        Retrieve each field value or provide the initial values
        """
        if value:
            return [value.get(field.name, None) for field in self.fields]
        return [field.field.initial for field in self.fields]

    def format_label(self, field, counter):
        """
        Format the label for each field
        """
        return '<label for="id_formfield_%s" %s>%s</label>' % (
            counter, field.field.required and 'class="required"', field.label)

    def format_help_text(self, field, counter):
        """
        Format the help text for the bound field
        """
        return '<p class="help">%s</p>' % field.help_text

    def format_output(self, rendered_widgets):
        """
        This output will yeild all widgets grouped in a un-ordered list
        """
        ret = [u'<ul class="formfield">']
        for i, field in enumerate(self.fields):
            label = self.format_label(field, i)
            help_text = self.format_help_text(field, i)
            ret.append(u'<li>%s %s %s</li>' % (
                label, rendered_widgets[i], field.help_text and help_text))

        ret.append(u'</ul>')
        return ''.join(ret)
