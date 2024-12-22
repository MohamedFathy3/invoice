from django.db import models
from datetime import datetime
# Create your models here.

class Product(models.Model):
    # حقل لاسم المنتج
    name = models.CharField(max_length=255)
    
    # حقل للكمية
    quantity = models.IntegerField()
    
    # حقل للسعر
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

    # خاصية لحساب إجمالي السعر
    @property
    def total_price(self):
        return self.price * self.quantity
    


class Customer(models.Model):
    # حقل لاسم العميل
    name = models.CharField(max_length=255)
    
    # حقل لرقم الهاتف
    phone_number = models.CharField(max_length=15)  # يمكن تخزين الأرقام بطول أقصى 15 خانة
    
    # حقل لتاريخ التسجيل
    created_at = models.DateField(auto_now_add=True)  # تاريخ التسجيل يتم تعيينه تلقائيًا عند الإضافة
    
    def __str__(self):
        return self.name


class Seller(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    phone_number = models.CharField(max_length=15)  # حقل رقم الهاتف
    invoice_number = models.CharField(max_length=20, unique=True, blank=True)  # رقم الفاتورة

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            super().save(*args, **kwargs)
            self.invoice_number = f"INV-{self.date.strftime('%Y%m%d')}-{str(self.pk).zfill(5)}"
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def total_invoice_price(self):
        # جمع إجمالي الأسعار لجميع المنتجات المرتبطة بالفاتورة
        return sum(item.total_price() for item in self.products.all())  # باستخدام related_name 'products'

    def __str__(self):
        return f"فاتورة رقم {self.invoice_number} - {self.customer.name}"
    


    
class InvoiceProduct(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        # حساب إجمالي السعر بناءً على الكمية والسعر
        if self.quantity and self.price:
            return self.quantity * self.price
        return 0  # إرجاع 0 إذا كانت الكمية أو السعر غير صحيحة

    def __str__(self):
        return f"{self.product.name} - {self.quantity} x {self.price}"
