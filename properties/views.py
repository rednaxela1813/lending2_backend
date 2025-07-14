from django.views.generic import ListView, DetailView
from .models import Property

class PropertyListView(ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    
    

class PropertyDetailView(DetailView):
    model = Property
    template_name = 'properties/property_detail.html'
    slug_field = 'public_id'
    slug_url_kwarg = 'public_id'
    context_object_name = 'property'
