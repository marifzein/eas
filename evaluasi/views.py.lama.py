from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Soal,Evaluasi,Nilai,Santri
from .forms import FormEvaluasi
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# soals = Soal()

# def get_soal():
#     global soals
#     soals = Soal.objects.prefetch_related("pilihan").order_by("?")[:4]
#     print(f"waiki soals => {soals}")
    
@login_required
def evaluasi_view(request):
    # nip_santri = request.user.username
    # user_info = User.objects.get(username=nip_santri)
    # santri_obj = Santri.objects.get(user=user_info.username)

    user_info = request.user 
    nip_santri = user_info.username
    santri_obj=user_info.santri
    
    try:
        # Ambil objek Santri yang terhubung dengan user yang sedang login (TIDAK ADA LAGI ERROR NIP!)
        santri_obj = user_info.santri 
    except ObjectDoesNotExist:
        return render(request, 'error_page.html', {'message': 'Data Santri Anda tidak ditemukan. Hubungi admin.'})
    


    
    # print(request.method)
    #soals = Soal()

    if request.method == "POST":
        # print(request.POST)
        
        # <QueryDict: {'csrfmiddlewaretoken': ['AFvg7P3m99AXrvhtAIepqTCtM0qGC3iXiiY2GiHgajjEKLYBoy2LsfsGswUY4j46'], 
        # 'soal_1': ['b'], 'soal_6': ['b'], 'soal_7': ['b'], 
        # 'soal_8': ['a']}>
        form = FormEvaluasi(soals, request.POST)
        if form.is_valid():
            # print(soals[0].id)
            
            hasil = {}
            nilai = 0
            total = soals.count()*2
            # print(soals.count())
            # Ambil objek Santri berdasarkan NIP
            # santri_obj = Santri.objects.get(nip=nip_santri)
            

            for soal in soals:
                field_name = f"soal_{soal.id}"
                jawaban_user = form.cleaned_data[field_name]
                benar = jawaban_user == soal.jawaban_benar
                if benar:
                    nilai = nilai + 2

                hasil[soal.id] = {
                    "pertanyaan": soal.pertanyaan,
                    "jawaban_user": jawaban_user,
                    "jawaban_benar": soal.jawaban_benar,
                    "benar": benar
                }

                # Insert data ke Evaluasi
                soal_obj=Soal.objects.get(id=soal.id)
                Evaluasi.objects.create(santri=santri_obj,
                                        soal=soal_obj,
                                        jawaban_santri=jawaban_user)

            # Insert data ke nilai
            Nilai.objects.create(santri=santri_obj,
                                 nilai=(nilai/total)*100)


            context = {
                "form": form,
                "hasil": hasil,
                "skor": (nilai/total)*100,
                "attr_submit":"disabled"
            }
            return render(request, "evaluasi.html", context)
        else:
            print(form.errors.as_json())
            print(request.POST)
    else:#method=GET
        print(request)
        # cek apakah santri sudah mengerjakan
        # nilai_record = None
        # santri_obj = Santri.objects.get(nip=nip_santri)
        stat="disabled"
        sudah_ujian = Nilai.objects.filter(santri=santri_obj).exists()

        if sudah_ujian:
            # atribut button submit disabled
            stat="disabled"
            is_disabled = True # <-- Tentukan state disable form
            initial_data={}
            # 1. Ambil data Evaluasi dan simpan (Gunakan select_related untuk efisiensi)
            evaluasi_data = Evaluasi.objects.filter(santri=santri_obj).select_related('soal').order_by('soal__id')
            # dapatkan soal id dan jawaban dari evaluasi yg sdh dikerjakan
            soal_ids = [item.soal_id for item in evaluasi_data]
            #buat queryset di Soal berdasarkan soal id dari Evaluasi
            soals=Soal.objects.filter(id__in=soal_ids).prefetch_related("pilihan").order_by('id')
            #membuat initial_data =jawaban santri
            for item in evaluasi_data:
                field_name = f"soal_{item.soal_id}"
                initial_data[field_name] = item.jawaban_santri

            #membuat data tampilan hasil-----start
            # for soal in soals:
            #     field_name = f"soal_{soal.id}"
            #     jawaban_user = form.cleaned_data[field_name]
            #     benar = jawaban_user == soal.jawaban_benar
            #     if benar:
            #         nilai = nilai + 2

            #     hasil[soal.id] = {
            #         "pertanyaan": soal.pertanyaan,
            #         "jawaban_user": jawaban_user,
            #         "jawaban_benar": soal.jawaban_benar,
            #         "benar": benar
            #     }
            hasil = {}

            for evl in evaluasi_data:
                soal=evl.soal
                # .prefetch_related("pilihan")
                benar = evl.jawaban_santri == soal.jawaban_benar
                hasil[soal.id] = {
                "pertanyaan": soal.pertanyaan,
                "jawaban_user": evl.jawaban_santri,
                "jawaban_benar": soal.jawaban_benar,
                "benar": benar
                }
            #membuat data tampilan hasil----end

                # "form": form,"skor": (nilai/total)*100,
            # mengambil skor dari class Nilai
            skor_record=Nilai.objects.filter(santri=santri_obj).first()
            skor=skor_record.nilai

            form = FormEvaluasi(soals,initial=initial_data)
            context = {"form": form ,
                    "hasil": hasil,
                    "skor": skor,
                    "attr_submit":stat
                    }
            
        else:
            # print(f"nilai record = {nilai_record}")
            stat=""

            get_soal()
            form = FormEvaluasi(soals)
            context = {"form": form ,
                    "nip":nip_santri,
                    "first_name":user_info.first_name,
                    "last_name":user_info.last_name,
                    "attr_submit":stat
                    }
            
        return render(request, "evaluasi.html", context)

def peringkat_view(request):
    ranking_evaluasi=Nilai.objects.all().values().prefetch_related("nilai_santri").order_by("nilai")
    print(ranking_evaluasi)
    context={
        "Title":"Peringkat Evaluasi",
        "Header":"Peringkat Evaluasi",
        "ranking":ranking_evaluasi
    }
    return render(request,'peringkat.html',context)

