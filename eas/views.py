from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from evaluasi.models import Nilai,Santri
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    context = {
        'page_title' : 'Beranda EAS',
        'page_text' : 'Ahlan wa Sahlan'
    }

    return render(request, 'home.html', context)

@login_required #decorator
def logoutView(request):
    context = {
        'page_title' : 'Homepage',
        'page_text' : 'Ahlan wa Sahlan'
    }

    logout(request)
        
    return render(request, 'home.html', context)


def loginView(request):
    context = {
        'page_title' : 'Login Page',
        'page_text' : 'Silahkan Masukkan Username dan Password untuk login'
    }

    user = None

    if request.method == "GET":
        if request.user.is_authenticated:
            # cek apakah sdh login
            user_info = request.user 
            # nip_santri = user_info.username

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
            try:
                statEva = Nilai.objects.filter(santri=santri_obj).exists()
            except:
                statEva = False    
            # end

            context = {
                "page_title":"Halaman Utama Evaluasi",
                "page_text":"Ahlan wa sahlan ",
                "statEva":statEva}
            return render(request, 'index.html', context)
        else:
            return render(request, 'login.html', context)
		
    if request.method == "POST":
        username_login = request.POST['username']
        username_password = request.POST['password']
        user = authenticate(request, username=username_login, password=username_password)
              
        
        if user is not None:
            login(request, user)
            # cek apakah sdh evaluasi
            try:
                santri_profile=Santri.objects.get(user=user)
                statEva = Nilai.objects.filter(santri=santri_profile).exists()
            except Santri.DoesNotExist:
                statEva = False

            user_info = User.objects.get(username=username_login)
            context = {
                "page_title":"Halaman Utama Evaluasi",
                "page_text":"Ahlan wa sahlan ",
                "nip":username_login,
                "first_name": user_info.first_name,
                "last_name": user_info.last_name,
                "email":user_info.email,
                "statEva":statEva
                }
            # "page_text":"Selamat Datang " + username_login + " - " +  + " " +  + " " + ,
            return render(request, 'index.html', context)
        else:
            return redirect('login')
    	
    return render(request, 'login.html', context)

