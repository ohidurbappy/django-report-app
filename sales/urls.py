from django.urls import path
from .views import index, SalesListView, SaleDetailView

app_name = 'sales'

urlpatterns = [
    path('', index, name='home'),
    path('sales/', SalesListView.as_view(), name='list'),
    path('sales/<pk>/', SaleDetailView.as_view(), name='detail')


]
