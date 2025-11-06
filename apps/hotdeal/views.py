# apps/hotdeal/views.py
from django.views.generic import DetailView
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from .models import HotDealItem



def hotdeal_partial(request, public_id):
    deal = get_object_or_404(
        HotDealItem.objects.select_related("property", "section", "property__type"),
        public_id=public_id
    )
    prop = deal.property
    prop_images = prop.images.all() if prop else []
    return render(request, "hotdeal/detail_partial.html", {
        "deal": deal,
        "prop_images": prop_images,
    })
    
    

class HotDealDetailView(DetailView):
    model = HotDealItem
    template_name = "hotdeal/detail.html"        
    context_object_name = "deal"                 

    # ← 3. указываем поле и имя параметра из URL
    slug_field = "public_id"
    slug_url_kwarg = "public_id"

    def get_queryset(self):
        today = timezone.localdate()
        return (
            HotDealItem.objects
            .select_related("property", "section", "property__type")
            .filter(
                is_active=True,                                        
                # section__is_active=True,                             
            )
            .filter(Q(date_expiry__isnull=True) | Q(date_expiry__gte=today))  
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        deal = ctx["deal"]

        # ← 5. срок действия в днях (если указан)
        today = timezone.localdate()
        ctx["expires_in_days"] = (
            (deal.date_expiry - today).days if deal.date_expiry else None
        )

        # ← 6. картинки связанного объекта (если есть related_name=images)
        images_manager = getattr(getattr(deal, "property", None), "images", None)
        ctx["prop_images"] = list(images_manager.all()) if images_manager else []

        return ctx
