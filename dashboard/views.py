from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import EditableText, EditableImage
from .forms import EditableTextForm, EditableImageForm


class ContentManagerRequired(UserPassesTestMixin):
    def test_func(self):
        u = self.request.user
        return u.is_authenticated and (u.is_superuser or u.groups.filter(name="Content managers").exists())

class DashboardHome(LoginRequiredMixin, ContentManagerRequired, TemplateView):
    template_name = "dashboard/base/home.html"

# --- TEXTS ---
class TextList(LoginRequiredMixin, ContentManagerRequired, ListView):
    model = EditableText
    template_name = "dashboard/texts/list.html"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().order_by("key", "-updated_at")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(key__icontains=q) | Q(title__icontains=q) | Q(text__icontains=q))
        lang = self.request.GET.get("lang", "").strip()
        if lang:
            qs = qs.filter(language=lang)
        return qs

class TextCreate(LoginRequiredMixin, ContentManagerRequired, CreateView):
    model = EditableText
    form_class = EditableTextForm
    template_name = "dashboard/texts/form.html"
    success_url = reverse_lazy("dashboard:text_list")

class TextUpdate(LoginRequiredMixin, ContentManagerRequired, UpdateView):
    model = EditableText
    form_class = EditableTextForm
    template_name = "dashboard/texts/form.html"
    success_url = reverse_lazy("dashboard:text_list")

class TextDelete(LoginRequiredMixin, ContentManagerRequired, DeleteView):
    model = EditableText
    template_name = "dashboard/common/confirm_delete.html"
    success_url = reverse_lazy("dashboard:text_list")

# --- IMAGES ---
class ImageList(LoginRequiredMixin, ContentManagerRequired, ListView):
    model = EditableImage
    template_name = "dashboard/images/list.html"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().order_by("key", "-updated_at")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(key__icontains=q) | Q(alt__icontains=q) | Q(caption__icontains=q))
        lang = self.request.GET.get("lang", "").strip()
        if lang:
            qs = qs.filter(language=lang)
        return qs

class ImageCreate(LoginRequiredMixin, ContentManagerRequired, CreateView):
    model = EditableImage
    form_class = EditableImageForm
    template_name = "dashboard/images/form.html"
    success_url = reverse_lazy("dashboard:image_list")

class ImageUpdate(LoginRequiredMixin, ContentManagerRequired, UpdateView):
    model = EditableImage
    form_class = EditableImageForm
    template_name = "dashboard/images/form.html"
    success_url = reverse_lazy("dashboard:image_list")

class ImageDelete(LoginRequiredMixin, ContentManagerRequired, DeleteView):
    model = EditableImage
    template_name = "dashboard/common/confirm_delete.html"
    success_url = reverse_lazy("dashboard:image_list")
