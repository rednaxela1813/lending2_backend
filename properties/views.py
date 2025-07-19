from django.views.generic import ListView, DetailView
from .models import Property
#from django.views.generic.base import TemplateView


class PropertyListView(ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    
    def get_queryset(self):
        return Property.objects.filter(type='office')
    
    

class PropertyDetailView(DetailView):
    model = Property
    template_name = 'properties/property_detail.html'
    slug_field = 'public_id'
    slug_url_kwarg = 'public_id'
    context_object_name = 'property'
    


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
        return Property.objects.filter(type='address')
    
    
    
class BillboardListView(ListView):
    model = Property
    template_name = 'properties/billboard_list.html'
    context_object_name = 'properties'

    def get_queryset(self):
        return Property.objects.filter(type='billboard')

