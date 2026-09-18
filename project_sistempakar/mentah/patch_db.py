import pymysql

def patch_database():
    print("Memulai proses update database...")
    try:
        conn = pymysql.connect(host='localhost', user='root', password='', db='db_pakar_kulit')
        cursor = conn.cursor()
        
        # Mengecek apakah kolom sudah ada
        cursor.execute("SHOW COLUMNS FROM tb_penyakit LIKE 'solusi_pengobatan'")
        result = cursor.fetchone()
        
        if result:
            print("Kolom 'solusi_pengobatan' sudah ada di tabel tb_penyakit.")
        else:
            print("Menambahkan kolom 'solusi_pengobatan' ke tabel tb_penyakit...")
            cursor.execute("ALTER TABLE tb_penyakit ADD COLUMN solusi_pengobatan TEXT")
            conn.commit()
            print("Berhasil! Kolom telah ditambahkan.")
            
            # Memperbarui data dummy agar tidak kosong
            dummy_data = [
                ('P01', 'Gunakan krim antijamur seperti clotrimazole atau miconazole.'),
                ('P02', 'Gunakan salep antivirus seperti acyclovir sesuai resep dokter.'),
                ('P03', 'Gunakan obat kutil yang mengandung asam salisilat atau tindakan medis (krioterapi).'),
                ('P04', 'Bersihkan wajah secara rutin, gunakan krim benzoil peroksida atau asam salisilat.')
            ]
            for kode, solusi in dummy_data:
                cursor.execute("UPDATE tb_penyakit SET solusi_pengobatan=%s WHERE kode_penyakit=%s", (solusi, kode))
            conn.commit()
            print("Data dummy solusi pengobatan berhasil diisi.")
            
    except Exception as e:
        print("Terjadi kesalahan:", str(e))
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()
            print("Koneksi database ditutup.")

if __name__ == '__main__':
    patch_database()
