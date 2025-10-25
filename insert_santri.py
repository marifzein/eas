from django.contrib.auth.models import User
from evaluasi.models import Santri
from django.db import transaction

# Data Santri yang Anda berikan
SANTRI_DATA = [
    {'nip': 'ARN202-12345', 'nama': 'Rizky Hamdan', 'hp': '081234567890', 'gender': 'L', 'tahun': 2020},
    {'nip': 'ARN201-30678', 'nama': 'Hasan Widodo', 'hp': '085698765432', 'gender': 'L', 'tahun': 2020},
    {'nip': 'ARN232-12221', 'nama': 'Zulkifli Bambang', 'hp': '087712345678', 'gender': 'L', 'tahun': 2023},
    {'nip': 'ARN221-67890', 'nama': 'Fikri Jaya', 'hp': '082155554444', 'gender': 'L', 'tahun': 2022},
    {'nip': 'ARN224-80001', 'nama': 'Faruq Hidayat', 'hp': '089600112233', 'gender': 'L', 'tahun': 2022},
    {'nip': 'ART201-76237', 'nama': 'Siti Jasmine', 'hp': '081377778888', 'gender': 'K', 'tahun': 2020},
    {'nip': 'ART222-94263', 'nama': 'Alya Lestari', 'hp': '085260607070', 'gender': 'K', 'tahun': 2022},
    {'nip': 'ART241-83266', 'nama': 'Nur Dewi', 'hp': '083849495858', 'gender': 'K', 'tahun': 2024},
    {'nip': 'ART251-45868', 'nama': 'Fatimah Indah', 'hp': '081920203030', 'gender': 'K', 'tahun': 2025},
    {'nip': 'ART211-93432', 'nama': 'Salma Puspita', 'hp': '087711223344', 'gender': 'K', 'tahun': 2021},
]

print("Memulai pembuatan data Santri dan User...")
with transaction.atomic():
    for data in SANTRI_DATA:
        # Pisahkan Nama Depan dan Belakang
        nama_parts = data['nama'].split()
        first_name = nama_parts[0]
        last_name = ' '.join(nama_parts[1:]) if len(nama_parts) > 1 else ''
        
        # 1. Buat Akun User (auth_user)
        user = User.objects.create_user(
            username=data['nip'],
            password='admin@1234',  # Ganti dengan password yang lebih kuat
            first_name=first_name,
            last_name=last_name,
            email=f"{first_name.lower()}.{last_name.lower().replace(' ', '')}@hsi.id"
        )

        # 2. Buat Objek Santri (evaluasi_santri) dan Hubungkan ke User
        Santri.objects.create(
            
            user=user,  # Relasi OneToOneField terisi
            hp=data['hp'],
            gender=data['gender'],
            tgl_lahir='1999-09-09', # Default tanggal lahir
            tahun_penerimaan=data['tahun']
        )
        print(f"✅ Data {data['user']} ({data['nama']}) berhasil dibuat dan terhubung.")

print("Semua data dummy berhasil diimpor.")
exit()