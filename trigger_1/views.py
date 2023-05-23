from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from collections import namedtuple
from django.db import connection
from django.contrib import messages
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


def is_authenticated(request):
    '''Check if user in a session'''
    try:
        request.session["id"]
        return True
    except KeyError:
        return False


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
    
def get_id(nama, email):
    print("get id")
    query = get_query(
        f'''
        SELECT id
        FROM member
        WHERE nama='{nama}' AND email='{email}';
        '''
    )[0]
    return str(query.id)



# Create your views here.
def login(request):
    request.session.flush()
    request.session.clear_expired()
    print("login")      #to be deleted

    if request.method != "POST" and not is_authenticated(request):
        return render(request, 'login.html')

    if is_authenticated(request):
        print("is authenticated")       #to be deleted
        id = str(request.session["id"])

        # to be deleted
        print('Type', type(request.session["id"]), 'UIID', request.session["id"]) 

    else:
        print("is not authenticated")       #to be deleted
        nama = str(request.POST["nama"])
        email = str(request.POST["email"])

    try:
        role = get_role(nama, email)
        id = get_id(nama, email)
        request.session["id"] = id
        request.session["role"] = role
        request.session.set_expiry(0)
        request.session.modified = True
    except:
        if not is_authenticated(request):
            messages.error(request, 'Email atau password salah')
            return render(request, 'login.html')

    #to be deleted
    print("DATA:")
    print(nama)
    print(email)
    print(role)
    print(id)
    print()
    print(request.session["id"])
    print(request.session["role"])
    print()
    print("type")
    print('Type', type(request.session["id"]), 'UIID', request.session["id"])

    if role == "atlet":
        print("redirecting to atlet dashboard")     #to be deleted
        # return redirect("../../dash/atlet")
        return redirect("../../trigger_4/daftar-event/")

    elif role == "umpire":
        print("redirecting to umpire dashboard")     #to be deleted
        return redirect("../../dash/umpire")
    elif role == "pelatih":
        print("redirecting to pelatih dashboard")     #to be deleted
        return redirect("../../dash/pelatih")

    return render(request, "login.html", messages)


def logout(request):
    request.session.flush()
    request.session.clear_expired()

    return HttpResponseRedirect(reverse('trigger_1:landing_page'))

def landing_page(request):
    return render(request, "landing_page.html")
