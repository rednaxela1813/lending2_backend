# apps/dashboard/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core_images.mixins import ImageOptimizationMixin
from apps.company.models import CompanyInfo
from django.db.models import Q


LANG_CHOICES = [('sk','Slovak'),('en','English'),('ru','Russian')]

class SiteSection(models.Model):
    slug = models.SlugField(_('Section slug'), max_length=64, unique=True,
                            help_text=_('napr.: home, services, footer'))
    name = models.CharField(_('Name'), max_length=128)

    class Meta:
        verbose_name = _('Site section')
        verbose_name_plural = _('Site sections')

    def __str__(self):
        return f'{self.slug} — {self.name}'


class SiteSlot(models.Model):
    TEXT = 'text'
    IMAGE = 'image'
    CONTENT_KIND_CHOICES = [(TEXT, 'Text'), (IMAGE, 'Image')]

    section = models.ForeignKey(SiteSection, on_delete=models.CASCADE, related_name='slots')
    slug = models.SlugField(_('Slot slug'), max_length=64,
                            help_text=_('napr.: hero_title, hero_lead, hero_image'))
    name = models.CharField(_('Name'), max_length=128)
    kind = models.CharField(_('Content kind'), max_length=16, choices=CONTENT_KIND_CHOICES)

    class Meta:
        unique_together = [('section', 'slug')]
        verbose_name = _('Site slot')
        verbose_name_plural = _('Site slots')

    def __str__(self):
        return f'{self.section.slug}.{self.slug} ({self.kind})'

    @property
    def full_key(self) -> str:
        return f'{self.section.slug}.{self.slug}'


def upload_to_images(instance, filename):
    # хранение по секции/слоту удобно для навигации в media
    path = instance.slot.full_key if instance.slot_id else (instance.key or 'dashboard')
    return f'dashboard/{path}/{filename}'


class EditableText(models.Model):
    # НОВОЕ: можно выбрать слот (приоритетнее ключа)
    slot = models.ForeignKey(SiteSlot, null=True, blank=True, on_delete=models.SET_NULL,
                             limit_choices_to={'kind': SiteSlot.TEXT}, related_name='texts')
    key = models.SlugField(_('Key'), max_length=128, blank=True, 
        help_text=_('Автогенерируется из секции/слота, если выбран слот.'))
    language = models.CharField(_('Language'), max_length=5, choices=LANG_CHOICES, default='sk')
    title = models.CharField(_('Title (optional)'), max_length=255, blank=True)
    text = models.TextField(_('Text / HTML'), blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(CompanyInfo, null=True, blank=True, on_delete=models.CASCADE, related_name="editable_texts")

    class Meta:
        constraints = [
            # 1) Один и тот же key разрешён в разных компаниях
            models.UniqueConstraint(
                fields=["key", "company"],
                name="uniq_editabletext_key_company",
            ),
            # 2) Но «глобальный» (company IS NULL) должен быть единственным на key
            models.UniqueConstraint(
                fields=["key"],
                condition=Q(company__isnull=True),
                name="uniq_editabletext_key_global",
            ),
        ]

    def __str__(self):
        return self.key or (self.slot.full_key if self.slot_id else '(no key)')

    def save(self, *args, **kwargs):
        if self.slot_id and not self.key:
            self.key = self.slot.full_key
        super().save(*args, **kwargs)


class EditableImage(ImageOptimizationMixin, models.Model):
    key = models.CharField(max_length=255)
    image = models.ImageField(upload_to="editable_images/", blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True)
    alt = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(
        CompanyInfo, null=True, blank=True,
        on_delete=models.CASCADE, related_name="editable_images"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["key", "company"],
                name="uniq_editableimage_key_company",
            ),
            models.UniqueConstraint(
            fields=["key"],
            condition=Q(company__isnull=True),
            name="uniq_editableimage_key_global",
        ),
    ]
    IMAGE_FIELDS = ("image",)

    def __str__(self):
        return f"{self.key} ({self.company or 'global'})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
