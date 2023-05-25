from django.shortcuts import render
import random
from django.db import connection
from collections import namedtuple
from django.http import HttpResponseRedirect
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
    
def randomize_teams():
    no_peserta = get_query("SELECT nomor_peserta FROM PESERTA_KOMPETISI;")
    tim = []
    for result in no_peserta:
        tim.append(result.nomor_peserta)

    match_1, match_2 = random.choice(tim), random.choice(tim)
    tipe_atlet_1, tipe_atlet_2 = random.choice(["id_atlet_ganda", "id_atlet_kualifikasi"]), random.choice(["id_atlet_ganda", "id_atlet_kualifikasi"])

    while (match_2 == match_1) and (tipe_atlet_2 == tipe_atlet_1):
        match_2 = random.choice(tim)

    if tipe_atlet_1 == "id_atlet_ganda":
        id_1 = get_query(f"SELECT {tipe_atlet_1} FROM PESERTA_KOMPETISI WHERE nomor_peserta = {match_1};")
        tim_1 = tim_ganda(id_1[0].id_atlet_ganda)
    else :
        id_1 = get_query(f"SELECT {tipe_atlet_1} FROM PESERTA_KOMPETISI WHERE nomor_peserta = {match_1};")
        tim_1 = tim_tunggal(id_1[0].id_atlet_kualifikasi)

    if tipe_atlet_2 == "id_atlet_ganda":
        id_2 = get_query(f"SELECT {tipe_atlet_2} FROM PESERTA_KOMPETISI WHERE nomor_peserta = {match_2};")
        tim_2 = tim_ganda(id_2[0].id_atlet_ganda)
    else :
        id_2 = get_query(f"SELECT {tipe_atlet_2} FROM PESERTA_KOMPETISI WHERE nomor_peserta = {match_2};")
        tim_2 = tim_tunggal(id_2[0].id_atlet_kualifikasi)

    return [[match_1, id_1, tim_1], [match_2, id_2, tim_2]]

def tim_ganda(id):
    id_atlet_1 = get_query(f"SELECT id_atlet_kualifikasi FROM ATLET_GANDA WHERE id_atlet_ganda = '{id}';")
    nama_atlet_1 = get_query(f"SELECT nama FROM MEMBER WHERE id = '{id_atlet_1[0].id_atlet_kualifikasi}';")

    id_atlet_2 = get_query(f"SELECT id_atlet_kualifikasi_2 FROM ATLET_GANDA WHERE id_atlet_ganda = '{id}';")
    nama_atlet_2 = get_query(f"SELECT nama FROM MEMBER WHERE id = '{id_atlet_2[0].id_atlet_kualifikasi_2}';")

    return f"{nama_atlet_1[0].nama} & {nama_atlet_2[0].nama}"

def tim_tunggal(id):
    nama_atlet = get_query(f"SELECT nama FROM MEMBER WHERE id = '{id}';")[0]

    return nama_atlet.nama

# NOTE: belum handle tunggal & ganda yang sama
pertandingan = []

for x in range (4):
    tim_1, tim_2 = randomize_teams()
    print(f"{tim_1[2]} VS {tim_2[2]}")

    pertandingan.append([tim_1, tim_2])


def show_perempat(request):
    global pertandingan
    print('sebelum perempat: ', pertandingan)

    context = {
        'pertandingan': pertandingan,
        'score': [[0, 0], [0, 0], [0, 0], [0, 0]]
    }

    if request.method == 'POST':
        score = [request.POST.get('score-1'),
            request.POST.get('score-2'),
            request.POST.get('score-3'),
            request.POST.get('score-4'),
            request.POST.get('score-5'),
            request.POST.get('score-6'),
            request.POST.get('score-7'),
            request.POST.get('score-8')
        ]

        print(score)

        winners = []
        if score[0] < score[1]:
            winners.append(pertandingan[0][1])
            get_query(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Perempat final', '17/10/2023', '17:00:00', '{pertandingan[0][1][0]}', '1');")
            print(get_query(f"SELECT * FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[0][1][0]}"))
            print(get_query(f"DELETE FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[0][1][0]}"))
        else :
            winners.append(pertandingan[0][0])
            get_query(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Perempat final', '17/10/2023', '17:00:00', '{pertandingan[0][0][0]}', '1');")
            print(get_query(f"SELECT * FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[0][0][0]}"))
            print(get_query(f"DELETE FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[0][0][0]}"))

        if score[2] < score[3]:
            winners.append(pertandingan[1][1])
            get_query(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Perempat final', '17/10/2023', '17:00:00', '{pertandingan[1][1][0]}', '1');")
            print(get_query(f"SELECT * FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[1][1][0]}"))
            print(get_query(f"DELETE FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[1][1][0]}"))
        else :
            winners.append(pertandingan[1][0])
            get_query(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Perempat final', '17/10/2023', '17:00:00', '{pertandingan[1][0][0]}', '1');")
            print(get_query(f"SELECT * FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[1][0][0]}"))
            print(get_query(f"DELETE FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[1][0][0]}"))

        if score[4] < score[5]:
            winners.append(pertandingan[2][1])
            get_query(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Perempat final', '17/10/2023', '17:00:00', '{pertandingan[2][1][0]}', '1');")
            print(get_query(f"SELECT * FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[2][1][0]}"))
            print(get_query(f"DELETE FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[2][1][0]}"))
        else :
            winners.append(pertandingan[2][0])
            get_query(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Perempat final', '17/10/2023', '17:00:00', '{pertandingan[2][0][0]}', '1');")
            print(get_query(f"SELECT * FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[2][0][0]}"))
            print(get_query(f"DELETE FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[2][0][0]}"))

        if score[6] < score[7]:
            winners.append(pertandingan[3][1])
            get_query(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Perempat final', '17/10/2023', '17:00:00', '{pertandingan[3][1][0]}', '1');")
            print(get_query(f"SELECT * FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[3][1][0]}"))
            print(get_query(f"DELETE FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[3][1][0]}"))
        else :
            winners.append(pertandingan[3][0])
            get_query(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Perempat final', '17/10/2023', '17:00:00', '{pertandingan[3][0][0]}', '1');")
            print(get_query(f"SELECT * FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[3][0][0]}"))
            print(get_query(f"DELETE FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[3][0][0]}"))

        pertandingan = winners
        return HttpResponseRedirect(reverse('umpire:show_semi'))
    return render(request, "perempat.html", context)

def show_semi(request):
    global pertandingan
    print('sebelum semi: ', pertandingan)

    context = {
        'pertandingan': pertandingan,
        'score': [[0, 0], [0, 0]]
    }

    if request.method == 'POST':
        score = [request.POST.get('score-1'),
            request.POST.get('score-2'),
            request.POST.get('score-3'),
            request.POST.get('score-4')
        ]

        print(score)

        winners = []
        if score[0] < score[1]:
            winners.append(pertandingan[1])
            get_query(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Semi final', '17/10/2023', '17:00:00', '{pertandingan[1]}', '1');")
            print(get_query(f"SELECT * FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[1]}"))
            print(get_query(f"DELETE FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[1]}"))
        else :
            winners.append(pertandingan[0])
            get_query(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Semi final', '17/10/2023', '17:00:00', '{pertandingan[0]}', '1');")
            print(get_query(f"SELECT * FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[0]}"))
            print(get_query(f"DELETE FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[0]}"))

        if score[2] < score[3]:
            winners.append(pertandingan[3])
            get_query(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Semi final', '17/10/2023', '17:00:00', '{pertandingan[3]}', '1');")
            print(get_query(f"SELECT * FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[3]}"))
            print(get_query(f"DELETE FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[3]}"))
        else :
            winners.append(pertandingan[2])

        pertandingan = winners
        print(pertandingan)
        return HttpResponseRedirect(reverse('umpire:show_final'))
    return render(request, "semi.html", context)


def show_final(request):
    global pertandingan
    print('sebelum final: ', pertandingan)

    context = {
        'pertandingan': pertandingan,
        'score': [[0, 0]]
    }

    if request.method == 'POST':
        score = [request.POST.get('score-1'),
            request.POST.get('score-2')
        ]

        print(score)

        winners = []
        if score[0] < score[1]:
            winners.append(pertandingan[0][1])
            get_query(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Final', '17/10/2023', '17:00:00', '{pertandingan[0][1]}', '1');")
            print(get_query(f"SELECT * FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[0][1]}"))
            print(get_query(f"DELETE FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[0][1]}"))
        else :
            winners.append(pertandingan[0][0])
            get_query(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Final', '17/10/2023', '17:00:00', '{pertandingan[0][0]}', '1');")
            print(get_query(f"SELECT * FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[0][0]}"))
            print(get_query(f"DELETE FROM PESERTA_MENGIKUTI_MATCH WHERE nomor_peserta = {pertandingan[0][0]}"))

        pertandingan = winners
        return HttpResponseRedirect(reverse('umpire:show_hasil'))
    return render(request, "final.html")


def show_hasil(request):
    return render(request, "hasil.html")


def list_event(request):
    return render(request, "list_event.html")
