from django.db import  models
from django.contrib.auth.models import User

class Santri(models.Model):
  
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  hp = models.CharField(max_length=20)
  gender=models.CharField(choices=[('L','Laki-laki'),('K','Perempuan')], max_length=1,default='L')
  tgl_lahir=models.DateField()
  tahun_penerimaan=models.SmallIntegerField()

  def __str__(self):
    return f"Santri ID: {self.pk}"

class Soal(models.Model):
  pertanyaan = models.CharField(max_length=255)
  jawaban_benar = models.CharField(max_length=1)#a,b,c,d

  def __str__(self):
    return self.pertanyaan
  
class PilihanJawaban(models.Model):
  soal=models.ForeignKey(Soal,related_name="pilihan",on_delete=models.CASCADE)
  kode=models.CharField(max_length=1)#a,b,c,d
  teks=models.CharField(max_length=255)

  def __str__(self):
    return f"{self.kode}. {self.teks}"
  
class Nilai(models.Model):
  santri = models.ForeignKey(Santri,related_name="nilai_santri",on_delete=models.CASCADE)
  nilai=models.DecimalField(max_digits=5,decimal_places=2)

  def __str__(self):
    return str(self.nilai)

class Evaluasi(models.Model):
  santri =models.ForeignKey(Santri,related_name="jawaban_santri",on_delete=models.CASCADE)
  soal =models.ForeignKey(Soal,related_name="jwbn_santri",on_delete=models.CASCADE)
  jawaban_santri=models.CharField(max_length=1)#a,b,c,d

  def __str__(self):
    return self.jawaban_santri