from django.views.generic import ListView, DetailView
from .models import Property, OfficeUnit
from django.shortcuts import get_object_or_404, render
from django.views import View



class PropertyListView(ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    
    def get_queryset(self):
        return Property.objects.filter(type__slug='offices')


class PropertyDetailView(View):
    def get(self, request, public_id):
        property = get_object_or_404(Property, public_id=public_id)

        if property.type.slug == 'offices' and property.office_units.exists():
            # Показываем список помещений по этажам
            return render(request, 'properties/office_units_list.html', {
                'property': property,
                'office_units': property.office_units.all()
            })

        # Старое поведение
        return render(request, 'properties/property_detail.html', {
            'property': property
        })
        
        
class OfficeUnitDetailView(DetailView):
    model = OfficeUnit
    template_name = 'properties/office_unit_detail.html'
    context_object_name = 'unit'
    pk_url_kwarg = 'unit_id' 




# class HomePageView(TemplateView):
#     template_name = 'csm/index.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['services'] = Property.objects.filter(type__in=['office', 'address', 'billboard'])
#         return context

class AddressListView(ListView):
    model = Property
    template_name = 'properties/address_list.html'
    context_object_name = 'properties'

    def get_queryset(self):
        return Property.objects.filter(type__slug='address')
    
    
    
class BillboardListView(ListView):
    model = Property
    template_name = 'properties/billboard_list.html'
    context_object_name = 'properties'

    def get_queryset(self):
        return Property.objects.filter(type__slug='billboard')

