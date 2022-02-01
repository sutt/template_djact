from django.db import models
import uuid

# Create your models here.

class Tweet(models.Model):
    uuid = models.UUIDField(unique=True, auto_created=True, default=uuid.uuid4)
    user_string = models.CharField(max_length=100, default='unknown_user')
    content = models.CharField(max_length=256)

    def __str__(self):
        if len(self.content) < 20:
            return str(self.content)
        else:
            return str( self.content[:20] + " ...")