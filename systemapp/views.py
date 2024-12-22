from django.forms import modelformset_factory
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from systemapp.forms import CustomerForm
from .models import Customer, Product
from .forms import InvoiceCreateForm, InvoiceForm, InvoiceProductForm, ProductForm
from .models import Customer, Seller, Invoice, Customer, Product, InvoiceProduct
from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.pdfgen import canvas # type: ignore
from io import BytesIO


def home(request):
    # جلب جميع المنتجات والعملاء
    products = Product.objects.all()
    customers = Customer.objects.all()

    # حساب عدد المنتجات
    total_products = products.count()

    # حساب إجمالي قيمة المخزون (إجمالي السعر)
    total_stock_value = sum(product.price * product.quantity for product in products)

    # حساب إجمالي عدد العملاء
    total_customers = customers.count()

    # حساب عدد العملاء الجدد اليوم باستخدام طريقة البحث حسب بداية ونهاية اليوم
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)  # بداية اليوم
    today_end = today_start + timezone.timedelta(days=1)  # نهاية اليوم

    new_customers_today = customers.filter(created_at__gte=today_start, created_at__lt=today_end).count()

    return render(request, 'content/home.html', {
        'customers': customers,  # جميع العملاء
        'total_customers': total_customers,  # إجمالي عدد العملاء
        'total_products': total_products,
        'total_stock_value': total_stock_value,
        'new_customers_today': new_customers_today,  # عدد العملاء الجدد اليوم
    })

                

def product_list(request):
    success_message = None
    form_add = ProductForm()  # نموذج لإضافة منتج جديد
    form_edit = None  # النموذج المعدل

    if request.method == 'POST':
        # إذا كانت العملية هي تعديل
        product_id = request.POST.get('product_id', None)
        if product_id:
            product = get_object_or_404(Product, id=product_id)

            # إذا كان المستخدم قد ضغط على زر "تعديل المنتج"
            if 'edit_product' in request.POST:
                form_edit = ProductForm(request.POST, instance=product)  # تعبئة النموذج بالبيانات القديمة
                if form_edit.is_valid():
                    form_edit.save()  # حفظ التعديلات
                    success_message = "تم تعديل المنتج بنجاح!"
                    return redirect('product_list')  # إعادة تحميل الصفحة بعد التعديل
            elif 'delete_product' in request.POST:  # إذا كان المستخدم ضغط على زر حذف
                product.delete()
                success_message = "تم حذف المنتج بنجاح!"
                return redirect('product_list')  # إعادة تحميل الصفحة بعد الحذف
        else:
            # إذا كان لا يوجد product_id، فهذا يعني أننا نقوم بإضافة منتج جديد
            form_add = ProductForm(request.POST)
            if form_add.is_valid():
                form_add.save()
                success_message = "تم إضافة المنتج بنجاح!"
                return redirect('product_list')

    else:
        # إذا كان الطلب GET، نقوم بإحضار المنتج لتعديل بياناته
        product_id = request.GET.get('product_id', None)
        if product_id:
            product = get_object_or_404(Product, id=product_id)
            form_edit = ProductForm(instance=product)  # تعبئة النموذج ببيانات المنتج الحالي

    # جلب جميع المنتجات
    products = Product.objects.all()

    # حساب عدد المنتجات
    total_products = products.count()

    # حساب إجمالي قيمة المخزون (إجمالي السعر)
    total_stock_value = sum(product.price * product.quantity for product in products)

    return render(request, 'content/product.html', {
        'products': products,
        'form_add': form_add,
        'form_edit': form_edit,
        'success_message': success_message,
        'total_products': total_products,
        'total_stock_value': total_stock_value,
    })




def customer_list(request):
    customers = Customer.objects.all()  # جلب جميع العملاء
    success_message = None
    
    # حساب عدد العملاء الجدد اليوم
    today = timezone.now().date()  # الحصول على تاريخ اليوم
    new_customers_today = Customer.objects.filter(created_at=today).count()  # عدد العملاء الجدد اليوم
    
    # إضافة عميل جديد
    if request.method == 'POST':
        if 'add_customer' in request.POST:
            form = CustomerForm(request.POST)
            if form.is_valid():
                form.save()
                success_message = "تم إضافة العميل بنجاح!"
                return redirect('customer_list')  # إعادة التوجيه للصفحة بعد الإضافة

        # تعديل عميل
        if 'edit_customer' in request.POST:
            customer_id = request.POST.get('customer_id')
            customer = get_object_or_404(Customer, id=customer_id)
            form = CustomerForm(request.POST, instance=customer)
            if form.is_valid():
                form.save()
                success_message = "تم تعديل بيانات العميل بنجاح!"
                return redirect('customer_list')  # إعادة التوجيه للصفحة بعد التعديل

        # حذف عميل
        if 'delete_customer' in request.POST:
            customer_id = request.POST.get('customer_id')
            customer = get_object_or_404(Customer, id=customer_id)
            customer.delete()
            success_message = "تم حذف العميل بنجاح!"
            return redirect('customer_list')  # إعادة التوجيه للصفحة بعد الحذف

    return render(request, 'content/clint.html', {
        'customers': customers,
        'success_message': success_message,
        'new_customers_today': new_customers_today,  # تمرير عدد العملاء الجدد
    })

# views.py

def invoice_list(request):
    # استرجاع جميع الفواتير المرتبطة بالعملاء والبائعين
    invoices = Invoice.objects.select_related('customer', 'seller').all()

    return render(request, 'content/invoice_lists.html', {
        'invoices': invoices,  # تمرير جميع الفواتير
    })

def view_invoice(request, id):
    # جلب الفاتورة باستخدام ID
    invoice = get_object_or_404(Invoice, id=id)
    
    # جلب المنتجات المرتبطة بالفاتورة
    invoice_products = invoice.products.all()
    
    # تمرير الفاتورة والمنتجات إلى القالب
    return render(request, 'content/view_invoice.html', {
        'invoice': invoice,
        'invoice_products': invoice_products
    })


def delete_invoice(request, id):
    # جلب الفاتورة باستخدام ID
    invoice = get_object_or_404(Invoice, id=id)
    
    # حذف الفاتورة
    invoice.delete()
    
    # إعادة التوجيه إلى صفحة الفواتير بعد الحذف
    return redirect('invoice_list')  # تأكد من أن 'invoice_list' هو اسم المسار المناسب

def add_invoice(request):
    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST)
        if invoice_form.is_valid():
            invoice = invoice_form.save()

            # معالجة بيانات المنتجات
            product_forms = []
            for i in range(int(request.POST.get('product_count', 0))):
                product_form = InvoiceProductForm(request.POST, prefix=f'product_{i}')
                if product_form.is_valid():
                    product_form.instance.invoice = invoice
                    product_form.save()
                    product_forms.append(product_form)
                    return redirect('invoice_list') 
    else:
        invoice_form = InvoiceForm()
        product_form = InvoiceProductForm(prefix='product_0')

    context = {
        'invoice_form': invoice_form,
        'product_form': product_form,
    }
    return render(request, 'content/add_invoice.html', context)