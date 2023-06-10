from PIL import Image, ImageDraw
from django.db import models
from django.contrib.auth.models import AbstractUser


def render_image_with_watermark(photo_path):
    photo = Image.open(photo_path)
    photo.load()

    background = Image.new("RGBA", photo.size, (0, 0, 0))

    watermark = Image.open('assets/watermark.png')
    watermark = watermark.resize(photo.size)
    background.paste(photo)

    background.paste(watermark, mask=watermark.split()[3])
    background = background.convert(photo.mode)

    background.save(photo_path, quality=100)


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True)  # аватар
    sex = models.CharField(max_length=100, null=False)  # пол
    match = models.ManyToManyField('self', blank=True)  # совпадение симпатии
    outgoing_match_requests = models.ManyToManyField(
        'self', symmetrical=False, related_name='incoming_match_requests', blank=True)  # исходящие симпатии
    __original_avatar = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_avatar = self.avatar

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        new_instance = self.id is None
        super().save(*args, **kwargs)
        if new_instance or (self.avatar != self.__original_avatar):
            if self.avatar:
                render_image_with_watermark(self.avatar.path)
