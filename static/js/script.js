let productCount = 1; // عداد المنتجات المضافة
const totalInvoiceAmountElement = document.getElementById('totalInvoiceAmount');

// وظيفة لحساب المبلغ الإجمالي لكل منتج
function calculateProductTotal(productId) {
    const price = parseFloat(document.getElementById(`productPrice${productId}`).value);
    const quantity = parseInt(document.getElementById(`productQuantity${productId}`).value);
    
    if (!isNaN(price) && !isNaN(quantity)) {
        const total = price * quantity;
        document.getElementById(`totalAmount${productId}`).innerText = total.toFixed(2);
        return total;
    } else {
        document.getElementById(`totalAmount${productId}`).innerText = '0';
        return 0;
    }
}

// وظيفة لحساب المبلغ الإجمالي للفاتورة
function calculateInvoiceTotal() {
    let totalInvoiceAmount = 0;
    for (let i = 1; i <= productCount; i++) {
        totalInvoiceAmount += calculateProductTotal(i);
    }
    totalInvoiceAmountElement.innerText = totalInvoiceAmount.toFixed(2);
}

// إضافة مستمعين لحساب المبالغ عند تغيير السعر أو الكمية
document.getElementById('addProductBtn').addEventListener('click', function() {
    productCount++;
    const newProductRow = document.createElement('div');
    newProductRow.classList.add('product-row');
    newProductRow.id = `productRow${productCount}`;
    newProductRow.innerHTML = `
        <h6>المنتج ${productCount}</h6>
        <div class="mb-3">
            <label for="productSelect${productCount}" class="form-label">اختر المنتج</label>
            <select class="form-select productSelect" id="productSelect${productCount}" required>
                <option value="" disabled selected>اختر المنتج</option>
                <option value="منتج 1">منتج 1</option>
                <option value="منتج 2">منتج 2</option>
                <option value="منتج 3">منتج 3</option>
                <option value="منتج 4">منتج 4</option>
            </select>
        </div>
        <div class="mb-3">
            <label for="productPrice${productCount}" class="form-label">السعر لكل منتج (جنيه)</label>
            <input type="number" class="form-control productPrice" id="productPrice${productCount}" placeholder="أدخل السعر لكل منتج" required>
        </div>
        <div class="mb-3">
            <label for="productQuantity${productCount}" class="form-label">الكمية</label>
            <input type="number" class="form-control productQuantity" id="productQuantity${productCount}" placeholder="أدخل الكمية" required>
        </div>
        <div class="total-amount">
            <span>المبلغ الإجمالي لهذا المنتج: </span><span id="totalAmount${productCount}">0</span> جنيه
        </div>

        <!-- زر حذف المنتج -->
        <button type="button" class="btn-remove" onclick="removeProduct(${productCount})">حذف المنتج</button>
    `;
    document.getElementById('productsContainer').appendChild(newProductRow);

    // إضافة مستمعات لحساب المبلغ عند التغيير في السعر أو الكمية
    document.getElementById(`productPrice${productCount}`).addEventListener('input', calculateInvoiceTotal);
    document.getElementById(`productQuantity${productCount}`).addEventListener('input', calculateInvoiceTotal);
});

// وظيفة لحذف المنتج
function removeProduct(productId) {
    const productRow = document.getElementById(`productRow${productId}`);
    productRow.remove();  // إزالة السطر الخاص بالمنتج
    calculateInvoiceTotal();  // إعادة حساب المبلغ الإجمالي
}

// إضافة مستمعين لحساب المبلغ الإجمالي عند التغيير في السعر أو الكمية
document.querySelectorAll('.productPrice').forEach(input => input.addEventListener('input', calculateInvoiceTotal));
document.querySelectorAll('.productQuantity').forEach(input => input.addEventListener('input', calculateInvoiceTotal));

// وظيفة لتقديم النموذج عند الضغط على زر إضافة الفاتورة
document.getElementById('submitInvoiceBtn').addEventListener('click', function() {
    var form = document.getElementById('invoiceForm');
    if (form.checkValidity()) {
        alert("تم إضافة الفاتورة بنجاح!");
        var modal = bootstrap.Modal.getInstance(document.getElementById('addInvoiceModal'));
        modal.hide();
    } else {
        form.reportValidity();
    }
});