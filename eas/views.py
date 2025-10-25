from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def home(request):
    context = {
        'page_title' : 'Beranda EAS',
        'page_text' : 'Ahlan wa Sahlan'
    }

    return render(request, 'home.html', context)

@login_required
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
            
            context = {
                "page_title":"Halaman Utama Evaluasi",
                "page_text":"Ahlan wa sahlan "}
            return render(request, 'index.html', context)
        else:
            return render(request, 'login.html', context)
		
    if request.method == "POST":
        username_login = request.POST['username']
        username_password = request.POST['password']
        user = authenticate(request, username=username_login, password=username_password)
        # print(f"hwooo {request}")
        # print(f"nip => {username_login}")
        # print(f"user => {user}")
        if user is not None:
            login(request, user)
            user_info = User.objects.get(username=username_login)
            context = {
                "page_title":"Halaman Utama Evaluasi",
                "page_text":"Ahlan wa sahlan ",
                "nip":username_login,
                "first_name": user_info.first_name,
                "last_name": user_info.last_name,
                "email":user_info.email
                }
            # "page_text":"Selamat Datang " + username_login + " - " +  + " " +  + " " + ,
            return render(request, 'index.html', context)
        else:
            return redirect('login')
    	
    return render(request, 'login.html', context)

