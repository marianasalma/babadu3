import datetime
from django.shortcuts import redirect, render
from django.db import connection
from django.http import JsonResponse
import json
# Create your views here.


def form_kualifikasi(request):
    return render(request, "form_kualifikasi.html")


def pertanyaan_kualifikasi(request):
    return render(request, "pertanyaan_kualifikasi.html")


def pilih_stadium(request):
    return render(request, "pilih_stadium.html")


def pilih_event(request):
    return render(request, "pilih_event.html")


def pilih_kategori(request):
    return render(request, "pilih_kategori.html")


def daftar_atlet(request):
    return render(request, "daftar_atlet.html")


def list_atlet(request):
    return render(request, "list_atlet.html")


def daftar_sponsor(request):
    email = request.session['email']  # ini ambil emailnya
    if email == None:
        return redirect("../../login")

    print(email)
    id_atlet = get_id_from_email(email)
    with connection.cursor() as cursor:
        cursor.execute("SELECT sponsor.id, sponsor.nama_brand FROM sponsor WHERE sponsor.id NOT IN (SELECT atlet_sponsor.id_sponsor FROM atlet_sponsor WHERE atlet_sponsor.id_atlet = '" + str(id_atlet) + "')")  # ambil row sponsor
        sponsors = cursor.fetchall()

        list_sponsors = []

        for data in sponsors:
            dic = {"id": data[0], "brand": data[1]}
            list_sponsors.append(dic)

        context = {
            'list_sponsors': list_sponsors
        }

    if request.method == "POST":
        id_sponsor = request.POST.get('dropdown')
        # print(id_sponsor)

        tgl_mulai_str = request.POST.get('tgl_mulai')  # format dd/mm/yy
        tgl_mulai = convert_date_string(tgl_mulai_str)

        tgl_selesai_str = request.POST.get('tgl_selesai')  # format dd/mm/yy
        tgl_selesai = convert_date_string(tgl_selesai_str)

        print(tgl_mulai)
        print(tgl_selesai)

        # with connection.cursor() as cursor:

        #     # Prepare the SQL query with the date value
        #     sql = "INSERT INTO ATLET_SPONSOR (id_atlet, id_sponsor, tgl_mulai, tgl_selesai) VALUES (%s,%s,%s,%s)"

        #     # Execute the SQL query
        #     cursor.execute(sql, (id_atlet,id_sponsor,tgl_mulai,tgl_selesai))

    return render(request, "daftar_sponsor.html", context)


def enrolled_event(request):
    return render(request, "enrolled_event.html")


def list_event(request):
    return render(request, "list_event.html")


########
def get_all_sponsor(request):
    email = request.session['email']  # ini ambil emailnya
    if email == None:
        return redirect("../../login")

    id_atlet = get_id_from_email(email)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM atlet_sponsor WHERE id_atlet = '" +
                       str(id_atlet)+"'")
        sponsorships = cursor.fetchall()
        list_sponsors = []

        for i in sponsorships:
            id_sponsor = i[1]
            cursor.execute("SELECT nama_brand FROM sponsor WHERE id = '" +
                           str(id_sponsor) + "'")  # ambil nama sponsor
            nama_sponsor = cursor.fetchone()
            tgl_mulai_sponsor = i[2].strftime("%m/%d/%Y")
            tgl_selesai_sponsor = i[3].strftime("%m/%d/%Y")
            dic = {
                "brand": nama_sponsor[0], "tgl_mulai": tgl_mulai_sponsor, "tgl_selesai": tgl_selesai_sponsor}
            list_sponsors.append(dic)
        print(list_sponsors)

        context = {
            'list_sponsors': list_sponsors
        }

        return render(request, "list_sponsor.html", context)


def convert_date_string(date_string):
    try:
        # Convert the string to a datetime object
        datetime_obj = datetime.strptime(date_string, "%d/%m/%y")

        # Extract the integer values for day, month, and year
        day = datetime_obj.day
        month = datetime_obj.month
        year = datetime_obj.year

        # Create a date object from the extracted values
        date_obj = datetime.date(year, month, day)

        return date_obj
    except ValueError:
        return None  # Invalid date string


def get_id_from_email(email):

    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM member WHERE email = '" +
                       email+"'")  # ambil row sponsor
        get_id = cursor.fetchone()
        return get_id[0]
