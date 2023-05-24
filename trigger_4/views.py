import uuid
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
    print("pilih stadium")

    query  = get_query(
        f'''
        SELECT nama as nama_stadium, kapasitas, negara
        FROM stadium;
        '''
    )

    return render(request, 'pilih_stadium.html', {"query":query})


def pilih_event(request, nama_stadium):
    print("pilih event")

    current_date = dt.today().strftime("%Y-%m-%d")

    query = get_query(
        f'''
        SELECT nama_event, total_hadiah, tgl_mulai, kategori_superseries
        FROM event
        WHERE nama_stadium='{nama_stadium}' AND tgl_mulai > '{current_date}';
        '''
    )

    return render(request, "pilih_event.html", {"query":query})


def pilih_kategori(request, nama_event, tahun_event):
    print("pilih kategori")

    id = uuid.UUID(request.session["id"])
    print(id)

    query = get_query(
        f'''
        SELECT nama_event, total_hadiah, tgl_mulai, tgl_selesai, 
        kategori_superseries, kapasitas, nama, stadium.negara
        FROM event INNER JOIN stadium ON nama = nama_stadium
        WHERE nama_event = '{nama_event}' AND tahun = '{tahun_event}';
        '''
    )[0]

    jenis_kelamin = get_query(
        f'''
        SELECT jenis_kelamin
        FROM atlet 
        WHERE id = '{id}';
        '''
    )[0]

    # PARTNER
    ganda_query = get_query(
        f'''
        SELECT nama, a.id
        FROM atlet a INNER JOIN member m ON a.id = m.id
        WHERE jenis_kelamin='{jenis_kelamin.jenis_kelamin}' AND a.id != '{id}'
        AND a.id NOT IN (SELECT id_atlet_kualifikasi 
                        FROM atlet_ganda
                        )
        AND a.id NOT IN (SELECT id_atlet_kualifikasi_2 FROM atlet_ganda);
        '''
    )
    print(ganda_query)

    # ganda_query = get_query(
    #     f'''
    #     (select id_atlet_kualifikasi, nama
    #     from atlet_ganda, member
    #     where id_atlet_kualifikasi != '{id}' AND id_atlet_kualifikasi = id AND id_atlet_kualifikasi not in (SELECT id_atlet_kualifikasi as a1
    #     FROM atlet_ganda INNER JOIN atlet b ON id_atlet_kualifikasi = b.id
    #     INNER JOIN atlet c ON id_atlet_kualifikasi_2 = c.id
    #     where b.jenis_kelamin = c.jenis_kelamin))
    #     UNION 
    #     (select id_atlet_kualifikasi_2, nama
    #     from atlet_ganda, member
    #     where id_atlet_kualifikasi != '{id}' AND id_atlet_kualifikasi = id AND id_atlet_kualifikasi_2 not in (SELECT id_atlet_kualifikasi_2 as a2
    #     FROM atlet_ganda INNER JOIN atlet b ON id_atlet_kualifikasi = b.id
    #     INNER JOIN atlet c ON id_atlet_kualifikasi_2 = c.id
    #     where b.jenis_kelamin = c.jenis_kelamin));
    #     '''
    # )

    campuran_query = get_query(
        f'''
        SELECT m.nama, m.id
        FROM member m inner join atlet a on a.id = m.id
        WHERE m.id != '{id}'
        AND m.id NOT IN (SELECT id_atlet_kualifikasi FROM atlet_ganda)
        AND m.id NOT IN (SELECT id_atlet_kualifikasi_2 FROM atlet_ganda);
        '''
    )

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
