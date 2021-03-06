from django.db import models
from django.utils import timezone
import uuid

# Create your models here.

class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    identifier = models.CharField(max_length=20, null=True)
    language = models.CharField(max_length=20, null=True)

    # field that described the status of the processing process
    # 0 -> opened but not started
    # 1 -> processing / ongoing
    # 2 -> closed
    status = models.IntegerField(default=0)

class TextData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_text = models.TextField()
    status = models.IntegerField(default=0)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    entities = models.JSONField(null=True)
    syllable = models.IntegerField(null=True)
    replacement_text = models.TextField(null=True)
    type = models.BooleanField(default=False) # False = to de-identify / True = to re-identify
    time_start = models.FloatField(null=True)
    time_end = models.FloatField(null=True)

class Entity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    in_entity = models.CharField(max_length=300)
    out_entity = models.CharField(max_length=300, null=True)
    type_entity = models.CharField(max_length=100, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)