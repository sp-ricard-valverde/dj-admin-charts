from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.contrib import admin
from django.conf.urls import url
# from .trabu.charts import DynamicAdminChart
# from .trabu.models import AdminChart


class CustomAdminSite(admin.AdminSite):

    @never_cache
    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        # extra_context['admin_charts'] = AdminChart.objects.all().order_by('-id', '-project')

        return super().index(request, extra_context)

    @never_cache
    def chart(self, request, adminchart_id):

        context = dict(
            self.each_context(request),
            # admin_chart=DynamicAdminChart(int(adminchart_id))
        )

        request.current_app = self.name

        return TemplateResponse(request, 'admin/chart.html', context)

    def get_urls(self):
        urlpatters = super().get_urls()
        urlpatters += [
            url(r'^chart/(?P<adminchart_id>[0-9]+)/$',
                self.chart, name='chart')
        ]
        return urlpatters


admin_site = CustomAdminSite(name='custom_admin')
admin.site = admin_site
admin.autodiscover()
