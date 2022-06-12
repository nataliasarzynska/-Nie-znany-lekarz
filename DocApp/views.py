from unittest import result
from django.shortcuts import render, redirect
from django.http import HttpResponse
from DocApp.models import NewAppointment
from .models import NewAppointment, Doctor, NewReview
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg
import csv


# Create your views here.

def index(request):
    return render(request, 'index.html');

def twojprofil(request):
    current_user = request.user.username 
    return render(request, 'twojprofil.html', {"current_user":current_user});

def base(request):
    return render(request, 'base.html');

def wykresrecenzji(request):
    return render(request, 'wykresrecenzji.html');

def umowwizyte(request):
    docs = Doctor.objects.all()
    return render(request, 'umowwizyte.html', {'docs': docs});

def szukajlekarzy(request):
    docs = Doctor.objects.all()
    if request.method == 'POST':
        i = request.POST["i"]
    else:
        i=1
    avg = NewReview.objects.filter(doctor = i).aggregate(Avg('rate'))

    for k, v in avg.items():
        avg[k] = round(v, 2)
    return render(request, 'szukajlekarzy.html', {'docs': docs, 'avg': avg})

def wizyta(request):

    if request.method == 'POST':

        current_doc_name = request.POST["doctor"]

        app = NewAppointment() 
        app.user = request.user
        app.doctor = Doctor.objects.get(id = current_doc_name)
        app.date = request.POST["date"]
        app.time = request.POST["time"]
        app.save()

        return render(request, 'wizyta.html', {"app":app})
    else:
        return render(request, 'wizyta.html')

def twojewizyty(request):
    current_user = request.user.id 
    wizyty = NewAppointment.objects.filter(user = current_user)
    return render(request, 'twojewizyty.html', {"wizyty":wizyty} );

current_doc_name = ''


def recenzje(request):
    if request.method == 'POST':

        global current_doc_name
        current_doc_name = request.POST["doctor"]

        review = NewReview()
        review.user = request.user
        review.doctor = Doctor.objects.get(id = current_doc_name)
        review.rate = request.POST["rate"]
        review.comment = request.POST["comment"]
        review.save()
        

        return render(request, 'recenzje.html', {'review': review})
    else:
        return render(request, 'recenzje.html')

def twojerecenzje(request):
    current_doc_name = request.GET["doctor"]
    current_user = request.user.id 
    doctor_id = Doctor.objects.get(id = current_doc_name)
    reviews = NewReview.objects.filter(doctor = doctor_id)
    return render(request, 'twojerecenzje.html', {"reviews":reviews} )

def dodajrecenzje(request):
    docs = Doctor.objects.all()
    return render(request, 'dodajrecenzje.html', {'docs': docs});

def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Nazwa użytkownika jest zajęta')
            return redirect('register');

        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Konto o podanym adresie email już istnieje')
            return redirect('register');

        else:
            user = User.objects.create_user(username = username, first_name = first_name, last_name = last_name, email = email, password = password)
            user.save();

        return redirect('login');

    else:
        return render(request, 'register.html');

def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect("twojprofil")
        else:
            messages.info(request,'Błędna nazwa użytkownika lub hasło')
            return redirect('login')

    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect("/")


def get_chart_data(request):
    labels = []
    data = []

    queryset = Doctor.objects.values('name')
    for entry in queryset:
        labels.append(entry['name'])
        id_doc = Doctor.objects.get(name = entry['name'])
        x = NewReview.objects.filter(doctor = id_doc).aggregate(Avg('rate'))
        data.append(x['rate__avg'])
        
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def wykresrecenzji(request):
    labels = []
    data = []

    queryset = Doctor.objects.values('name')
    for entry in queryset:
        labels.append(entry['name'])
        id_doc = Doctor.objects.get(name = entry['name'])
        x = NewReview.objects.filter(doctor = id_doc).aggregate(Avg('rate'))
        data.append(x['rate__avg'])
    return render(request, 'wykresrecenzji.html', {'labels': labels, 'data': data})

def save_to_csv(request):
    response = HttpResponse(
        content_type = 'text/csv',
        headers = {'Content-Disposition': 'attachment; filename="wizyty.csv"'},
        )

    writer = csv.writer(response)
    current_user = request.user.id 
    wizyty = NewAppointment.objects.filter(user = current_user)
    for wizyta in wizyty:
        writer.writerow([wizyta.doctor.name, wizyta.date, wizyta.time])
    
    return response