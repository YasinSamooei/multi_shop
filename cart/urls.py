from django.urls import path
from . import views

app_name="cart"

urlpatterns=[
    path('detail',views.CartDetailView.as_view(),name="Cart-detail"),
    path('add/<int:pk>',views.CartAddView.as_view(),name="Cart-add"),
    path('delete/<str:id>',views.CartDeleteView.as_view(),name="cart-delete"),
    path('order/<int:pk>',views.OrderDetailView.as_view(),name="order-detail"),
    path('order/create',views.OrderCreationView.as_view(),name="order-creation"),
    path('apply/discount/<int:pk>',views.ApplyDiscountView.as_view(),name="apply-discount"),
    path('sendrequest/<int:pk>',views.SendRequestView.as_view(),name="send-request"),
]