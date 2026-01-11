from django.urls import path
from . import views

urlpatterns = [
    path('process-payment/', views.ProcessPaymentView.as_view(), name='process-payment'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('purchases/', views.PurchaseListView.as_view(), name='purchase-list'),
]
