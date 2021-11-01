from django.db import models

# Create your models here.
class Client(models.Model):
    id = models.CharField(max_length=20)
    data = models.JSONField(null=True)

class Caregiver(models.Model):
    id = models.CharField(max_length=20)
    data = models.JSONField(null=True)

class Session(models.Model):
    identifier = models.CharField(max_length=20, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    caregiver = models.ForeignKey(Caregiver, on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=20, null=True)

    # field that described the status of the processing process
    # 0 -> opened but not started
    # 1 -> processing / ongoing
    # 2 -> closed
    status = models.IntegerField(default=0)

class Sentence(models.Model):
    original_text = models.TextField()
    status = models.IntegerField(default=0)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    entities = models.JSONField(null=True)
    replacement_text = models.TextField(null=True)

class Entity(models.Model):
    in_entity = models.CharField(max_length=100)
    out_entity = models.CharField(max_length=100, null=True)
    type_entity = models.CharField(max_length=100, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

class Eponym(models.Model):
    language = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
