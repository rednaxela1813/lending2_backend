from django import template
from django.utils.safestring import mark_safe
from apps.dashboard.models import EditableText, EditableImage, SiteSection, SiteSlot


register = template.Library()

def _lang(context):
    req = context.get('request')
    return getattr(req, 'LANGUAGE_CODE', 'sk') or 'sk'

def _get_slot(section_slug, slot_slug, kind=None):
    qs = SiteSlot.objects.select_related('section').filter(
        section__slug=section_slug, slug=slot_slug
    )
    if kind:
        qs = qs.filter(kind=kind)
    return qs.first()

# --- by key (как раньше) ---
@register.simple_tag(takes_context=True)
def content_text(context, key, default=''):
    lang = _lang(context)
    obj = (EditableText.objects
           .filter(key=key, language=lang, is_active=True)
           .order_by('-updated_at').first())
    return mark_safe(obj.text) if obj and obj.text else default

@register.simple_tag(takes_context=True)
def content_image_url(context, key, default=''):
    lang = _lang(context)
    obj = (EditableImage.objects
           .filter(key=key, language=lang, is_active=True)
           .order_by('-updated_at').first())
    return obj.image.url if obj and obj.image else default

@register.simple_tag(takes_context=True)
def content_title(context, key, default=''):
    lang = _lang(context)
    obj = (EditableText.objects
           .filter(key=key, language=lang, is_active=True)
           .order_by('-updated_at').first())
    return obj.title if obj and obj.title else default

# --- by section/slot (НОВОЕ) ---
@register.simple_tag(takes_context=True)
def slot_text(context, section_slug, slot_slug, default=''):
    lang = _lang(context)
    slot = _get_slot(section_slug, slot_slug, kind='text')
    if not slot:
        return default
    obj = (EditableText.objects
           .filter(slot=slot, language=lang, is_active=True)
           .order_by('-updated_at').first())
    if obj and obj.text:
        return mark_safe(obj.text)
    # fallback на key = section.slot
    return content_text(context, f'{section_slug}.{slot_slug}', default)

@register.simple_tag(takes_context=True)
def slot_title(context, section_slug, slot_slug, default=''):
    lang = _lang(context)
    slot = _get_slot(section_slug, slot_slug, kind='text')
    if not slot:
        return default
    obj = (EditableText.objects
           .filter(slot=slot, language=lang, is_active=True)
           .order_by('-updated_at').first())
    return obj.title if obj and obj.title else default

@register.simple_tag(takes_context=True)
def slot_image_url(context, section_slug, slot_slug, default=''):
    lang = _lang(context)
    slot = _get_slot(section_slug, slot_slug, kind='image')
    if not slot:
        return default
    obj = (EditableImage.objects
           .filter(slot=slot, language=lang, is_active=True)
           .order_by('-updated_at').first())
    if obj and obj.image:
        return obj.image.url
    # fallback на key = section.slot
    return content_image_url(context, f'{section_slug}.{slot_slug}', default)

@register.simple_tag(takes_context=True)
def slot_image_alt(context, section_slug, slot_slug, default=''):
    lang = _lang(context)
    slot = _get_slot(section_slug, slot_slug, kind='image')
    if not slot:
        return default
    obj = (EditableImage.objects
           .filter(slot=slot, language=lang, is_active=True)
           .order_by('-updated_at').first())
    return obj.alt if obj and obj.alt else default
