from django.db import models
# прописываем модели

class Resource_accounting(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=15)
    amount = models.FloatField()
    type_measure = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    date = models.DateField()


    def __str__(self):
        return self.name

