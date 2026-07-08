from django.db.models import Model, TextField, ImageField, OneToOneField, CASCADE
from django.contrib.auth.models import User
from PIL import Image


class Profile(Model):
    """This one will be linked to the django default username to add a "bio" and "image"."""

    bio = TextField(verbose_name="Bio", blank=True, null=True, max_length=500)
    user = OneToOneField(to=User, on_delete=CASCADE, null=False, blank=False)
    image = ImageField(default="default_pic.png", upload_to="profile_pics")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            max_dimensions = (300,300)
            img.thumbnail(max_dimensions)
            img.save(self.image.path)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id, self.user.username})"
    
    def __str__(self):
        return f"{self.__class__.__name__}: {self.user.username}"

