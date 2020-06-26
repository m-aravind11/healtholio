from django.contrib import admin
from .models import Disease,Symptom,Medicine
# Register your models here.
admin.site.register(Disease)
admin.site.register(Symptom)
admin.site.register(Medicine)