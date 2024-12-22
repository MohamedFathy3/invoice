from django.contrib import admin
from .models import Customer,Product,Invoice,InvoiceProduct
# Register your models here.


admin.site.register(Customer)
admin.site.register(Product)

# تعريف Inline لعرض المنتجات المرتبطة بكل فاتورة داخل صفحة الفاتورة
class InvoiceProductInline(admin.TabularInline):
    model = InvoiceProduct
    extra = 1
    fields = ('product', 'quantity', 'price', 'total_price')  # إضافة total_price لعرضه في النموذج
    readonly_fields = ('total_price',)
      # تعيين total_price ليكون حقل للعرض فقط
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'customer', 'seller', 'phone_number', 'total_price_display', 'date']
    
    # دالة لعرض total_price
    def total_price_display(self, obj):
        # هنا يمكنك حساب total_price استنادًا إلى المنتجات في الفاتورة أو أية معايير أخرى
        # مثال:
        return sum(product.price for product in obj.products.all())  # افترض أن لديك علاقة many-to-many مع المنتجات
        
    total_price_display.short_description = 'إجمالي السعر'  # تخصيص اسم العمود في واجهة الإدارة

class InvoiceProductAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'product', 'quantity', 'price', 'total_price')  # الحقول التي تظهر في جدول المنتجات المرتبطة بالفواتير
    search_fields = ('invoice__invoice_number', 'product__name')  # البحث في رقم الفاتورة واسم المنتج
    list_filter = ('invoice', 'product')  # تصفية المنتجات حسب الفاتورة أو المنتج

# تسجيل الفاتورة والمنتجات المرتبطة بها في لوحة الإدارة
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceProduct, InvoiceProductAdmin)