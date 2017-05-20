from django.contrib.admin import ModelAdmin

from .forms import ChartModelForm, FormField, MutableDatasetForm
from .models import ChartModel
from .. import admin


class ChartModelAdmin(ModelAdmin):
    change_form_template = 'admin/chart_change_form.html'
    form = ChartModelForm

    def get_fields(self, request, obj=None):
        gf = super(ChartModelAdmin, self).get_fields(request, obj)
        new_dynamic_fields = [('dataset_form', FormField(
            form=MutableDatasetForm, label="Dataset Form"))]
        for f in new_dynamic_fields:
            gf = gf + [f[0]]
            self.form.declared_fields.update({f[0]: f[1]})
        return gf


admin.admin_site.register(ChartModel, ChartModelAdmin)
