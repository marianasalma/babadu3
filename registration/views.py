from django.shortcuts import render
from django.db import connection
from collections import namedtuple
import uuid
from django.http import HttpResponseRedirect
from django.urls import reverse

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def get_query(str):
    '''Execute SQL query and return its result as a list'''
    cursor = connection.cursor()
    result = []
    try:
        cursor.execute(str)
        result = namedtuplefetchall(cursor)
    except Exception as e:
        result = e
    finally:
        cursor.close()
        return result
    
def generate_uuid():
    id = uuid.uuid4()
    if get_query(f"SELECT * FROM MEMBER WHERE id = '{id}';") != []:
        return generate_uuid()
    else:
        return id

# Create your views here.
def show_registration(request):
    data = get_query("SELECT * FROM MEMBER;")
    if type(data) == list and len(data) != 0:
        print("data", data)
    return render(request, "registration.html")

def show_registration_atlet(request):
    if request.method == "POST":
        id = generate_uuid()
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        lahir = request.POST.get('lahir')
        play = bool(request.POST.get('play'))
        tinggi = int(request.POST.get('tinggi'))
        sex = bool(request.POST.get('sex'))

        print(id, nama, email, negara, lahir, play, tinggi, sex)

        # INSERT TO MEMBER
        print("MEMBER :")
        get_query(f"INSERT INTO MEMBER VALUES ('{id}', '{nama}', '{email}');")
        print(get_query(f"SELECT * FROM MEMBER WHERE id = '{id}';"))

        if get_query(f"SELECT * FROM MEMBER WHERE id = '{id}';") != []:
            print("uploaded!")
        else :
            print("unsuccesful")

        # INSERT TO ATLET
        print("ATLET :")
        if get_query(f"SELECT * FROM MEMBER WHERE id = '{id}';") != []:
            get_query(f"INSERT INTO ATLET VALUES ('{id}', '{lahir}', '{negara}', '{play}', '{tinggi}', NULL, '{sex}');")
        print(get_query(f"SELECT * FROM ATLET WHERE id = '{id}';"))

        if get_query(f"SELECT * FROM ATLET WHERE id = '{id}';") != []:
            print("uploaded!")
        else :
            print("unsuccesful")

        # INSERT TO ATLET_NONKUALIFIKASI
        print("ATLET_NONKUALIFIKASI :")
        if get_query(f"SELECT * FROM MEMBER WHERE id = '{id}';") != []:
            get_query(f"INSERT INTO ATLET_NONKUALIFIKASI VALUES ('{id}');")
        print(get_query(f"SELECT * FROM ATLET WHERE id = '{id}';"))

        if get_query(f"SELECT * FROM ATLET_NONKUALIFIKASI WHERE id = '{id}';") != []:
            print("uploaded!")
        else :
            print("unsuccesful")
            
        return HttpResponseRedirect(reverse('dashboard:dash_atlet'))
    else:
        return render(request, "registration_atlet.html")

def show_registration_pelatih(request):
    if request.method == "POST":
        id = generate_uuid()
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        mulai = request.POST.get('mulai')
        kategori = request.POST.get('kategori')

        print(id, nama, email, negara, mulai, kategori)

        # INSERT TO MEMBER
        print("MEMBER :")
        get_query(f"INSERT INTO MEMBER VALUES ('{id}', '{nama}', '{email}');")
        print(get_query(f"SELECT * FROM MEMBER WHERE id = '{id}';"))

        if get_query(f"SELECT * FROM MEMBER WHERE id = '{id}';") != []:
            print("uploaded!")
        else :
            print("unsuccesful")

        # INSERT TO PELATIH
        print("PELATIH :")
        get_query(f"INSERT INTO PELATIH VALUES ('{id}', '{mulai}');")
        print(get_query(f"SELECT * FROM PELATIH WHERE id = '{id}';"))

        if get_query(f"SELECT * FROM PELATIH WHERE id = '{id}';") != []:
            print("uploaded!")
        else :
            print("unsuccesful")

        # INSERT TO PELATIH_SPESIALISASI
        kat_id = get_query(f"SELECT id FROM SPESIALISASI WHERE spesialisasi = '{kategori}';")[0].id

        print("PELATIH_SPESIALISASI :")
        get_query(f"INSERT INTO PELATIH_SPESIALISASI VALUES ('{id}', '{kat_id}');")
        print(get_query(f"SELECT * FROM PELATIH_SPESIALISASI WHERE id_pelatih = '{id}';"))

        if get_query(f"SELECT * FROM PELATIH_SPESIALISASI WHERE id_pelatih = '{id}';") != []:
            print("uploaded!")
        else :
            print("unsuccesful")

        return HttpResponseRedirect(reverse('dashboard:dash_pelatih'))
    else:
        return render(request, "registration_pelatih.html")

def show_registration_umpire(request):
    if request.method == "POST":
        id = generate_uuid()
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        negara = request.POST.get('negara')

        print(id, nama, email, negara)

        # INSERT TO MEMBER
        print("MEMBER :")
        get_query(f"INSERT INTO MEMBER VALUES ('{id}', '{nama}', '{email}');")
        print(get_query(f"SELECT * FROM MEMBER WHERE id = '{id}';"))

        if get_query(f"SELECT * FROM MEMBER WHERE id = '{id}';") != []:
            print("uploaded!")
        else :
            print("unsuccesful")

        # INSERT TO UMPIRE
        print("PELATIH :")
        get_query(f"INSERT INTO UMPIRE VALUES ('{id}', '{negara}');")
        print(get_query(f"SELECT * FROM UMPIRE WHERE id = '{id}';"))

        if get_query(f"SELECT * FROM UMPIRE WHERE id = '{id}';") != []:
            print("uploaded!")
        else :
            print("unsuccesful")

        return HttpResponseRedirect(reverse('dashboard:dash_umpire'))
    else:
        return render(request, "registration_umpire.html")