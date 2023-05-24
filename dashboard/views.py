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
        id_atlet = request.session["id"]
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
        status = cursor.fetchone()
        print(status)
        if status[0]:
            string_status = "Qualified"
        else:
            string_status = "Not qualified"

        sql = """SELECT SUM(total_point) AS accumulated_points
                FROM point_history
                WHERE id_atlet = '{id}';""".format(id=id_atlet)
        cursor.execute(sql)  # ambil status
        total = cursor.fetchone()
        print(total)
        if total is None:
            total = 0
        else:
            total = total[0]

        sql = """SELECT M.Nama
                FROM MEMBER M
                JOIN PELATIH P ON P.ID = M.ID
                JOIN ATLET_PELATIH AP ON P.ID = AP.ID_Pelatih
                WHERE AP.ID_Atlet = '{id}';""".format(id=id_atlet)
        cursor.execute(sql)  # ambil status
        pelatih = cursor.fetchall()

        context = {
            'nama': member[0][1],
            'negara': atlet[0][2],
            'email': member[0][2],
            'tgl_lahir': datetime.date.strftime(atlet[0][1], "%d/%m/%Y"),
            'play': right_or_left(atlet[0][3]),
            'tinggi_badan': str(atlet[0][4]),
            'world_rank': atlet[0][5],
            'total_poin': total,
            'status': string_status,
            'pelatih': pelatih
        }

    return render(request, "dashboard_atlet.html", context)


def show_dashboard_pelatih(request):
    # Nama, Negara, Email, Spesialisasi Kategori, Tanggal Mulai
    pelatih_id = request.session["id"]
    response = {}
    with connection.cursor() as cursor:
        cursor.execute("""
                        SELECT DISTINCT
                            M.Nama,
                            M.Email,
                            P.tanggal_mulai
                        FROM
                            PELATIH P,
                            MEMBER M,
                            PELATIH_SPESIALISASI PS

                        WHERE P.ID = M.ID AND P.ID = %s
                        """, [pelatih_id])

        response['list_dashboard_pelatih'] = cursor.fetchall()
        print(response['list_dashboard_pelatih'])

        cursor.execute("""
                        SELECT DISTINCT
                            S.Spesialisasi
                        FROM
                            PELATIH P,
                            MEMBER M,
                            SPESIALISASI S,
                            PELATIH_SPESIALISASI PS

                        WHERE P.ID = M.ID AND PS.ID_Pelatih = P.ID AND PS.ID_SPESIALISASI = S.ID AND P.ID = %s
                        """, [pelatih_id])
        response['pelatih_spesialisasi'] = cursor.fetchall()  
        # print(response['pelatih_spesialisai'])

        merge = []
        for i in response['pelatih_spesialisasi']:
            merge.append(i[0])
        
        string_sp = ''
        for sp in merge:
            string_sp += " " + sp + ","

        spec = string_sp[1:len(string_sp)-1]
        
        new_tuple = (spec,)
        
        response['list_dashboard_pelatih'][0] += new_tuple
        print(response['list_dashboard_pelatih'])

        return render(request, "dashboard_pelatih.html", response)


def show_dashboard_umpire(request):
    umpire_id = request.session["id"]
    response = {}
    with connection.cursor() as cursor:
        #nama, negara, email
        cursor.execute("""
                        SELECT DISTINCT
                            M.Nama,
                            U.Negara,
                            M.Email
                        FROM
                            MEMBER M,
                            UMPIRE U
                        WHERE U.ID = M.ID AND U.ID = %s
                        """, [umpire_id])

        response['list_dashboard_umpire'] = cursor.fetchall()
        print(response['list_dashboard_umpire'])
    return render(request, "dashboard_umpire.html",response)


def right_or_left(boolean):
    if boolean:
        return "Right Hand"
    else:
        return "Left Hand"
