from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import EditableText, EditableImage
from .forms import EditableTextForm, EditableImageForm



class DashboardHome(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/base/home.html"

# --- TEXTS ---
class TextList(LoginRequiredMixin, ListView):
    model = EditableText
    template_name = "dashboard/texts/list.html"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().order_by("key", "-updated_at")
        company = getattr(self.request, "company", None)
        if hasattr(self.model, "company") and company is not None:
            qs = qs.filter(Q(company=company) | Q(company__isnull=True))
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(key__icontains=q) | Q(title__icontains=q) | Q(text__icontains=q))
        lang = self.request.GET.get("lang", "").strip()
        if lang:
            qs = qs.filter(language=lang)
        return qs

class TextCreate(LoginRequiredMixin, CreateView):
    model = EditableText
    form_class = EditableTextForm
    template_name = "dashboard/texts/form.html"
    success_url = reverse_lazy("dashboard:text_list")

    def form_valid(self, form):
        company = getattr(self.request, "company", None)
        if company and getattr(form.instance, "company_id", None) is None:
            form.instance.company = company
        return super().form_valid(form)

class TextUpdate(LoginRequiredMixin, UpdateView):
    model = EditableText
    form_class = EditableTextForm
    template_name = "dashboard/texts/form.html"
    success_url = reverse_lazy("dashboard:text_list")

class TextDelete(LoginRequiredMixin, DeleteView):
    model = EditableText
    template_name = "dashboard/common/confirm_delete.html"
    success_url = reverse_lazy("dashboard:text_list")

# --- IMAGES ---
class ImageList(LoginRequiredMixin, ListView):
    model = EditableImage
    template_name = "dashboard/images/list.html"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().order_by("key", "-updated_at")
        company = getattr(self.request, "company", None)
        if hasattr(self.model, "company") and company is not None:
            qs = qs.filter(Q(company=company) | Q(company__isnull=True))
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(key__icontains=q) | Q(alt__icontains=q) | Q(caption__icontains=q))
        lang = self.request.GET.get("lang", "").strip()
        if lang:
            qs = qs.filter(language=lang)
        return qs

class ImageCreate(LoginRequiredMixin, CreateView):
    model = EditableImage
    form_class = EditableImageForm
    template_name = "dashboard/images/form.html"
    success_url = reverse_lazy("dashboard:image_list")

    def form_valid(self, form):
        company = getattr(self.request, "company", None)
        if company and getattr(form.instance, "company_id", None) is None:
            form.instance.company = company
        return super().form_valid(form)

class ImageUpdate(LoginRequiredMixin, UpdateView):
    model = EditableImage
    form_class = EditableImageForm
    template_name = "dashboard/images/form.html"
    success_url = reverse_lazy("dashboard:image_list")

class ImageDelete(LoginRequiredMixin, DeleteView):
    model = EditableImage
    template_name = "dashboard/common/confirm_delete.html"
    success_url = reverse_lazy("dashboard:image_list")
