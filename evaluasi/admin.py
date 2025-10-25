from django.contrib import admin

from . import models
# from models import 

def get_all_model_fields(model):
  return [field.name for field in model._meta.fields]

class Santri(admin.ModelAdmin):
  list_display=get_all_model_fields(models.Santri)

class Soal(admin.ModelAdmin):
  list_display=get_all_model_fields(models.Soal)

class PilihanJawaban(admin.ModelAdmin):
  list_display=get_all_model_fields(models.PilihanJawaban)

class Nilai(admin.ModelAdmin):
  list_display=get_all_model_fields(models.Nilai)

class Evaluasi(admin.ModelAdmin):
  list_display=get_all_model_fields(models.Evaluasi)


admin.site.register(models.Santri,Santri)
admin.site.register(models.Soal,Soal)
admin.site.register(models.PilihanJawaban,PilihanJawaban)
admin.site.register(models.Nilai,Nilai)
admin.site.register(models.Evaluasi,Evaluasi)
