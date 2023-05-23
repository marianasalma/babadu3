from django.shortcuts import render
from collections import namedtuple
from django.db import connection
from datetime import datetime as dt


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
    
# Create your views here.
def pilih_stadium(request):
    print("test")

    #railway
    # query  = get_query(
    #     f'''
    #     SELECT nama as nama_stadium, kapasitas, negara
    #     FROM stadium;
    #     '''
    # )

    # lokal
    query  = get_query(
        f'''
        SELECT nama as nama_stadium, kapasitas, negara
        FROM babadu2.stadium;
        '''
    )
    print(query)
    print("test1")
    return render(request, 'pilih_stadium.html', {"query":query})

def pilih_event(request, nama_stadium):
    current_date = dt.today().strftime("%Y-%m-%d")

    # railway
    # query = get_query(
    #     f'''
    #     SELECT nama_event, total_hadiah, tgl_mulai, kategori_superseries
    #     FROM event
    #     WHERE event.nama_stadium='{nama_stadium}' AND tgl_mulai > '{current_date}';
    #     '''
    # )

    # lokal
    query = get_query(
        f'''
        SELECT nama_event, total_hadiah, tgl_mulai, kategori_superseries
        FROM babadu2.event as e
        WHERE e.nama_stadium='{nama_stadium}' AND tgl_mulai > '{current_date}';
        '''
    )
    # print(query)

    return render(request, "pilih_event.html", {"query":query})

# def pilih_event(request):
#     print("sini2")
#     return render(request, "pilih_event.html")

def pilih_kategori(request, nama_event, tahun_event):
    nama = request.session["nama"]
    email = request.session["email"]

    # railway
    # query = get_query(
    #     f'''
    #     SELECT nama_event, total_hadiah, tgl_mulai, tgl_selesai, 
    #     kategori_superseries, kapasitas, nama, stadium.negara
    #     FROM event INNER JOIN stadium ON nama = nama_stadium
    #     WHERE nama_event = '{nama_event}';
    #     '''
    # )[0]

    # jenis_kelamin = get_query(
    #     f'''
    #     SELECT jenis_kelamin
    #     FROM atlet INNER JOIN member ON member.id = atlet.id
    #     WHERE member.nama = '{nama}' AND member.email = '{email}';
    #     '''
    # )[0]

    # ganda_query = get_query(
    #     f'''
    #     SELECT jenis_kelamin
    #     FROM atlet INNER JOIN member ON member.id = atlet.id
    #     WHERE member.nama = '{nama}' AND member.email = '{email}';
    #     '''
    # )
    # campuran_query = get_query(
    #     f'''
    #     SELECT nama, m.id
    #     FROM atlet as a INNER JOIN member as m ON m.id = a.id
    #     WHERE nama!='{nama}'
    #     AND m.id NOT IN (SELECT id_atlet_kualifikasi FROM atlet_ganda)
    #     AND m.id NOT IN (SELECT id_atlet_kualifikasi_2 FROM atlet_ganda);
    #     '''
    # )
   

    # lokal
    query = get_query(
        f'''
        SELECT nama_event, total_hadiah, tgl_mulai, tgl_selesai, 
        kategori_superseries, kapasitas, nama, stadium.negara
        FROM babadu2.event INNER JOIN babadu2.stadium ON nama = nama_stadium
        WHERE nama_event = '{nama_event}';
        '''
    )[0]

    jenis_kelamin = get_query(
        f'''
        SELECT jenis_kelamin
        FROM babadu2.atlet INNER JOIN babadu2.member ON member.id = atlet.id
        WHERE member.nama = '{nama}' AND member.email = '{email}';
        '''
    )[0]

    # PARTNER
    ganda_query = get_query(
        f'''
        SELECT nama, m.id
        FROM babadu2.atlet as a INNER JOIN babadu2.member as m ON m.id = a.id
        WHERE jenis_kelamin='{jenis_kelamin.jenis_kelamin}' AND nama!='{nama}'
        AND m.id NOT IN (SELECT id_atlet_kualifikasi FROM babadu2.atlet_ganda)
        AND m.id NOT IN (SELECT id_atlet_kualifikasi_2 FROM babadu2.atlet_ganda);
        '''
    )

    campuran_query = get_query(
        f'''
        SELECT nama, m.id
        FROM babadu2.atlet as a INNER JOIN babadu2.member as m ON m.id = a.id
        WHERE nama!='{nama}'
        AND m.id NOT IN (SELECT id_atlet_kualifikasi FROM babadu2.atlet_ganda)
        AND m.id NOT IN (SELECT id_atlet_kualifikasi_2 FROM babadu2.atlet_ganda);
        '''
    )

    # KAPASITAS
    if (jenis_kelamin.jenis_kelamin == True):
        kapasitas_tunggal = get_query(
            f'''     
            SELECT count(nomor_peserta), k.jenis_partai, k.nama_event, k.tahun_event
            FROM babadu2.PARTAI_PESERTA_KOMPETISI as p RIGHT OUTER JOIN babadu2.PARTAI_KOMPETISI as k 
            ON k.jenis_partai=p.jenis_partai AND k.nama_event=p.nama_event AND k.tahun_event=p.tahun_event
            WHERE k.jenis_partai = 'TL' AND k.nama_event = '{nama_event}' AND k.tahun_event = '{tahun_event}'
            GROUP BY (k.jenis_partai, k.nama_event, k.tahun_event);            
            '''
        )[0]

        kapasitas_ganda = get_query(
            f'''          
            SELECT count(nomor_peserta), k.jenis_partai, k.nama_event, k.tahun_event
            FROM babadu2.PARTAI_PESERTA_KOMPETISI as p RIGHT OUTER JOIN babadu2.PARTAI_KOMPETISI as k 
            ON k.jenis_partai=p.jenis_partai AND k.nama_event=p.nama_event AND k.tahun_event=p.tahun_event
            WHERE k.jenis_partai = 'GL' AND k.nama_event = '{nama_event}' AND k.tahun_event = '{tahun_event}'
            GROUP BY (k.jenis_partai, k.nama_event, k.tahun_event);            
            '''
        )[0]
    else:
        kapasitas_tunggal = get_query(
            f'''          
            SELECT count(nomor_peserta), k.jenis_partai, k.nama_event, k.tahun_event
            FROM babadu2.PARTAI_PESERTA_KOMPETISI as p RIGHT OUTER JOIN babadu2.PARTAI_KOMPETISI as k 
            ON k.jenis_partai=p.jenis_partai AND k.nama_event=p.nama_event AND k.tahun_event=p.tahun_event
            WHERE k.jenis_partai = 'TP' AND k.nama_event = '{nama_event}' AND k.tahun_event = '{tahun_event}'
            GROUP BY (k.jenis_partai, k.nama_event, k.tahun_event);            
            '''
        )[0]


        kapasitas_ganda = get_query(
            f'''      
            SELECT count(nomor_peserta), k.jenis_partai, k.nama_event, k.tahun_event
            FROM babadu2.PARTAI_PESERTA_KOMPETISI as p RIGHT OUTER JOIN babadu2.PARTAI_KOMPETISI as k 
            ON k.jenis_partai=p.jenis_partai AND k.nama_event=p.nama_event AND k.tahun_event=p.tahun_event
            WHERE k.jenis_partai = 'GP' AND k.nama_event = '{nama_event}' AND k.tahun_event = '{tahun_event}'
            GROUP BY (k.jenis_partai, k.nama_event, k.tahun_event);            
            '''
        )[0]

    kapasitas_campuran = get_query(
        f'''
        SELECT count(nomor_peserta), k.jenis_partai, k.nama_event, k.tahun_event
        FROM babadu2.PARTAI_PESERTA_KOMPETISI as p RIGHT OUTER JOIN babadu2.PARTAI_KOMPETISI as k 
        ON k.jenis_partai=p.jenis_partai AND k.nama_event=p.nama_event AND k.tahun_event=p.tahun_event
        WHERE k.jenis_partai = 'GC' AND k.nama_event = '{nama_event}' AND k.tahun_event = '{tahun_event}'
        GROUP BY (k.jenis_partai, k.nama_event, k.tahun_event);
        '''
    )[0]
    

    # print("INI JENIS KELAMIN")
    # print(jenis_kelamin)
    # print(ganda_query)
    # print()
    # print(campuran_query)

    context = {"jenis_kelamin" : jenis_kelamin,
               "query":query,
               "ganda_query":ganda_query, 
               "campuran_query":campuran_query,
               "kapasitas_tunggal": kapasitas_tunggal,
               "kapasitas_ganda": kapasitas_ganda,
               "kapasitas_campuran": kapasitas_campuran
               }
    print(context)    
    return render(request, "pilih_kategori.html", context)

    # return render(request, "pilih_kategori.html", {"query":query, "jenis_kelamin":jenis_kelamin, "ganda_query":ganda_query, "campuran_query":campuran_query})
