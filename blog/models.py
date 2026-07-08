from django.db.models import Model, CharField, TextField, IntegerField, ForeignKey, ManyToManyField, SET_NULL, CASCADE, ImageField
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse


class Place(Model):
    """This model will represent each place we want to review"""
    user = ForeignKey(to=User, on_delete=SET_NULL, null=True, blank=True)
    name = CharField(verbose_name="Name", max_length=100, unique=True)
    address = CharField(verbose_name="Address", max_length=150, null=True, blank=True)
    phone = IntegerField(verbose_name="Telephone", null=True, blank=True)
    description = TextField(verbose_name="Description", max_length=1000)
    image = ImageField(default="default_place.png", upload_to="place_pics")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 600:
            max_dimensions = (300, 600)
            img.thumbnail(max_dimensions)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk":self.pk})

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.id} - {self.name}"
    
    def __str__(self):
        return f"{self.name}"
    
class Review(Model):
    """This model will be the review a user writes about a place"""
    user = ForeignKey(to=User, on_delete=SET_NULL, null=True, blank=True)
    place = ForeignKey(to=Place, on_delete=CASCADE)
    description = TextField(verbose_name="Description", max_length=500)

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.id}"
    
    def __str__(self):
        return f"{self.user.username}: {self.description}"
    
class Category(Model):
    """This model will contain all the categories a place can have."""
    name = CharField(verbose_name="Name", max_length=100)
    place = ManyToManyField(to=Place, verbose_name="Place")
    
    def __repr__(self):
        return f"{self.__class__.__name__}: {self.name}"
    
    def __str__(self):
        return f"{self.name}"
    
class Like(Model):
    """This model will be the likes a user can give to a Place or a Review"""
    place = ForeignKey(to=Place, on_delete=CASCADE, null=True)
    review = ForeignKey(to=Review, on_delete=CASCADE, null=True)
    user = ForeignKey(to=User, on_delete=CASCADE)

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.id}"
    
    def __str__(self):
        return f"{self.__class__.__name__}: {self.id}"


