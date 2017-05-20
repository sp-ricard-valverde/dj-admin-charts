import six
from django import forms
from django.core.exceptions import ValidationError
from django.template.defaultfilters import striptags

from .widgets import ColorWidget, FormFieldWidget


class ColorField(forms.CharField):
    widget = ColorWidget

    def __init__(self, *args, **kwargs):
        super(ColorField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super(ColorField, self).widget_attrs(widget)
        attrs.update(widget.attrs)

        if not 'options' in attrs:
            attrs['options'] = {}
        color = attrs['options'][
            'color'] if 'color' in attrs['options'] else self.initial

        attrs['options']['color'] = color or "#f00"

        return attrs


class FormField(forms.MultiValueField):
    """The form field we can use in forms"""

    def __init__(self, form, **kwargs):
        import inspect
        if inspect.isclass(form) and issubclass(form, forms.Form):
            form_class = form
        elif callable(form):
            form_class = form()
            self.form = form_class()
        elif isinstance(form, six.string_types):
            from django.utils import module_loading
            form_class = module_loading.import_by_path(form)
        self.form = form_class()

        # Set the widget and initial data
        kwargs['widget'] = FormFieldWidget([f for f in self.form])
        kwargs['initial'] = [f.field.initial for f in self.form]

        self.max_length = kwargs.pop('max_length', None)

        super(FormField, self).__init__(**kwargs)

        self.fields = [f.field for f in self.form]

    def compress(self, data_list):
        """
        Return the cleaned_data of the form, everything should already be valid
        """
        data = {}
        if data_list:
            data = dict(
                (f.name, data_list[i]) for i, f in enumerate(self.form))

            f = self.form.__class__(data)
            f.is_valid()
            return f.cleaned_data
        return data

    def clean(self, value):
        """
        Call the form is_valid to ensure every value supplied is valid
        """
        if not value:
            raise ValidationError(
                'Error found in Form Field: Nothing to validate')

        data = dict((bf.name, value[i]) for i, bf in enumerate(self.form))
        self.form = form = self.form.__class__(data)
        if not form.is_valid():
            error_dict = list(form.errors.items())
            errors = striptags(
                ", ".join(["%s (%s)" % (v, k) for k, v in error_dict]))
            raise ValidationError('Error(s) found: %s' % errors)

        # This call will ensure compress is called as expected.
        return super(FormField, self).clean(value)
