from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404

# Create your views here.


from .models import Product


class ProductDetailView(DetailView):
    model = Product
    # template_name = '<appname>/<modelname>_detail.html'


class ProductListView(ListView):
    model = Product
    # queryset = Product.objects.filter(active=False)

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        print context
        return context

# def product_detail_view_func(request, id):
#     # product_instance = Product.objects.get(id=id)
#     product_instance = get_object_or_404(Product, id=id)
#     template = 'products/product_detail.html'
#     context = {
#         'object': product_instance,
#     }
#     return render(request, template, context)

