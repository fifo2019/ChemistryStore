from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse


@login_required
def basket(request):
    title = 'Корзина'
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

    content = {
        'title': title,
        'basket_items': basket_items,
        'basket': basket_items,
    }

    return render(request, 'basketapp/basket.html', content)


@login_required
def basket_add(request, pk, quantity, *args, **kwargs):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))

    try:
        if request.is_ajax():
            quantity = int(quantity)
            product = get_object_or_404(Product, pk=pk)
            old_basket_item = Basket.objects.filter(user=request.user, product=product)

            if old_basket_item:
                old_basket_item[0].quantity += quantity
                old_basket_item[0].save()
            else:
                new_basket_item = Basket(user=request.user, product=product)
                new_basket_item.quantity += quantity
                new_basket_item.save()

            products = Product.objects.filter(category__name='Новинки')
            basket = []
            basket = Basket.objects.filter(user=request.user)

            content = {
                'basket': basket,
            }

            result = render_to_string('mainapp/includes/inc_sing_in.html', content)
            return JsonResponse({'result': result})

    except ValueError:

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)

    if request.method == 'POST':
        basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    try:
        if request.is_ajax():
            quantity = int(quantity)
            new_basket_item = Basket.objects.get(pk=int(pk))

            if quantity > 0:
                new_basket_item.quantity = quantity
                new_basket_item.save()
            else:
                new_basket_item.delete()

            basket = Basket.objects.filter(user=request.user).order_by('product__category')

            content = {
                'basket': basket,
            }

            result = render_to_string('basketapp/includes/inc_basket_list.html', content)

            return JsonResponse({'result': result})

    except ValueError:

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))