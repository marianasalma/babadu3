from django.shortcuts import render
from django.db import connection
from collections import namedtuple
import uuid
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

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
        get_query(f"SELECT * FROM MEMBER;")

        # INSERT TO MEMBER
        print("MEMBER :")
        get_query(f"INSERT INTO MEMBER VALUES ('{id}', '{nama}', '{email}')")
        print(get_query(f"SELECT * FROM MEMBER WHERE id = '{id}';"))

        if get_query(f"SELECT * FROM MEMBER WHERE id = '{id}';") != []:
            get_query(f"DELETE FROM MEMBER WHERE id = '{id}';")
            print("uploaded & deleted!")
        else :
            print("unsuccesful")

        # INSERT TO ATLET
        print("ATLET :")
        print(get_query("SELECT * FROM ATLET WHERE id = 'b6a2f602-d7fc-4e6b-8d20-c60b79bef849'"))
        get_query(f"INSERT INTO ATLET VALUES ('{id}', {lahir}, '{negara}', {play}, {tinggi}, '', {sex})")
        print(get_query(f"SELECT * FROM ATLET WHERE id = '{id}';"))

        if get_query(f"SELECT * FROM ATLET WHERE id = '{id}';") != []:
            get_query(f"DELETE FROM ATLET WHERE id = '{id}';")
            print("uploaded & deleted!")
        else :
            print("unsuccesful")
        return HttpResponseRedirect(reverse('registration:reg_atlet'))
    else:
        return render(request, "registration_atlet.html")
    
def show_registration_pelatih(request):
    return render(request, "registration_pelatih.html")

def show_registration_umpire(request):
    return render(request, "registration_umpire.html")