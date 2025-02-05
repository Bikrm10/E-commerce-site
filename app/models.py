from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator,MinLengthValidator
STATE_CHOICE = (
    ("Koshi Pradesh","Koshi Pradesh"),
    ("Madhesh Pradesh","Madhesh Pradesh"),
    ("Gandaki Pradesh","Gandaki Pradesh"),
    ("Bagmati Pradesh","Bagmati Pradesh"),
    ("Karnali Pradesh","Karnali Pradesh"),
    (" Lumbini Pradesh","Lumbini Pradesh"),
    ('Sudurpaschim Pradesh','Sudurpaschim Pradesh')
)
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.IntegerField()
    state = models.CharField(choices = STATE_CHOICE, max_length=50)

    def __str__(self):
        return str(self.id)
CATEGORY_CHOICES = (
    ('M',"Mobile"),
    ('L',"Laptop"),
    ('TW',"Top Wear"),
    ('BW',"Bottom Wear"),
)
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    brand = models.CharField(max_length=100)
    description = models.TextField(default = "Lorem Ipsum ")
    category = models.CharField(choices=  CATEGORY_CHOICES,max_length=2)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)
    

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    #this is property not incuded in the model which isonly derived from the proerty used in the model
    @property
    def total_cost(self):
        return self.quantity* self.product.discounted_price
    
STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On way','On way'),
    ('Delivered','Delivered')
)
class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default="Pending")
    def __str__(self):
        return str(self.id)
    


