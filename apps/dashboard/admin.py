# from django.contrib import admin
# from django.utils.html import format_html
# from .models import SiteSection, SiteSlot, EditableText, EditableImage


# @admin.register(SiteSection)
# class SiteSectionAdmin(admin.ModelAdmin):
#     list_display = ('slug', 'name')
#     search_fields = ('slug','name')


# @admin.register(SiteSlot)
# class SiteSlotAdmin(admin.ModelAdmin):
#     list_display = ('section','slug','name','kind')
#     list_filter = ('section','kind')
#     search_fields = ('slug','name')
#     autocomplete_fields = ('section',)


# @admin.register(EditableText)
# class EditableTextAdmin(admin.ModelAdmin):
#     list_display = ('key','language','title','is_active','updated_at')
#     list_filter = ('language','is_active')
#     search_fields = ('key','title','text',)
#     #autocomplete_fields = ('slot',)


# @admin.register(EditableImage)
# class EditableImageAdmin(admin.ModelAdmin):
#     list_display = ("company", "is_active", "updated_at", "preview")
#     list_filter = ("company", "is_active")
#     search_fields = ( "caption", "alt")
#     autocomplete_fields = ("company",)
#     fields = ( "image", "alt", "caption", "is_active", "company", "updated_at", "preview")
#     readonly_fields = ("updated_at", "preview")

#     def preview(self, obj):
#         if obj.image and getattr(obj.image, "url", None):
#             return format_html(
#                 '<img src="{}" style="max-height:80px;border-radius:6px;box-shadow:0 0 4px #ccc;">',
#                 obj.image.url
#             )
#         return "(no image)"
#     preview.short_description = "Preview"
