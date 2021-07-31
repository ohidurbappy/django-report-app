from django.db import models
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from pandas.core.base import IndexOpsMixin
from .models import Sale
from .forms import SalesSearchForm
from reports.forms import ReportForm
import pandas as pd
from .utils import *


from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def index(request):
    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm()
    sales_df = None
    positions_df = None
    merged_df = None
    chart = None
    no_data = True

    df = None

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')
        print(date_from, date_to, chart_type, results_by)

        # qs = Sale.objects.all()
        qs = Sale.objects.filter(
            created__date__lte=date_to, created__date__gte=date_from)
        if len(qs) > 0:
            no_data = False
            print('#'*20)
            sales_df = df1 = pd.DataFrame(qs.values())

            # pandas apply
            sales_df['customer_id'] = sales_df['customer_id'].apply(
                get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(
                get_salesman_from_id)
            sales_df['sales_id'] = sales_df['id']
            sales_df['created'] = sales_df['created'].apply(
                lambda x: x.strftime("%Y-%m-%d"))
            sales_df['updated'] = sales_df['updated'].apply(
                lambda x: x.strftime("%Y-%m-%d"))

            # rename columns
            sales_df.rename({'customer_id': 'customer',
                            'salesman_id': 'salesman'}, axis=1, inplace=True)

            positions_data = []

            for sale in qs:
                for position in sale.get_positions():
                    obj = {
                        'position': position.id,
                        'product': position.product.name,
                        'quantity': position.quantity,
                        'price': position.price,
                        'sales_id': position.get_sales_id()
                    }

                    positions_data.append(obj)

            positions_df = pd.DataFrame(positions_data)

            # merging the two dataframes

            merged_df = pd.merge(sales_df, positions_df, on='sales_id')

            df = merged_df.groupby('transaction_id', as_index=False)[
                'price'].agg('sum')

            # get the chart

            # chart = get_chart(
            #     chart_type, df, results_by, labels=df['transaction_id'].values)
            chart = get_chart(
                chart_type, sales_df, results_by, labels=df['transaction_id'].values)

            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            merged_df = merged_df.to_html()
            df = df.to_html()

            print(df1)
            print('#'*20)
        else:
            print("No data")

            # print(qs)
            # print(qs.values())
            # print(qs.values_list())

            # df2 = pd.DataFrame(qs.values_list())
            # print(df2)
            # print('#'*20)

    context = {
        'search_form': search_form,
        'report_form': report_form,
        'sales_df': sales_df,
        'positions_df': positions_df,
        'merged_df': merged_df,
        'df': df,
        "no_data": no_data,
        'chart': chart
    }

    return render(request, 'sales/home.html', context=context)


class SalesListView(LoginRequiredMixin,ListView):
    model = Sale
    template_name = 'sales/main.html'
    context_object_name = 'sales_items'


class SaleDetailView(LoginRequiredMixin,DetailView):
    model = Sale
    template_name = 'sales/detail.html'


# using function views
@login_required
def sale_list_view(request):
    qs = Sale.objects.all()
    return render(request, 'sales/main.html', {'object_list': qs})

@login_required
def sale_detail_view(request, pk):
    obj = Sale.objects.get(pk=pk)
    return render(request, 'sales/detail.html', {'object': obj})
