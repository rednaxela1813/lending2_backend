# apps/dashboard/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core_images.mixins import ImageOptimizationMixin  # ⬅️ используем ваш миксин

LANG_CHOICES = [
    ('sk', 'Slovak'),
    ('en', 'English'),
    ('ru', 'Russian'),
]

def upload_to_images(instance, filename):
    return f'dashboard/{instance.key}/{filename}'

class EditableText(models.Model):
    key = models.SlugField(_('Key'), max_length=128, unique=True,
        help_text=_('Напр.: hero.title, footer.about, services.office.lead'))
    language = models.CharField(_('Language'), max_length=5, choices=LANG_CHOICES, default='sk')
    title = models.CharField(_('Title (optional)'), max_length=255, blank=True)
    text = models.TextField(_('Text / HTML'), blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Editable text')
        verbose_name_plural = _('Editable texts')

    def __str__(self):
        return f'{self.key} [{self.language}]'


class EditableImage(ImageOptimizationMixin, models.Model):   # ⬅️ миксин первым
    # какие поля оптимизировать:
    IMAGE_FIELDS = ("image",)                                # ⬅️ важно
    # опционально — дефолты оптимизации (можно не трогать)
    IMAGE_OPT_KWARGS = {
        "max_w": 1600,
        "max_h": 1200,
        "target_format": "WEBP",    # "WEBP"|"JPEG"; JPEG автоматически заменится на WEBP, если есть альфа-канал
        "quality": 80,
        "only_downscale": True,
        "keep_exif": False,
    }

    key = models.SlugField(
        _('Key'),
        max_length=128,
        unique=True,
        help_text=_('Напр.: hero.image, services.billboard.hero, about.gallery1')
    )
    language = models.CharField(_('Language'), max_length=5, choices=LANG_CHOICES, default='sk')
    image = models.ImageField(_('Image'), upload_to=upload_to_images)
    alt = models.CharField(_('Alt text'), max_length=255, blank=True)
    caption = models.CharField(_('Caption'), max_length=255, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Editable image')
        verbose_name_plural = _('Editable images')

    def __str__(self):
        return f'{self.key} [{self.language}]'
