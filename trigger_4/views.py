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
    # print(id)

    query = get_query(
        f'''
        SELECT nama_event, total_hadiah, tgl_mulai, tgl_selesai, 
        kategori_superseries, kapasitas, nama, stadium.negara, tahun
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
        AND a.id NOT IN (SELECT id_atlet_kualifikasi_2 FROM atlet_ganda)
        AND a.id IN (SELECT id_atlet FROM atlet_kualifikasi);
        '''
    )
    # print(ganda_query)

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
        AND m.id NOT IN (SELECT id_atlet_kualifikasi_2 FROM atlet_ganda)
        AND m.id IN (SELECT id_atlet FROM atlet_kualifikasi);
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
    
    if request.method == 'POST':
        if request.POST.get("partai") == 'TP' or request.POST.get("partai") == 'TL':
            partai = request.POST.get("partai")
            # cek apakah atlet sudah terdaftar di PESERTA_KOMPETISI
            query_peserta_kompetisi = get_query(
                f'''
                SELECT nomor_peserta
                FROM peserta_kompetisi
                WHERE id_atlet_kuaifikasi = '{id}';
                '''
            )

            # insert atlet ke PESERTA KOMPETISI
            if len(query_peserta_kompetisi) == 0:
                nomor_peserta = get_query(f"SELECT max(nomor_peserta) FROM peserta_kompetisi;") + 1
                world_rank = get_query(f"SELECT world_rank FROM atlet_kualifikasi WHERE id_atlet='{id}';")
                world_tour_rank = get_query(f"SELECT world_tour_rank FROM atlet_kualifikasi WHERE id_atlet='{id}';")

                # INSERT
                get_query(f"INSERT INTO PESERTA_KOMPETISI VALUES('{nomor_peserta}', NULL, '{id}', '{world_rank}', '{world_tour_rank}');")

            nomor_peserta = get_query(f"SELECT nomor_peserta FROM peserta_kompetisi WHERE id_atlet_kualifikasi='{id}';")

            # Insert ke partai kompetisi
            get_query(f"INSERT INTO PARTAI_PESERTA_KOMPETISI VALUES('{partai}', '{nama_event}', '{tahun_event}', '{nomor_peserta}');")



        elif request.POST.get("partai") == 'GP' or request.POST.get("partai") == 'GL':
            partai = request.POST.get("partai")
            id_partner = request.POST.get('dropdownGanda')

            # cek apakah data sudah ada di ATLET_GANDA
            query_atlet_ganda = get_query(
                f'''
                (SELECT id_atlet_ganda 
                FROM atlet_ganda
                WHERE id_atlet_kualifikasi = '{id}' AND id_atlet_kualifikasi_2 = '{id_partner}')
                UNION
                (SELECT id_atlet_ganda 
                FROM atlet_ganda
                WHERE id_atlet_kualifikasi = '{id_partner}' AND id_atlet_kualifikasi_2 = '{id}')
                ;
                '''
            )
            # print(query_atlet_ganda)
            
            if len(query_atlet_ganda) == 0:
                id_atlet_ganda = str(uuid.uuid4())

                # query insert data atlet ganda
                get_query(f"INSERT INTO ATLET_GANDA VALUES('{id_atlet_ganda}', '{id}', '{id_partner}');")
                # tes = get_query(f"SELECT * FROM ATLET_GANDA WHERE id_atlet_kualifikasi='{id}';")

            # menyimpan nilai id_atlet_ganda
            id_atlet_ganda = get_query(
                f'''
                SELECT id_atlet_ganda
                FROM atlet_ganda
                WHERE id_atlet_kualifikasi = '{id}' AND id_atlet_kualifikasi_2 = '{id_partner}');
                '''
            )

            # cek apakah atlet sudah terdaftar di PESERTA_KOMPETISI
            query_peserta_kompetisi = get_query(
                f'''
                SELECT nomor_peserta
                FROM peserta_kompetisi
                WHERE id_atlet_ganda = '{id_atlet_ganda}';
                '''
            )

            # insert atlet ke PESERTA KOMPETISI
            if len(query_peserta_kompetisi) == 0:
                nomor_peserta = get_query(f"SELECT max(nomor_peserta) FROM peserta_kompetisi;") + 1
                world_rank = get_query(f"SELECT world_rank FROM atlet_kualifikasi WHERE id_atlet='{id}';")
                world_tour_rank = get_query(f"SELECT world_tour_rank FROM atlet_kualifikasi WHERE id_atlet='{id}';")

                # INSERT
                get_query(f"INSERT INTO PESERTA_KOMPETISI VALUES('{nomor_peserta}', '{id_atlet_ganda}', NULL, '{world_rank}', '{world_tour_rank}');")

            nomor_peserta = get_query(f"SELECT nomor_peserta FROM peserta_kompetisi WHERE id_atlet_ganda='{id_atlet_ganda}';")

            # Insert ke partai kompetisi
            get_query(f"INSERT INTO PARTAI_PESERTA_KOMPETISI VALUES('{partai}', '{nama_event}', '{tahun_event}', '{nomor_peserta}');")


        elif request.POST.get("partai") == 'GC':
            partai = request.POST.get("partai")
            id_partner = request.POST.get('dropdownGandaCampuran')

            query_atlet_ganda = get_query(
                f'''
                (SELECT id_atlet_ganda 
                FROM atlet_ganda
                WHERE id_atlet_kualifikasi = '{id}' AND id_atlet_kualifikasi_2 = '{id_partner}')
                UNION
                (SELECT id_atlet_ganda 
                FROM atlet_ganda
                WHERE id_atlet_kualifikasi = '{id_partner}' AND id_atlet_kualifikasi_2 = '{id}')
                ;
                '''
            )
            # print(query_atlet_ganda)
            
            if len(query_atlet_ganda) == 0:
                id_atlet_ganda = str(uuid.uuid4())

                # query insert data atlet ganda
                get_query(f"INSERT INTO ATLET_GANDA VALUES('{id_atlet_ganda}', '{id}', '{id_partner}');")
                # tes = get_query(f"SELECT * FROM ATLET_GANDA WHERE id_atlet_kualifikasi='{id}';")

            # menyimpan nilai id_atlet_ganda
            id_atlet_ganda = get_query(
                f'''
                SELECT id_atlet_ganda
                FROM atlet_ganda
                WHERE id_atlet_kualifikasi = '{id}' AND id_atlet_kualifikasi_2 = '{id_partner}');
                '''
            )

            # cek apakah atlet sudah terdaftar di PESERTA_KOMPETISI
            query_peserta_kompetisi = get_query(
                f'''
                SELECT nomor_peserta
                FROM peserta_kompetisi
                WHERE id_atlet_ganda = '{id_atlet_ganda}';
                '''
            )

            # insert atlet ke PESERTA KOMPETISI
            if len(query_peserta_kompetisi) == 0:
                nomor_peserta = get_query(f"SELECT max(nomor_peserta) FROM peserta_kompetisi;") + 1
                world_rank = get_query(f"SELECT world_rank FROM atlet_kualifikasi WHERE id_atlet='{id}';")
                world_tour_rank = get_query(f"SELECT world_tour_rank FROM atlet_kualifikasi WHERE id_atlet='{id}';")

                # INSERT
                get_query(f"INSERT INTO PESERTA_KOMPETISI VALUES('{nomor_peserta}', '{id_atlet_ganda}', NULL, '{world_rank}', '{world_tour_rank}');")

            nomor_peserta = get_query(f"SELECT nomor_peserta FROM peserta_kompetisi WHERE id_atlet_ganda='{id_atlet_ganda}';")

            # Insert ke partai kompetisi
            get_query(f"INSERT INTO PARTAI_PESERTA_KOMPETISI VALUES('{partai}', '{nama_event}', '{tahun_event}', '{nomor_peserta}');")


    context = {"jenis_kelamin" : jenis_kelamin,
               "query":query,
               "ganda_query":ganda_query, 
               "campuran_query":campuran_query,
               "kapasitas_tunggal": kapasitas_tunggal,
               "kapasitas_ganda": kapasitas_ganda,
               "kapasitas_campuran": kapasitas_campuran
               }
    # print(context)    
    return render(request, "pilih_kategori.html", context)
