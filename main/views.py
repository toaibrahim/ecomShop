
from unicodedata import category
from django.conf import settings
from django.shortcuts import redirect, render,get_object_or_404
from requests import request
from .models import *
from django.views.generic import ListView,DetailView,View
from django.utils import timezone
from django.contrib import messages
from django.db.models import Count,Q
from marketing.forms import NewletterAdd
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm,BillingIt,ProductReview
import stripe
from django.http import JsonResponse



# Create your views here.

class HomeView(ListView):
    model = Item
    template_name = "main/index.html"
    context_object_name = 'product'

    def get_queryset(self):
        queryset = {'featured': Item.objects.filter(featured=True), 
                    'recent': Item.objects.all().order_by('-time')[:5],
                    'blog_1': BlogPost.objects.all().order_by('-time')[:2],
                    'blog_2': BlogPost.objects.all().order_by('-time')[0:1],
                    'blog_3': BlogPost.objects.all().order_by('-time')[1:3],
                    'blog_4': BlogPost.objects.all().order_by('-time')[3:5],
                    'blog_5': BlogPost.objects.all().order_by('-time')[5:6],
                    'form':NewletterAdd()
                    }
        return queryset
    


class ProducDetailstView(DetailView):
    model = Item
    template_name = "main/product_details.html"
    context_object_name = "imageGallery"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_gallery'] = ImageGallery.objects.filter(product=self.object.id)
        context['cart_item'] = OrderItem.objects.filter(item = self.object.id)
        context['related_product'] = Item.objects.filter(category=self.object.category)
        context['all_product'] = Item.objects.all().order_by('-time')[:6]
        return context
    


def product_details(request,slug):
    object = Item.objects.get(slug = slug)
    gallerys = ImageGallery.objects.filter(product = object)
    related = Item.objects.filter(category=object.category)
    cart_item = OrderItem.objects.filter(item=object.id)

    if request.method == "POST":
        form = ProductReview(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.product = object
            form.save()
            messages.success(request,"You comment have been posted successfully")
            def get_absolute_url(self):
                return reverse("main:product_details",kwargs={
                    'slug':self.slug
                })
    else:
        form = ProductReview()
        def get_absolute_url(self):
            return reverse("main:product_details",kwargs={
                'slug':self.slug
            })
    
    return render(request,"main/product_details.html",{
        'object':object,
        'gallerys':gallerys,
        'related':related,
        'reviewForm':form,
        'cart_item':cart_item
    })


    




class Products(ListView):
    model = Item
    template_name = "main/product.html"
    paginate_by = 9
    context_object_name = 'orderitem'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orderitem'] = OrderItem.objects.filter(ordered=False)
        context['recent'] = Item.objects.all().order_by('-time')
        
        #context['image_gallery'] = ImageGallery.objects.filter(product=self.object.id)
        #context['cart_item'] = OrderItem.objects.filter(item = self.object.id)
        #context['related_product'] = Item.objects.filter(category=self.object.category)
        #context['all_product'] = Item.objects.all().order_by('-time')[:6]
        return context

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)



class OrderSummery(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'main/cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have any Item on your cart")
            return redirect("/")





def cart(request):
    cartItems = OrderItem.objects.filter(user=request.user,ordered=False)
    finalCart = Order.objects.filter(user=request.user,ordered=False)
    return render(request,"main/cart.html",{
        'cartItems':cartItems,
        'finalCart':finalCart
    })

@login_required(login_url="account:login")
def add_to_cart(request, slug):
  

    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("main:product_details",slug=slug)
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("main:product_details",slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("main:product_details",slug=slug)

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("main:cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("main:cart")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("main:cart")



def remove_from_cart_totally(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("main:cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("main:cart")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("main:cart")




class CheckoutView(View):
    def get(self,request,*args,**kwargs):
        form = CheckoutForm()
        order = Order.objects.filter(user=self.request.user,ordered = False).first()
        context = {
            'form':form,
            "order":order
        }
        return render(self.request,'main/checkout.html',context)

    def post(self,request, *args,**kwargs):
        form = CheckoutForm(request.POST)
        
        
        try:
            order = Order.objects.filter(user=self.request.user,ordered = False).first()
            
            if form.is_valid():
                user = request.user
                fname = form.cleaned_data.get('fname')
                lname = form.cleaned_data.get('lname')
                email = form.cleaned_data.get('email')
                mobile = form.cleaned_data.get('mobile')
                address = form.cleaned_data.get('address')
                country = form.cleaned_data.get('country')
                state = form.cleaned_data.get('state')
                zipcode = form.cleaned_data.get('zipcode')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user = user,
                    fname = fname,
                    lname = lname,
                    email = email,
                    mobile = mobile,
                    address = address,
                    country = country,
                    state = state,
                    zipcode = zipcode,
                    payment_option = payment_option,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.ordered = True
                order.save()
                
                #TODO : add redirect to the selected payment options
                messages.success(self.request,"Checkout successfully")
                return redirect("main:checkout")
            else:
                messages.warning(self.request,"Checkout Failed")
            context = {
                'form':form
            }
            return render(self.request,'main/checkout.html',context)
        except ObjectDoesNotExist:
            messages.error(request,"You don't have any active order")
            return redirect("main:cart")
        
class PaymentView(View):

    def get(self,request, *args,**kwargs):
        
        return render(self.request,"main/payment.html")

    def post(self,*args,**kwargs):
        
        return render(self.request,"main/payment.html")      
        





def wishlist(request):
    wishlist = WishlistItem.objects.filter(user=request.user)
    return render(request,"main/wishlist.html",{
        'wishlist':wishlist
    })

@login_required(login_url="account:login")
def add_to_wishlist(request,slug):
    item = get_object_or_404(Item,slug=slug)
    wishlist_item,create = WishlistItem.objects.get_or_create(
        item = item,
        user=request.user,
        wishlist = False
    )
    wishlisted_qs = Wishlisted.objects.filter(user=request.user)
    if wishlisted_qs.exists():
        wishlisted = wishlisted_qs[0]

        if wishlisted.items.filter(item__slug=item.slug).exists():
            messages.info(request,"You already have this item on your wishlist")
            return redirect("main:product_details",slug=slug)
        else:
            wishlisted.items.add(wishlist_item)
            messages.info(request,"This item was added to your wishlist")
            return redirect("main:product_details",slug=slug)
    else:
        wishlisted = Wishlisted.objects.create(user=request.user)
        wishlisted.items.add(wishlist_item)
        messages.info(request,"This item was added to your wishlist")
        return redirect("main:product_deatils",slug=slug)

def remove_from_wishlist(request,slug):

    item = get_object_or_404(Item,slug=slug)
    
    wishlisted_qs = Wishlisted.objects.filter(user=request.user)
    if wishlisted_qs.exists():
        wishlisted = wishlisted_qs[0]

        if wishlisted.items.filter(item__slug=item.slug).exists():
            wishlist_item = WishlistItem.objects.filter(item = item,user=request.user,wishlist=False).first()
            wishlisted.items.remove(wishlist_item)
            wishlist_item.delete()
            messages.info(request,"This item is deleted from your wishlist")
            return redirect("main:wishlist")
        else:
            
            messages.info(request,"You don't have this item on your wishlist to be removed")
            return redirect("main:wishlist")
    else:
        
        messages.info(request,"This item was not added to the wishlist")
        return redirect("main:wishlist")


def contact(request):
    return render(request,"main/contact.html")

def search(request):
    recent = Item.objects.all().order_by('-time')[:5]
    if request.method == "POST":
        queryset = Item.objects.all()
        searched = request.POST['search']
        if searched:
            queryset = queryset.filter(
                Q(title__icontains = searched) | Q(description__icontains = searched) | Q(category__icontains = searched)
            ).distinct()
    
    return render(request,"main/search_result.html",{
        'queryset':queryset,
        'recent':recent,
        'searched':searched
    })


class Blogpost(ListView):
    model = BlogPost
    template_name = "main/blog.html"
    paginate_by = 9
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = BlogPost.objects.all().order_by('-time')
        context['aside'] = BlogPost.objects.all().order_by('-time')[0:6]

        return context

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)


def blog_details(request,id):
    blog = BlogPost.objects.get(id = id)
    
    return render(request,"main/blog-detail.html",{
        'blog':blog,
    })

def my_account(request):
    address = BillingAddress.objects.filter(user = request.user).first()
    orders = Order.objects.filter(user=request.user,ordered=True)
    addressForm = BillingIt(request.POST or None,request.FILES or None,instance = address)

    if request.method == "POST":
       if addressForm.is_valid():
           addressForm.instance.user = request.user
           addressForm.save()
           messages.success(request,"Your address have been updated successfully!")
           return redirect("main:my_account")
    context = {
        'address':address,
        'orders':orders,
        'addressForm':addressForm
    }
    return render(request,"main/my-account.html",context)


def error_404_view(request,exception):
    return render(request,'main/404.html')