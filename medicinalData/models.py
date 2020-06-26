from django.db import models
from users.models import user
# Create your models here.

class Medicine(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Symptom(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Disease(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Prescription(models.Model):
    date = models.DateField(auto_now=True)
    diagnosis = models.ForeignKey(Disease,on_delete=models.CASCADE)
    status = models.CharField(max_length = 10,null = True)

class Advice(models.Model):
    adv = models.CharField(max_length = 200,null = True)
    prescription = models.ForeignKey(Prescription,on_delete=models.CASCADE)

class Dosage(models.Model):
    time_of_day = models.CharField(max_length = 20)
    duration = models.CharField(max_length = 20)
    when = models.CharField(max_length = 20)
    med = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    amount = models.CharField(max_length = 10,null=True)
    prescription = models.ForeignKey(Prescription,on_delete=models.CASCADE)
    med_type = models.CharField(max_length = 3,null = True)

class linktable(models.Model):
    prescription = models.ForeignKey(Prescription,on_delete=models.CASCADE)
    user = models.ForeignKey(user,on_delete=models.CASCADE)
    user_type = models.CharField(max_length = 10)

    def save(self):
        self.user_type = self.user.type
        super().save()

class complaints(models.Model):
    symptom = models.ForeignKey(Symptom,on_delete=models.CASCADE)
    prescription = models.ForeignKey(Prescription,on_delete=models.CASCADE)

class hashtable(models.Model):
    pres = models.ForeignKey(Prescription,on_delete=models.CASCADE)
    hashcode = models.CharField(max_length = 200)