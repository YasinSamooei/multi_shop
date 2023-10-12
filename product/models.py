from django.db import models

class Size(models.Model):
    title=models.CharField(max_length=10)

    def __str__(self):
        return self.title

class Color(models.Model):
    title=models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Color(models.Model):
    title=models.CharField(max_length=10)

    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField('title', max_length=30)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children',
                            verbose_name='parent')
    slug = models.SlugField('slug', allow_unicode=True, blank=True, null=True, unique=True)
    created_at = models.DateTimeField('created_at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True, null=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['parent__id']

    def __str__(self):
        return self.title

class Product(models.Model):
    title=models.CharField(max_length=30)
    description = models.TextField()
    price= models.IntegerField()
    discount= models.SmallIntegerField()
    image=models.ImageField(upload_to="products")
    size=models.ManyToManyField(Size,related_name="products",blank=True,null=True)
    Color=models.ManyToManyField(Color,related_name="products")
    category=models.ManyToManyField(Category,related_name="products")

    def __str__(self):
        return self.title 

class Information(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="informations")
    text=models.TextField()

    def __str__(self):
        return self.text[:30]