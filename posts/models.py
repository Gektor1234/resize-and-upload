from django.db import models
import PIL
from PIL import Image
from PIL import ImageFile
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
ImageFile.LOAD_TRUNCATED_IMAGES = True

class Post(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def save(self):
        # открывает загруженное изоб.
        im = Image.open(self.cover)

        output = BytesIO()

        # Resize изображения
        im = im.resize((100, 100))

        # после ресайза, сохраняет на выход
        im.save(output, format='JPEG', quality=100)
        output.seek(0)


        # change the imagefield value to be the newley modifed image value
        self.cover = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.cover.name.split('.')[0], 'image/jpeg',
                                        sys.getsizeof(output), None)

        super(Post, self).save()

    def __str__(self):
        return self.title

