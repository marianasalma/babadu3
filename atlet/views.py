from datetime import datetime
from datetime import date
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
        print(id_sponsor)

        tgl_mulai_str = request.POST.get('tgl_mulai')  # format dd/mm/yy
        tgl_mulai = convert_date_string(tgl_mulai_str)

        tgl_selesai_str = request.POST.get('tgl_selesai')  # format dd/mm/yy
        tgl_selesai = convert_date_string(tgl_selesai_str)

        print(tgl_mulai)
        print(tgl_selesai)

        with connection.cursor() as cursor:

            # Prepare the SQL query with the date value
            sql = "INSERT INTO ATLET_SPONSOR (id_atlet, id_sponsor, tgl_mulai, tgl_selesai) VALUES (%s,%s,%s,%s)"

            # Execute the SQL query
            cursor.execute(sql, (str(id_atlet), str(
                id_sponsor), tgl_mulai, tgl_selesai))

    return render(request, "daftar_sponsor.html", context)


def enrolled_event(request):
    email = request.session['email']  # ini ambil emailnya
    if email == None:
        return redirect("../../login")
    id_atlet = get_id_from_email(email)

    with connection.cursor() as cursor:
        # If not logged in
        cursor.execute("SELECT EXISTS ( SELECT id_atlet FROM atlet_kualifikasi WHERE id_atlet = '" +
                       str(id_atlet)+"');")
        isQualified = cursor.fetchone()
        print(isQualified)
        if not isQualified[0]:
            return render(request, "not_qualified.html")
        sql = """select distinct 
                PME.Nomor_Peserta,
                E.Nama_Event,
                E.Tahun,
                S.Nama AS Stadium,
                E.Kategori_Superseries,
                E.Tgl_Mulai,
                E.Tgl_Selesai
                from
                PARTAI_PESERTA_KOMPETISI PPK,
                PESERTA_MENDAFTAR_EVENT PME
                JOIN PESERTA_KOMPETISI PK ON PME.Nomor_Peserta = PK.Nomor_Peserta
                JOIN EVENT E ON PME.Nama_Event = E.Nama_Event AND PME.Tahun = E.Tahun
                JOIN STADIUM S ON E.Nama_Stadium = S.Nama
                JOIN ATLET_GANDA AG ON PK.ID_Atlet_Ganda = AG.ID_Atlet_Ganda
                JOIN ATLET_KUALIFIKASI AK ON AG.ID_Atlet_Kualifikasi = AK.ID_Atlet OR AG.ID_Atlet_Kualifikasi_2 = AK.ID_Atlet
                WHERE
                AK.ID_Atlet = '{id}'
                """.format(id=str(id_atlet))
        cursor.execute(sql)
        list_enrolled_tuples = cursor.fetchall()
        print(list_enrolled_tuples)

        list_enrolled = []

        for i in list_enrolled_tuples:
            tgl_mulai_event = i[5].strftime("%d %b %Y")
            tgl_selesai_event = i[6].strftime("%d %b %Y")

            dic = {
                "id_atlet": str(id_atlet),
                "nama_event": i[1],
                "tahun": str(i[2]),
                "stadium": i[3],
                "kategori": i[4],
                "tgl_mulai": tgl_mulai_event,
                "tgl_selesai": tgl_selesai_event
            }
            list_enrolled.append(dic)

        print(list_enrolled)

        context = {
            'list_enrolled': list_enrolled
        }

    if request.method == "POST":
        event_unenroll = request.POST.get('unenroll')
        event_name = event_unenroll[:-5]
        tahun_event = event_unenroll[-4:]
        print(event_name+" "+tahun_event)

    return render(request, "enrolled_event.html", context)


def list_event(request):
    return render(request, "list_event.html")


def enrolled_partai_event(request):
    email = request.session['email']  # ini ambil emailnya
    if email == None:
        return redirect("../../login")
    id_atlet = get_id_from_email(email)
    with connection.cursor() as cursor:
        cursor.execute("SELECT EXISTS ( SELECT id_atlet FROM atlet_kualifikasi WHERE id_atlet = '" +
                       str(id_atlet)+"');")
        isQualified = cursor.fetchone()
        print(isQualified)
        if not isQualified[0]:
            return render(request, "not_qualified.html")

        sql = """select distinct 
                PME.Nomor_Peserta,
                E.Nama_Event,
                E.Tahun,
                S.Nama AS Stadium,
                PPK.Jenis_Partai,
                E.Kategori_Superseries,
                E.Tgl_Mulai,
                E.Tgl_Selesai
                from
                PARTAI_PESERTA_KOMPETISI PPK,
                PESERTA_MENDAFTAR_EVENT PME
                JOIN PESERTA_KOMPETISI PK ON PME.Nomor_Peserta = PK.Nomor_Peserta
                JOIN EVENT E ON PME.Nama_Event = E.Nama_Event AND PME.Tahun = E.Tahun
                JOIN STADIUM S ON E.Nama_Stadium = S.Nama
                JOIN ATLET_GANDA AG ON PK.ID_Atlet_Ganda = AG.ID_Atlet_Ganda
                JOIN ATLET_KUALIFIKASI AK ON AG.ID_Atlet_Kualifikasi = AK.ID_Atlet OR AG.ID_Atlet_Kualifikasi_2 = AK.ID_Atlet
                WHERE
                AK.ID_Atlet = '{id}'
                """.format(id=str(id_atlet))
        cursor.execute(sql)
        list_enrolled_tuples = cursor.fetchall()
        print(list_enrolled_tuples)

        list_enrolled = []

        for i in list_enrolled_tuples:
            tgl_mulai_event = i[6].strftime("%d %b %Y")
            tgl_selesai_event = i[7].strftime("%d %b %Y")

            dic = {
                "nama_event": i[1],
                "tahun": str(i[2]),
                "stadium": i[3],
                "partai": i[4],
                "kategori": i[5],
                "tgl_mulai": tgl_mulai_event,
                "tgl_selesai": tgl_selesai_event
            }
            list_enrolled.append(dic)

        print(list_enrolled)

        context = {
            'list_enrolled': list_enrolled
        }
    return render(request, "list_enrolled_partai_event.html", context)


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
            # tgl_mulai_sponsor = i[2].strftime("%m/%d/%Y")
            # tgl_selesai_sponsor = i[3].strftime("%m/%d/%Y")
            tgl_mulai_sponsor = i[2].strftime("%d %b %Y")
            tgl_selesai_sponsor = i[3].strftime("%d %b %Y")
            # %d %b %Y
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
        print(year)

        # Create a date object from the extracted values
        date_obj = date(year, month, day)

        return date_obj
    except ValueError:
        return None  # Invalid date string


def get_id_from_email(email):

    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM member WHERE email = '" +
                       email+"'")  # ambil row sponsor
        get_id = cursor.fetchone()
        return get_id[0]
