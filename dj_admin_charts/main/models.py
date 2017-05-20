from django.db import models


class ChartModel(models.Model):
    # config will not be displayed as is
    config = models.TextField(blank=False, null=False, editable=False)
