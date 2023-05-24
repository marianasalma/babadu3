import datetime
from django.db import connection
from django.shortcuts import redirect, render

# Create your views here.


def show_dashboard_atlet(request):

    try:
        # request.session['nama']
        request.session['email']
    except KeyError:
        return redirect("../../login")

    with connection.cursor() as cursor:

        email_user = request.session["email"]
        print(email_user)
        id_atlet = "69340675-1776-4491-8a8f-24aa617a4542"
        sql = "SELECT * FROM ATLET WHERE id='"+id_atlet+"'"
        cursor.execute(sql)  # ambil atlet
        atlet = cursor.fetchall()
        print(atlet)

        sql = "SELECT * FROM MEMBER WHERE id='"+id_atlet+"'"
        cursor.execute(sql)  # ambil member
        member = cursor.fetchall()
        print(member)

        sql = "SELECT EXISTS (SELECT 1 FROM atlet_kualifikasi WHERE id_atlet = '"+id_atlet+"');"
        cursor.execute(sql)  # ambil status
        status = cursor.fetchall()
        print(status)

        context = {
            'nama': member[0][1],
            'negara': atlet[0][2],
            'email': member[0][2],
            'tgl_lahir': datetime.date.strftime(atlet[0][1], "%d/%m/%Y"),
            'play': right_or_left(atlet[0][3]),
            'tinggi_badan': atlet[0][4],
            'world_rank': atlet[0][5],
        }

    return render(request, "dashboard_atlet.html", context)


def show_dashboard_pelatih(request):
    return render(request, "dashboard_pelatih.html")


def show_dashboard_umpire(request):
    return render(request, "dashboard_umpire.html")


def right_or_left(boolean):
    if boolean:
        return "Right Hand"
    else:
        return "Left Hand"
