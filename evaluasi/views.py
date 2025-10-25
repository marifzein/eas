from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Soal,Evaluasi,Nilai,Santri
from .forms import FormEvaluasi
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist



@login_required
def evaluasi_view(request):
    user_info = request.user 
    nip_santri = user_info.username

    try:
        # Ambil objek Santri yang sedang login
        user_info = request.user
        santri_obj = Santri.objects.get(user=user_info)
        # santri_obj = user_info.santri 
        # print(f"santri obj => {santri_obj}")
    except ObjectDoesNotExist:
        # Jika relasi Santri belum dibuat untuk user ini
        return render(request, 'error_page.html', {'message': 'Data Santri Anda tidak ditemukan. Hubungi admin.'})

    # Cek apakah santri sudah mengerjakan
    sudah_ujian = Nilai.objects.filter(santri=santri_obj).exists()
    
    # Inisialisasi variabel
    context = {}

    if request.method == "POST":
        #MENGAMBIL SOAL BERDASARKAN ID YANG DIKIRIM OLEH FORM
        
        # 1. Ekstrak Soal ID dari request.POST
        soal_ids = []
        for key in request.POST.keys():
            if key.startswith('soal_'):
                try:
                    # Ambil ID integer setelah 'soal_'
                    soal_id = int(key.split('_')[1])
                    #bikin tuple soal_ids
                    soal_ids.append(soal_id)
                except ValueError:
                    continue
        
        # 2. Ambil QuerySet Soal berdasarkan ID yang dikirim
        if not soal_ids:
            # Jika form kosong, kembali ke halaman evaluasi GET
            return render(request, "evaluasi.html", {'message': 'Formulir kosong. Silakan coba lagi.'})
            
        # QuerySet Soal yang sedang dievaluasi
        soals_post = Soal.objects.filter(id__in=soal_ids).prefetch_related("pilihan") 

        # 3. Instantiate FormEvaluasi dengan QuerySet Soal yang benar dan data POST
        form = FormEvaluasi(soals_post, request.POST)
        
        if form.is_valid(): 
            
            hasil = {}
            nilai = 0
            total = soals_post.count() * 2 # Gunakan soals_post untuk total
            
            # 4. Save data dan hitung nilai
            for soalnya in soals_post:
                field_name = f"soal_{soalnya.id}"
                jawaban_user = form.cleaned_data[field_name]
                benar = jawaban_user == soalnya.jawaban_benar
                if benar:
                    nilai = nilai + 2

                hasil[soalnya.id] = {
                    "pertanyaan": soalnya.pertanyaan,
                    "jawaban_user": jawaban_user,
                    "jawaban_benar": soalnya.jawaban_benar,
                    "benar": benar
                }

                # Insert data ke Evaluasi
                Evaluasi.objects.create(santri=santri_obj,
                                        soal=soalnya, # Gunakan objek 'soalnya' langsung
                                        jawaban_santri=jawaban_user)

            # Insert data ke Nilai
            skor_akhir = (nilai/total)*100
            Nilai.objects.create(santri=santri_obj, nilai=skor_akhir)

            # Siapkan konteks hasil untuk render
            context = {
                "form": form,
                "hasil": hasil,
                "skor": skor_akhir,
                "attr_submit":"disabled"
            }
            return render(request, "evaluasi.html", context)
        else:
            # Jika form tidak valid (misal ada field kosong), render form yang gagal agar error terlihat
            context = {
                "form": form, # Form yang mengandung error
                "nip": nip_santri,
                "first_name": user_info.first_name,
                "last_name": user_info.last_name,
                "attr_submit": "" 
            }
            return render(request, "evaluasi.html", context) # Return di sini

    # METHOD = GET
    if sudah_ujian:
        stat="disabled"
        
        # 1. Ambil data Evaluasi
        evaluasi_data = Evaluasi.objects.filter(santri=santri_obj).select_related('soal').order_by('soal__id')
        #bikin tuple soal_id
        soal_ids = [item.soal_id for item in evaluasi_data]
        # 2. ambil queryset Soal beserta pilihan jawabn urut id soal
        soals=Soal.objects.filter(id__in=soal_ids).prefetch_related("pilihan").order_by('id')
        
        # 3. Membuat initial_data, otomatis akan ngeset radio pilihan jawaban checked
        initial_data={}
        for item in evaluasi_data:
            field_name = f"soal_{item.soal_id}"
            initial_data[field_name] = item.jawaban_santri

        # 4. Membuat data tampilan hasil
        hasil = {}
        for evl in evaluasi_data:
            soal=evl.soal
            benar = evl.jawaban_santri == soal.jawaban_benar
            hasil[soal.id] = {
            "pertanyaan": soal.pertanyaan,
            "jawaban_user": evl.jawaban_santri,
            "jawaban_benar": soal.jawaban_benar,
            "benar": benar
            }
        
        # 5. Ambil skor berdsarkan santri_obj (PK)
        skor_record=Nilai.objects.filter(santri=santri_obj).first()
        skor=skor_record.nilai

        form = FormEvaluasi(soals,initial=initial_data)
        context = {"form": form ,
                "hasil": hasil,
                "skor": skor,
                "attr_submit":stat
                }
        
    else:
        # Jika BELUM ujian, definisikan soals (LOKAL) dengan 4 soal baru
        soals = Soal.objects.prefetch_related("pilihan").order_by("?")[:4]
        stat=""

        form = FormEvaluasi(soals)
        context = {"form": form ,
                "nip":nip_santri,
                "first_name":user_info.first_name,
                "last_name":user_info.last_name,
                "attr_submit":stat
                }
        
    return render(request, "evaluasi.html", context)


# PERINGKAT VIEW (Sudah di-fix untuk relasi User/Santri)
@login_required
def peringkat_view(request):
    # mengambil queryset model Nilai beserta santri dan user (spy nama bisa tampil) order desc
    ranking_evaluasi=Nilai.objects.all().select_related("santri__user").order_by("-nilai")
    
    rank_list = []
    for rank in ranking_evaluasi:
        rank_list.append({
            'nip': rank.santri.user.username,
            'nama': f"{rank.santri.user.first_name} {rank.santri.user.last_name}",
            'nilai': rank.nilai
        })
    # print(f"rank lst => {rank_list} ")    
    context={
        "Title":"Peringkat Evaluasi",
        "Header":"Peringkat Evaluasi",
        "ranking":rank_list
    }
    return render(request,'peringkat.html',context)