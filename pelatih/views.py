from collections import namedtuple
from django.db import connection
from django.shortcuts import render, redirect
from django.shortcuts import render
from collections import namedtuple
from django.db import connection
from datetime import datetime as dt



# Create your views here.
def fetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def get_query(str):
    '''Execute SQL query and return its result as a list'''
    cursor = connection.cursor()
    result = []
    try:
        cursor.execute(str)
        result = fetchall(cursor)
    except Exception as e:
        result = e
    finally:
        cursor.close()
        return result


def pelatihan(request):
    pelatih_id = request.session["id"]
    print(pelatih_id)
    response = {}
    with connection.cursor() as cursor:
        # cursor.execute("SET SEARCH_PATH TO public;")
        # if request.session.get("role", None) == "umpire":
        cursor.execute("""
                        SELECT M.Nama
                        FROM MEMBER M, ATLET A
                        WHERE M.ID = A.ID
                        ORDER BY M.Nama ASC;
                        """)

        response['list_atlet'] = cursor.fetchall()
        #print(response['list_atlet'])

        if request.method == "POST":
            nama_atlet = request.POST.get('dropdown2')
            #print(nama_atlet)
            
            
            # INSERT INTO ATLET_PELATIH (ID_Pelatih, ID_Atlet) VALUES ('a2709e74-9b3e-4246-80ea-a18aa2b4248c', '69340675-1776-4491-8a8f-24aa617a4542');
            cursor.execute("""
                    SELECT A.ID
                    FROM MEMBER M
                    INNER JOIN ATLET A ON M.ID = A.ID
                    WHERE M.Nama = %s;
                """, [nama_atlet])
            atlet_id = cursor.fetchall()
            atlet_id_to_string = str(atlet_id[0][0])
            print(atlet_id_to_string)

            cursor.execute("INSERT INTO ATLET_PELATIH (ID_Pelatih, ID_Atlet) VALUES (%s,%s)", (pelatih_id, atlet_id[0][0]))
            
            # insert trigger iei
            
        return render(request, "pilih_atlet.html", response)

def list_atlet_pelatih(request):
    pelatih_id = request.session["id"]
    response = {}
    print(pelatih_id)
    with connection.cursor() as cursor:
        # Nama Atlet, Email, World Rank
        cursor.execute("""SELECT M.Nama, M.Email, A.World_Rank
                       FROM MEMBER M, ATLET A, ATLET_PELATIH AP
                       WHERE M.ID = A.ID AND A.ID = AP.ID_ATLET AND AP.id_pelatih = %s
                     """, [pelatih_id])
        response['data_atlet_pelatih']  = cursor.fetchall()
        print(response['data_atlet_pelatih'])
        return render(request, "list_atlet_pelatih.html", response)
