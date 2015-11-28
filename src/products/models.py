from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify

# Create your models here.


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    active = models.BooleanField(default=True)
    # slug
    # inventory

    objects = ProductManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={'pk': self.pk})


class Variation(models.Model):
    product = models.ForeignKey(Product)
    title = models.CharField(max_length=120)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    sale_price = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(blank=True, null=True)  # refer none == unlimited amount

    def __unicode__(self):
        return self.title

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()


def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
    product = instance
    variations = product.variation_set.all()
    if variations.count() == 0:
        new_vari = Variation()
        new_vari.product = product
        new_vari.title = 'Default'
        new_vari.price = product.price
        new_vari.save()


post_save.connect(product_post_saved_receiver, sender=Product)


def image_upload_to(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    file_extension = filename.split(".")[1]
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return "products/%s/%s" % (slug, new_filename)

# Product Image
# sudo yum install --assumeyes libjpeg-devel
# sudo pip-python install --upgrade PIL


class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to=image_upload_to)

    def __unicode__(self):
        return self.product.title


# Product Category
