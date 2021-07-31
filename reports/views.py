from datetime import datetime
from time import timezone
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404
from profiles.models import Profile
from django.http import JsonResponse
from .models import Report
from .utils import get_report_image
from .forms import ReportForm
from django.views.generic import ListView, DetailView, TemplateView 

from products.models import Product
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import csv 
from sales.models import Sale,Position,CSV 
from customers.models import Customer
from django.utils.dateparse import parse_date
from django.utils import timezone


from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



class ReportListView(LoginRequiredMixin,ListView):
    model = Report
    template_name = "reports/main.html"


class ReportDetailView(DetailView):
    model = Report
    template_name = "reports/detail.html"


class UploadTemplateView(LoginRequiredMixin,TemplateView):
    template_name="reports/from_file.html"


@login_required
def csv_upload_view(request):
    print('file uploaded')
    if request.method=='POST':

        
        csv_file_name=request.FILES.get('file').name
        csv_file=request.FILES.get('file')
        obj,created=CSV.objects.get_or_create(filename=csv_file_name)

        if created:
            obj.csv_file=csv_file
            obj.save()
            with open(obj.csv_file.path,'r') as f:
                reader=csv.reader(f)
                next(reader)
                for row in reader:
                    # data=",".join(row)
                    # print(data,type(row))
                    transaction_id=row[1]
                    product=row[2]
                    quantity=int(row[3])
                    customer=row[4]
                    date=parse_date(row[5])
                    date=timezone.now()

                    try:
                        product_obj=Product.objects.get(name__iexact=product)
                    
                    except Product.DoesNotExist:
                        product_obj=None

                    if product_obj is not None:
                        customer_obj, _ = Customer.objects.get_or_create(name=customer) 
                        salesman_obj = Profile.objects.get(user=request.user)
                        position_obj = Position.objects.create(product=product_obj, quantity=quantity,created=date)

                        sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id, customer=customer_obj, salesman=salesman_obj,created=date)
                        sale_obj.positions.add(position_obj)
                        sale_obj.save()
            return JsonResponse({'ex':False})
        else:
            return JsonResponse({'ex':True})


    return HttpResponse()

@login_required
def create_report_view(request):
    if request.is_ajax():
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        image = request.POST.get('image')
        author = Profile.objects.get(user=request.user)

        img = get_report_image(image)

        # Report.objects.create(name=name,remarks=remarks,image=img,author=author)

        # alternative way...
        form = ReportForm(request.POST or None)
        if request.is_ajax():
            if form.is_valid():
                instance = form.save(commit=False)
                instance.image = img
                instance.author = author
                instance.save()
        return JsonResponse({
            'msg': 'send'
        })
    return JsonResponse({})


@login_required
def render_pdf_view(request, pk):
    template_path = 'reports/pdf.html'

    # report=Report.objects.get(pk=pk)
    report = get_object_or_404(Report, pk=pk)

    context = {'report': report}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # for displaying in the browser.......
    response['Content-Disposition'] = 'filename="report.pdf"'
    # for downloading.................
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
