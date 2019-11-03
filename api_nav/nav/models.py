from django.db import models


# Create your models here.

class NestedCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    lft = models.IntegerField(null=False)
    rgt = models.IntegerField(null=False)
