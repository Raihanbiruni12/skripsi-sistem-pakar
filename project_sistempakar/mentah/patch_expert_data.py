import pymysql

def patch_db():
    try:
        print("Menghubungkan ke database...")
        conn = pymysql.connect(host='localhost', user='root', password='', db='db_pakar_kulit')
        cursor = conn.cursor()

        # Nonaktifkan sementara pengecekan Foreign Key agar tidak error saat menghapus data
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        # Kosongkan tabel yang lama
        print("Mereset data penyakit, gejala, dan aturan lama...")
        cursor.execute("TRUNCATE TABLE tb_aturan_cf")
        cursor.execute("TRUNCATE TABLE tb_gejala")
        cursor.execute("TRUNCATE TABLE tb_penyakit")

        # 1. Masukkan Data Penyakit & Solusi Penanganan (Sesuai Tabel 4)
        print("Menyuntikkan data Penyakit dan Solusi Pakar...")
        penyakit_data = [
            ('K01', 'Jerawat (Acne Vulgaris)', 'Peradangan kronis pada kelenjar pilosebasea.', 'Rutin membersihkan wajah dengan produk non-komedogenik. Jangan memencet lesi. Gunakan obat oles jerawat atau konsultasi ke dokter jika meradang parah.'),
            ('K02', 'Herpes (Herpes Simplex Virus)', 'Infeksi virus menular pada kulit.', 'Jaga area lepuhan tetap kering dan bersih. Jangan berbagi barang pribadi. Segera konsultasikan ke dokter untuk resep salep/obat antivirus.'),
            ('K03', 'Panu (Tinea Versicolor)', 'Infeksi jamur pada kulit.', 'Jaga kebersihan badan dan gunakan pakaian yang menyerap keringat. Aplikasikan krim atau sampo antijamur sesuai anjuran apoteker/dokter.'),
            ('K04', 'Kutil (Warts)', 'Infeksi virus HPV pada kulit.', 'Hindari menggaruk atau mencabut paksa benjolan. Gunakan plester asam salisilat atau temui dokter spesialis untuk tindakan medis (kauter/pembekuan).')
        ]
        cursor.executemany("INSERT INTO tb_penyakit (kode_penyakit, nama_penyakit, deskripsi, solusi_pengobatan) VALUES (%s, %s, %s, %s)", penyakit_data)

        # 2. Masukkan Data Gejala (Karena kode gejala di kertas berulang G01-G04, di database harus unik G01-G14)
        print("Menyuntikkan data Gejala Klinis...")
        gejala_data = [
            # Jerawat (K01)
            ('G01', 'Timbul komedo (terbuka/tertutup) pada area wajah atau punggung.'),
            ('G02', 'Terdapat papula atau pustul kemerahan yang meradang.'),
            ('G03', 'Kondisi permukaan kulit cenderung berminyak.'),
            ('G04', 'Terdapat nodul atau kista yang terasa nyeri di bawah kulit.'),
            
            # Herpes (K02)
            ('G05', 'Muncul lepuhan kecil berisi cairan (vesikel) yang berkelompok.'),
            ('G06', 'Terasa nyeri, panas, atau kesemutan sebelum lepuhan muncul.'),
            ('G07', 'Lepuhan pecah dan meninggalkan luka berkerak (krusta).'),
            ('G08', 'Disertai demam ringan atau pembengkakan kelenjar getah bening.'),
            
            # Panu (K03)
            ('G09', 'Timbul bercak berwarna putih, merah muda, atau cokelat pada kulit.'),
            ('G10', 'Bercak terasa gatal, terutama saat tubuh berkeringat.'),
            ('G11', 'Permukaan bercak memiliki sisik halus saat digaruk ringan.'),
            ('G12', 'Batas bercak terlihat jelas dan dapat meluas seiring waktu.'),
            
            # Kutil (K04) - Catatan: G02 dan G03 dicoret oleh pakar (nilai 0), jadi dibuang.
            ('G13', 'Terdapat benjolan kecil bertekstur kasar pada permukaan kulit.'),
            ('G14', 'Umumnya tidak nyeri kecuali jika ditekan atau berada di area tumpuan.')
        ]
        cursor.executemany("INSERT INTO tb_gejala (kode_gejala, nama_gejala) VALUES (%s, %s)", gejala_data)

        # 3. Masukkan Aturan Nilai CF (Sesuai Tabel 1, 2, 3)
        print("Menyuntikkan bobot Certainty Factor (MB & MD)...")
        # Nilai Pakar dianggap sebagai Nilai MB (Measure of Belief). MD = 0
        aturan_data = [
            # Jerawat (K01)
            ('K01', 'G01', 0.6, 0.0),
            ('K01', 'G02', 0.8, 0.0),
            ('K01', 'G03', 0.4, 0.0),
            ('K01', 'G04', 0.6, 0.0),
            
            # Herpes (K02)
            ('K02', 'G05', 1.0, 0.0),
            ('K02', 'G06', 1.0, 0.0),
            ('K02', 'G07', 0.6, 0.0),
            ('K02', 'G08', 0.8, 0.0),
            
            # Panu (K03)
            ('K03', 'G09', 1.0, 0.0),
            ('K03', 'G10', 1.0, 0.0),
            ('K03', 'G11', 1.0, 0.0),
            ('K03', 'G12', 1.0, 0.0),
            
            # Kutil (K04)
            ('K04', 'G13', 1.0, 0.0),
            ('K04', 'G14', 1.0, 0.0)
        ]
        cursor.executemany("INSERT INTO tb_aturan_cf (kode_penyakit, kode_gejala, mb, md) VALUES (%s, %s, %s, %s)", aturan_data)

        # Kembalikan status Foreign Key
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        conn.close()
        print("✅ SUKSES! Database berhasil direvisi sesuai validasi Pakar Medis!")
        
    except Exception as e:
        print(f"❌ Gagal: {str(e)}")
        print("Pastikan aplikasi XAMPP (Apache & MySQL) sudah berjalan (Start).")

if __name__ == "__main__":
    patch_db()
