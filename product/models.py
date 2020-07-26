from django.db import models

# Create your models here.
class Category(models.Model):
    STATUS =(
        ('True','Evet'),
        ('False','Hayır')
    )
    title = models.CharField(max_length=30)
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

