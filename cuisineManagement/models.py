from django.db import models

# Create your models here.

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Starter', 'Starter'),
        ('Main Course', 'Main Course'),
        ('Desserts', 'Desserts'),
        ('Beverages', 'Beverages'),
    ]
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    SUBCATEGORY_CHOICES = [
        ('Veg', 'Vegetarian'),
        ('Non-Veg', 'Non-Vegetarian'),
    ]
    name = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class CuisineType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='menu_category', on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, related_name='menu_subcategory', on_delete=models.CASCADE)
    type = models.ForeignKey(CuisineType, related_name='cuisine_type', on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, blank=True)
   
    def __str__(self):
        return self.name
    
class MenuItemImage(models.Model):
    menu_item = models.ForeignKey(MenuItem, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='menu_item_images/')

    def __str__(self):
        return f"Image for {self.menu_item.name}"
    