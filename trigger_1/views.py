from django.shortcuts import redirect, render
from collections import namedtuple
from django.db import connection

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

def is_authenticated(request):
    '''Check if user in a session'''
    try:
        request.session["email"]
        return True
    except KeyError:
        return False

def get_role(nama, email):
    # railway
    # atlet_query = get_query(
    #     f'''
    #     SELECT nama, email
    #     FROM member INNER JOIN atlet ON member.id=atlet.id
    #     WHERE nama='{nama}' AND email='{email}';
    #     '''
    # )

    # lokal
    atlet_query = get_query(
        f'''
        SELECT nama, email
        FROM babadu2.member as m INNER JOIN babadu2.atlet as a ON m.id=a.id
        WHERE nama='{nama}' AND email='{email}';
        '''
    )
    if type(atlet_query) == list and len(atlet_query) != 0:
        print("atlet")
        return "atlet"

    
# Create your views here.
def login(request):
    request.session.flush()
    request.session.clear_expired()
    print("here")
    if request.method != "POST" and not is_authenticated(request):
        print("if1")
        print(request.method)
        return render(request, 'login.html')
    
    if is_authenticated(request):
        print("if 2")
        nama = str(request.session["nama"])
        email = str(request.session["email"])
    else:
        print("else")
        nama = str(request.POST["nama"])
        email = str(request.POST["email"])

    print("here2")
    role = get_role(nama, email)
    print("role")
    request.session["nama"] = nama
    request.session["email"] = email
    request.session["role"] = role
    request.session.set_expiry(0)
    request.session.modified = True
    print("DATA:")
    print(nama)
    print(email)
    print(role)


    if role == "atlet":
        print("there")
        return redirect("../../trigger_4/daftar-event/")
    
    return render(request, "login.html")