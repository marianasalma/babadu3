from collections import namedtuple
from django.db import connection
from django.shortcuts import render, redirect

# Create your views here.
def fetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def pelatihan(request):
    response = {}
    with connection.cursor() as cursor:
        # cursor.execute("SET SEARCH_PATH TO public;")
        # if request.session.get("role", None) == "umpire":
        cursor.execute("""
                        SELECT M.Nama
                        FROM MEMBER M, ATLET A
                        WHERE M.ID = A.ID;
                        """)

        response['list_atlet'] = cursor.fetchall()
        print(response['list_atlet'])
    return render(request, "latih_atlet.html")
    