from collections import namedtuple
from django.db import connection
from django.shortcuts import render, redirect

# Create your views here.


def show_perempat(request):
    return render(request, "perempat.html")


def show_semi(request):
    return render(request, "semi.html")


def show_final(request):
    return render(request, "final.html")


def show_mulai(request,nama_event, jenis_partai):
    return render(request, "mulai.html")


def list_event(request):
    return render(request, "list_event.html")

def list_daftar_atlet(request):
    return render(request, "list_daftar_atlet.html")

def fetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def list_daftar_atlet(request):
    # if request.session.get("role", None) == None:
    #     return redirect("/authentication/user_login")
    response = {}
    with connection.cursor() as cursor:
        # cursor.execute("SET SEARCH_PATH TO public;")
        # if request.session.get("role", None) == "umpire":
        cursor.execute("""
                        SELECT M.Nama, A.Tgl_Lahir, A.Negara_Asal, A.Play_Right, A.Height, K.World_Rank, K.World_Tour_Rank, A.Jenis_Kelamin, COALESCE(PH.Total_Point, 0) AS Total_Poin
                        FROM
                            ATLET A
                            INNER JOIN ATLET_KUALIFIKASI K ON A.ID = K.ID_Atlet
                            INNER JOIN MEMBER M ON A.ID = M.ID
                            LEFT JOIN (
                                SELECT
                                    ID_Atlet,
                                    SUM(Total_Point) AS Total_Point
                                FROM
                                    POINT_HISTORY
                                GROUP BY
                                    ID_Atlet
                            ) PH ON A.ID = PH.ID_Atlet
                        ORDER BY Total_poin DESC
                        """)

        response['list_kualifikasi'] = cursor.fetchall()

        cursor.execute("""
                        SELECT M.Nama, A.Tgl_Lahir, A.Negara_Asal, A.Play_Right, A.Height, A.Jenis_Kelamin
                        FROM
                            ATLET A INNER JOIN ATLET_NON_KUALIFIKASI K ON A.ID = K.ID_Atlet
                            INNER JOIN MEMBER M ON A.ID = M.ID
                        ORDER BY M.Nama
                        """)

        response['list_kualifikasi_2'] = cursor.fetchall()
        # print(response['list_kualifikasi_2'])

        cursor.execute("""
                        SELECT
                            AG.ID_Atlet_Ganda,
                            M1.Nama AS Nama_Atlet1,
                            M2.Nama AS Nama_Atlet2,
                            COALESCE(PH.Total_Point, 0) AS Total_Poin
                        FROM
                            ATLET_GANDA AG
                            INNER JOIN ATLET_KUALIFIKASI AK1 ON AG.ID_Atlet_Kualifikasi = AK1.ID_Atlet
                            INNER JOIN ATLET_KUALIFIKASI AK2 ON AG.ID_Atlet_Kualifikasi_2 = AK2.ID_Atlet
                            INNER JOIN MEMBER  M1 ON AK1.ID_Atlet = M1.ID
                            INNER JOIN MEMBER M2 ON AK2.ID_Atlet = M2.ID
                            LEFT JOIN (
                                SELECT
                                    ID_Atlet,
                                    SUM(Total_Point) AS Total_Point
                                FROM
                                    POINT_HISTORY
                                GROUP BY
                                    ID_Atlet
                            ) PH ON AK1.ID_Atlet = PH.ID_Atlet AND AK2.ID_Atlet = PH.ID_Atlet;
                        """)

        response['list_kualifikasi_3'] = cursor.fetchall()
        # print(response['list_kualifikasi_3'])



        return render(request, 'list_daftar_atlet.html', response)

    # if request.session.get("role", None) == "umpire":
    #     return render(request, 'list_daftar_atlet.html', response)

def partai_kompetisi_event(request):
    # if request.session.get("role", None) == None:
    #     return redirect("/authentication/user_login")
    response = {}
    with connection.cursor() as cursor:
        # cursor.execute("SET SEARCH_PATH TO public;")
        # if request.session.get("role", None) == "umpire":
        cursor.execute("""
                        SELECT
                            E.Nama_Event,
                            E.Tahun,
                            E.Nama_Stadium,
                            PK.Jenis_Partai,
                            E.Kategori_Superseries,
                            E.Tgl_Mulai,
                            E.Tgl_Selesai,
                            ST.Kapasitas
                        FROM
                            EVENT E
                            INNER JOIN PARTAI_KOMPETISI PK ON E.Nama_Event = PK.Nama_Event AND E.Tahun = PK.Tahun_Event
                            INNER JOIN STADIUM ST ON E.Nama_Stadium = ST.Nama
                        ORDER BY E.Tgl_Mulai DESC
                        """)

        response['list_partai_kompetisi'] = cursor.fetchall()
        print(response['list_partai_kompetisi'])
        return render(request, 'partai_kompetisi_event.html', response)
    

def hasil_pertandingan(request, nama_event, jenis_partai):

    response = {}
    with connection.cursor() as cursor:
        
        # nama event, stadium, hadiah, kategori superseries, tanggal_mulai, tanggal_selesai, kapasitas

        cursor.execute("""
                        SELECT
                            E.Nama_Event,
                            E.Nama_Stadium,
                            PK.Jenis_Partai,
                            E.Total_Hadiah,
                            E.Kategori_Superseries,
                            E.Tgl_Mulai,
                            E.Tgl_Selesai,
                            ST.Kapasitas
                        FROM
                            EVENT E
                            INNER JOIN PARTAI_KOMPETISI PK ON E.Nama_Event = PK.Nama_Event AND E.Tahun = PK.Tahun_Event
                            INNER JOIN STADIUM ST ON E.Nama_Stadium = ST.Nama
                        WHERE E.Nama_Event = %s AND PK.Jenis_Partai = %s
                        ORDER BY E.Tgl_Mulai DESC
                        """, (nama_event, jenis_partai))

        response['list_hasil_pertandingan'] = cursor.fetchall()
        # print(response['list_hasil_pertandingan'])
        
        cursor.execute("""
                        SELECT DISTINCT
                            E.Nama_Event,
                            PK.Jenis_Partai,
                            P.nomor_peserta,
                            G.jenis_babak,
                            M1.Nama AS Nama_Atlet1,
                            M2.Nama AS Nama_Atlet2

                        FROM
                            EVENT E
                            INNER JOIN PARTAI_KOMPETISI PK ON E.Nama_Event = PK.Nama_Event AND E.Tahun = PK.Tahun_Event AND PK.Jenis_Partai = %s
                            INNER JOIN PARTAI_PESERTA_KOMPETISI P ON PK.Jenis_Partai = P.Jenis_Partai AND P.Nama_event = PK.Nama_Event AND P.tahun_event = PK.tahun_event
                            INNER JOIN PESERTA_KOMPETISI Pe ON Pe.nomor_peserta =  P.nomor_peserta
                            INNER JOIN PESERTA_MENDAFTAR_EVENT PME ON PME.Nama_Event = E.Nama_Event AND PME.tahun = E.tahun
                            INNER JOIN PESERTA_MENGIKUTI_MATCH PM ON PM.nomor_peserta = Pe.nomor_peserta
                            INNER JOIN MATCH M ON M.jenis_babak = PM.jenis_babak AND M.Waktu_mulai = PM. waktu_mulai
                            INNER JOIN GAME G ON G.jenis_babak = M.jenis_babak
                            INNER JOIN PESERTA_MENGIKUTI_GAME PMG ON PMG.nomor_peserta = Pe.nomor_peserta AND PMG.no_game = G.no_game
                            INNER JOIN ATLET_KUALIFIKASI AK ON AK.ID_Atlet = Pe.id_atlet_kualifikasi AND Pe.ID_Atlet_Kualifikasi = AK.ID_ATLET 
                            INNER JOIN ATLET_GANDA GA ON GA.ID_ATLET_GANDA = Pe.ID_ATLET_GANDA
                            INNER JOIN ATLET A ON AK.ID_ATLET = A.ID
                            INNER JOIN MEMBER ME ON A.ID = ME.ID
                            INNER JOIN ATLET_KUALIFIKASI AK1 ON GA.ID_Atlet_Kualifikasi = AK1.ID_Atlet
                            INNER JOIN ATLET_KUALIFIKASI AK2 ON GA.ID_Atlet_Kualifikasi_2 = AK2.ID_Atlet
                            INNER JOIN MEMBER  M1 ON AK1.ID_Atlet = M1.ID
                            INNER JOIN MEMBER M2 ON AK2.ID_Atlet = M2.ID
                        WHERE E.Nama_Event = %s AND PK.Jenis_Partai = %s
                        """, (jenis_partai, nama_event, jenis_partai))

        response['list_hasil_pertandingan2'] = cursor.fetchall()
        # print(response['list_hasil_pertandingan2'])
        return render(request, 'hasil.html', response)

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

    
def pilih_kategori(request, nama_event, tahun_event):

    id = request.session["id"]
    # print(id)

    jenis_kelamin = get_query(
        f'''
        SELECT jenis_kelamin
        FROM atlet 
        WHERE id = '{id}';
        '''
    )[0]

    # KAPASITAS
    if (jenis_kelamin.jenis_kelamin == True):
        kapasitas_tunggal = get_query(
            f'''     
            SELECT count(nomor_peserta), k.jenis_partai, k.nama_event, k.tahun_event
            FROM PARTAI_PESERTA_KOMPETISI as p RIGHT OUTER JOIN PARTAI_KOMPETISI as k 
            ON k.jenis_partai=p.jenis_partai AND k.nama_event=p.nama_event AND k.tahun_event=p.tahun_event
            WHERE k.jenis_partai = 'TL' AND k.nama_event = '{nama_event}' AND k.tahun_event = '{tahun_event}'
            GROUP BY (k.jenis_partai, k.nama_event, k.tahun_event);            
            '''
        )[0]

        kapasitas_ganda = get_query(
            f'''          
            SELECT count(nomor_peserta), k.jenis_partai, k.nama_event, k.tahun_event
            FROM PARTAI_PESERTA_KOMPETISI as p RIGHT OUTER JOIN PARTAI_KOMPETISI as k 
            ON k.jenis_partai=p.jenis_partai AND k.nama_event=p.nama_event AND k.tahun_event=p.tahun_event
            WHERE k.jenis_partai = 'GL' AND k.nama_event = '{nama_event}' AND k.tahun_event = '{tahun_event}'
            GROUP BY (k.jenis_partai, k.nama_event, k.tahun_event);            
            '''
        )[0]
    else:
        kapasitas_tunggal = get_query(
            f'''          
            SELECT count(nomor_peserta), k.jenis_partai, k.nama_event, k.tahun_event
            FROM PARTAI_PESERTA_KOMPETISI as p RIGHT OUTER JOIN PARTAI_KOMPETISI as k 
            ON k.jenis_partai=p.jenis_partai AND k.nama_event=p.nama_event AND k.tahun_event=p.tahun_event
            WHERE k.jenis_partai = 'TP' AND k.nama_event = '{nama_event}' AND k.tahun_event = '{tahun_event}'
            GROUP BY (k.jenis_partai, k.nama_event, k.tahun_event);            
            '''
        )[0]


        kapasitas_ganda = get_query(
            f'''      
            SELECT count(nomor_peserta), k.jenis_partai, k.nama_event, k.tahun_event
            FROM PARTAI_PESERTA_KOMPETISI as p RIGHT OUTER JOIN PARTAI_KOMPETISI as k 
            ON k.jenis_partai=p.jenis_partai AND k.nama_event=p.nama_event AND k.tahun_event=p.tahun_event
            WHERE k.jenis_partai = 'GP' AND k.nama_event = '{nama_event}' AND k.tahun_event = '{tahun_event}'
            GROUP BY (k.jenis_partai, k.nama_event, k.tahun_event);            
            '''
        )[0]

    kapasitas_campuran = get_query(
        f'''
        SELECT count(nomor_peserta), k.jenis_partai, k.nama_event, k.tahun_event
        FROM PARTAI_PESERTA_KOMPETISI as p RIGHT OUTER JOIN PARTAI_KOMPETISI as k 
        ON k.jenis_partai=p.jenis_partai AND k.nama_event=p.nama_event AND k.tahun_event=p.tahun_event
        WHERE k.jenis_partai = 'GC' AND k.nama_event = '{nama_event}' AND k.tahun_event = '{tahun_event}'
        GROUP BY (k.jenis_partai, k.nama_event, k.tahun_event);
        '''
    )[0]
    
    
    # print(context)    
    return render(request, "pilih_kategori.html", context)
