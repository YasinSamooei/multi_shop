from django.shortcuts import render , redirect , get_object_or_404
from django.views import View
from product.models import Product
from account.models import Address
from .models import Order,OrderItem,DiscountCode
from .madule import Cart
import requests
import json
from django.conf import settings
from django.http import HttpResponse
class CartDetailView(View):
    def get(self,request):
        cart=Cart(request)
        return render(request,"cart/cart.html",{'cart':cart})
        
class CartAddView(View):
    def post(self,request,pk):
        product=get_object_or_404(Product,id=pk)
        size,color,quantity=request.POST.get('size','empty'),request.POST.get('color','empty'),request.POST.get('quantity')
        cart=Cart(request)
        cart.add(product,quantity,color,size)
        return redirect("cart:Cart-detail")

class CartDeleteView(View):
    def get(self,request,id):
        cart= Cart(request)
        cart.delete(id)
        return redirect("cart:Cart-detail")

class OrderDetailView(View):
    def get(self,request,pk):
        order = get_object_or_404(Order,id=pk)
        return render(request,'cart/order_detail.html',{'order':order})

class OrderCreationView(View):
    def get(self,request):
        cart=Cart(request)
        order = Order.objects.create(user=request.user,total_price=cart.total())
        for item in cart:
            OrderItem.objects.create(order=order,product=item['product'],color=item['color'],size=item['size'],quantity=item['quantity'],price=item['price'])
        cart.remove_cart()
        return redirect('cart:order-detail',order.id)
    
class ApplyDiscountView(View):
    def post(self,request,pk):
        code=request.POST.get('discount_code')
        order=get_object_or_404(Order,id=pk)
        discount_code=get_object_or_404(DiscountCode,name=code)
        if discount_code.quantity==0:
            return redirect('cart:order-detail',order.id)
        order.total_price -= order.total_price*discount_code.discount/100
        order.save()
        discount_code.quantity -= 1
        discount_code.save()
        return redirect('cart:order-detail',order.id)







#? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

MERCHANT = "00000000-0000-0000-0000-000000000000"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/cart/verify/'


class SendRequestView(View):
    def post(self,request,pk):
        order=get_object_or_404(Order,id=pk,user=request.user)
        address=get_object_or_404(Address,id=request.POST.get('address'))
        order.address=f"{address.address}-{address.phone}"
        order.save()
        req_data = {
            "merchant_id": MERCHANT,
            "amount": order.total_price,
            "callback_url": CallbackURL,
            "description": description,
            "metadata": {"mobile": request.user.phone}
        }
        req_header = {"accept": "application/json",
                    "content-type": "application/json'"}
        req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
            req_data), headers=req_header)
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


class VerifyView(View):
    def get(request):
        order_id=request.session['order_id']
        order=Order.objects.get(id=int(order_id))
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": order.total_price,
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    return HttpResponse('Transaction success.\nRefID: ' + str(
                        req.json()['data']['ref_id']
                    ))
                elif t_status == 101:
                    return HttpResponse('Transaction submitted : ' + str(
                        req.json()['data']['message']
                    ))
                else:
                    return HttpResponse('Transaction failed.\nStatus: ' + str(
                        req.json()['data']['message']
                    ))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
        else:   
            return HttpResponse('Transaction failed or canceled by user')