from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe


class Category(models.Model):
    STATUS =(
        ('True','Evet'),
        ('False','Hayır')
    )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    keywords=models.CharField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/')
    status=models.CharField(max_length=30, choices=STATUS)
    slug=models.SlugField()
    parent=models.ForeignKey('self',blank=True, null=True,related_name='children',on_delete=models.CASCADE)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class Product(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    #dersler-ogrenciler : many to many
    #danışman-öğrencilar : many to one
    #üye-kimlik bilgisi : one to one
    #ürünler ile kategori arasındaki ilişki
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # relation with Category table
    title = models.CharField(max_length=150)
    keywords = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.FloatField()
    amount = models.IntegerField()
    detail = models.TextField()
    #slug = models.SlugField(null=False, unique=True)
    status = models.CharField(blank=True, max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    #burada otomatik slug oluşturma fonk. yazdık.
    #def get_absolute_url(self):
     #   return reverse('product_detail', kwargs={'slug': self.slug})

class Images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(blank=True,max_length=50)
    image = models.ImageField(blank=True, upload_to='images/')
    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

