from wagtail.models import Page
from django.db import models
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    intro = models.CharField(max_length=250, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
