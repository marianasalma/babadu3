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
    aa = request.session.get('id')
    print(aa)
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
        print(response['list_atlet'])

        if request.method == "POST":
            nama_atlet = request.POST.get('dropdown2')
            print(nama_atlet)

            # cursor.execute()

            
        return render(request, "pilih_atlet.html", response)


def get_role(nama, email):
    atlet_query = get_query(
        f'''
        SELECT nama, email
        FROM member as m INNER JOIN atlet as a ON m.id=a.id
        WHERE nama='{nama}' AND email='{email}';
        '''
    )

    umpire_query = get_query(
        f'''
        SELECT nama, email
        FROM member as m INNER JOIN umpire as u ON m.id=u.id
        WHERE nama='{nama}' AND email='{email}';
        '''
    )

    pelatih_query = get_query(
        f'''
        SELECT nama, email
        FROM member as m INNER JOIN pelatih as p ON m.id=p.id
        WHERE nama='{nama}' AND email='{email}';
        '''
    )

    if type(atlet_query) == list and len(atlet_query) != 0:
        print("atlet")      #to be deleted
        return "atlet"
    elif type(umpire_query) == list and len(umpire_query) != 0:
        print("umpire")     #to be deleted
        return "umpire"
    elif type(pelatih_query) == list and len(pelatih_query) != 0:
        print("pelatih")    #to be deleted
        return "pelatih"


def pilih_atlet(request):
    
    cursor = connection.cursor()
    nama_atlet = request.session.get("nama")

    # get daftar stadium
    cursor.execute('SELECT * FROM ATLET')
    daftar_stadium = cursor.fetchall()

    list_atlet = []
    for atlet in nama_atlet:
        list_atlet.append(atlet[1])
    print(list_atlet)

    if request.method == "POST":
        atlet = request.POST.get("atlet")
        print(atlet)
        
        # # STORED PROCEDURE N TRIGGER? nnti list yg unavail di oper ke pilih jam 
        # try:
        #     cursor.execute(
        #         f"""
        #         INSERT INTO PEMINJAMAN VALUES ('{id_manajer}', '{start_datetime}', '{end_datetime}', '{nama_stadium}')"""
        #     )

        #     return redirect("dashboard/panitia")
        return redirect("../pelatih/list_atlet")
        # except Exception as e:
        #     messages.error(request, e)

    ## BLM DIGANTI
    cursor.close()
    return render(request, "list_atlet.html", { 
            "list_atlet": list_atlet })