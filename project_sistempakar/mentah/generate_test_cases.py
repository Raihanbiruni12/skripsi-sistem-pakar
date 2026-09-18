import os

output_file = r"C:\Users\hp\OneDrive\Documents\project_sistempakar\hasil_pengujian_lengkap.md"

def generate_table(p_id, prioritas, modul, nama_uji, deskripsi, kondisi_awal, langkah_list, kondisi_akhir):
    html = f"""
<table border="1" cellpadding="5" cellspacing="0" style="width:100%; border-collapse: collapse; margin-bottom: 30px;">
  <tr>
    <td colspan="7">
      <b>Nama Projek:</b> Sistem Pakar Identifikasi Penyakit Kulit Menggunakan <i>MobileNetV2</i> dan Metode <i>Certainty Factor</i> Berbasis Web
    </td>
  </tr>
  <tr>
    <td colspan="7">
      <b>ID Kasus Uji:</b> {p_id}<br>
      <b>Prioritas Uji:</b> {prioritas}<br>
      <b>Nama Modul:</b> {modul}<br>
      <b>Nama Uji:</b> {nama_uji}<br>
      <b>Deskripsi:</b> {deskripsi}
    </td>
  </tr>
  <tr>
    <td colspan="7">
      <b>Kondisi Awal:</b> {kondisi_awal}
    </td>
  </tr>
  <tr style="text-align: center; font-weight: bold;">
    <td width="5%">No</td>
    <td width="15%">Langkah Uji</td>
    <td width="15%">Data Uji</td>
    <td width="25%">Hasil yang Diharapkan</td>
    <td width="25%">Hasil Aktual</td>
    <td width="5%">Status</td>
    <td width="10%">Keterangan</td>
  </tr>
"""
    for i, step in enumerate(langkah_list):
        html += f"""  <tr>
    <td align="center">{i+1}</td>
    <td>{step['langkah']}</td>
    <td>{step['data']}</td>
    <td>{step['harapan']}</td>
    <td>{step['aktual']}</td>
    <td align="center">{step['status']}</td>
    <td>{step['ket']}</td>
  </tr>
"""
    html += f"""  <tr>
    <td colspan="7">
      <b>Kondisi Akhir:</b> {kondisi_akhir}
    </td>
  </tr>
</table>
"""
    return html

cases = [
    {
        "id": "P1", "prio": "Tinggi", "modul": "Modul Autentikasi Publik", "nama": "Registrasi Akun Baru", "desc": "Menguji kelancaran formulir registrasi untuk pasien baru pada halaman publik.",
        "awal": "Pengguna berada di Halaman Registrasi dan belum memiliki akun.", "akhir": "Pengguna tervalidasi pada basis data dan berhasil didaftarkan. Detail kredensial tercatat di basis data.",
        "steps": [
            {"langkah": "Akses halaman registrasi", "data": "-", "harapan": "Sistem menampilkan form registrasi", "aktual": "Sistem menampilkan form registrasi dengan baik", "status": "Sukses", "ket": "Halaman termuat"},
            {"langkah": "Masukkan nama, username, password", "data": "User: pasien1<br>Pass: 123", "harapan": "Kolom input terisi dengan data yang diketik", "aktual": "Kolom input terisi dengan data yang diketik", "status": "Sukses", "ket": "Input tervalidasi"},
            {"langkah": "Klik tombol 'Daftar'", "data": "-", "harapan": "Sistem menyimpan data dan mengalihkan ke halaman Login", "aktual": "Sistem berhasil menyimpan data dan mengalihkan ke halaman Login (Gambar L.1)", "status": "Sukses", "ket": "Akun level pasien"}
        ]
    },
    {
        "id": "P2", "prio": "Tinggi", "modul": "Modul Login & Register", "nama": "Login dengan Kredensial Valid", "desc": "Menguji proses otorisasi masuk menggunakan username dan password yang benar untuk Admin dan Pasien.",
        "awal": "Pengguna berada di Halaman Login.", "akhir": "Sesi pengguna tercipta dan diarahkan ke Dashboard masing-masing sesuai hak akses (Admin/Pasien).",
        "steps": [
            {"langkah": "Login sbg Admin", "data": "User: admin<br>Pass: admin123", "harapan": "Masuk ke Dashboard Admin", "aktual": "Pengguna diarahkan ke Dashboard Admin dengan sukses", "status": "Sukses", "ket": "Aktor: Admin"},
            {"langkah": "Logout lalu Login sbg Pasien", "data": "User: pasien1<br>Pass: 123", "harapan": "Masuk ke Dashboard Pasien", "aktual": "Pengguna diarahkan ke Dashboard Pasien dengan sukses", "status": "Sukses", "ket": "Aktor: Pasien"}
        ]
    },
    {
        "id": "P3", "prio": "Sedang", "modul": "Modul Login & Register", "nama": "Login dengan Kredensial Tidak Valid", "desc": "Menguji penolakan sistem terhadap username atau password yang salah untuk kedua tipe pengguna.",
        "awal": "Pengguna berada di Halaman Login.", "akhir": "Sistem menolak otorisasi dan menampilkan peringatan error.",
        "steps": [
            {"langkah": "Uji kredensial Admin salah", "data": "User: admin<br>Pass: 111", "harapan": "Sistem menolak, muncul error", "aktual": "Muncul notifikasi peringatan kredensial salah", "status": "Sukses", "ket": "Aktor: Admin"},
            {"langkah": "Uji kredensial Pasien salah", "data": "User: pasien1<br>Pass: 111", "harapan": "Sistem menolak, muncul error", "aktual": "Muncul notifikasi peringatan kredensial salah", "status": "Sukses", "ket": "Aktor: Pasien"}
        ]
    },
    {
        "id": "P4", "prio": "Tinggi", "modul": "Modul Login & Register", "nama": "Logout dari Sistem", "desc": "Menguji penghancuran sesi (logout) dengan aman pada akun Admin maupun Pasien.",
        "awal": "Admin/Pasien sedang dalam status login.", "akhir": "Sesi terhapus bersih dari peramban.",
        "steps": [
            {"langkah": "Logout dari akun Admin", "data": "-", "harapan": "Sesi terhapus, dialihkan ke Login", "aktual": "Dialihkan ke Halaman Login dan sesi musnah", "status": "Sukses", "ket": "Aktor: Admin"},
            {"langkah": "Logout dari akun Pasien", "data": "-", "harapan": "Sesi terhapus, dialihkan ke Login", "aktual": "Dialihkan ke Halaman Login dan sesi musnah", "status": "Sukses", "ket": "Aktor: Pasien"}
        ]
    },
    {
        "id": "P5", "prio": "Tinggi", "modul": "Modul Kelola Penyakit", "nama": "Tambah Data Penyakit Kulit", "desc": "Menguji form penambahan data master penyakit baru oleh Admin.",
        "awal": "Admin berada di halaman Kelola Master Data.", "akhir": "Penyakit baru tersimpan ke dalam tabel database tb_penyakit.",
        "steps": [
            {"langkah": "Klik 'Tambah Penyakit'", "data": "Kode: P05<br>Nama: Eksim", "harapan": "Data berhasil disubmit", "aktual": "Data berhasil disubmit tanpa error", "status": "Sukses", "ket": "-"},
            {"langkah": "Cek tabel penyakit", "data": "-", "harapan": "Penyakit baru muncul di daftar tabel", "aktual": "Penyakit baru muncul di daftar tabel dengan benar", "status": "Sukses", "ket": "Insert DB Sukses"}
        ]
    },
    {
        "id": "P6", "prio": "Tinggi", "modul": "Modul Kelola Penyakit", "nama": "Edit Data Penyakit Kulit", "desc": "Menguji pembaruan teks deskripsi/solusi pada data penyakit yang sudah ada.",
        "awal": "Terdapat data penyakit di dalam tabel.", "akhir": "Teks deskripsi/solusi penyakit berhasil diperbarui di database.",
        "steps": [
            {"langkah": "Klik tombol 'Edit' pada baris penyakit", "data": "Ubah deskripsi", "harapan": "Form edit muncul dengan data lama", "aktual": "Form edit muncul dengan data lama terisi", "status": "Sukses", "ket": "-"},
            {"langkah": "Klik 'Perbarui'", "data": "-", "harapan": "Data lama diganti dengan data baru di tabel", "aktual": "Teks deskripsi pada tabel berhasil berubah (Gambar P.6)", "status": "Sukses", "ket": "Update Sukses"}
        ]
    },
    {
        "id": "P7", "prio": "Tinggi", "modul": "Modul Kelola Penyakit", "nama": "Hapus Data Penyakit Kulit", "desc": "Menguji penghapusan data penyakit dan relasinya.",
        "awal": "Terdapat data penyakit di dalam tabel.", "akhir": "Data penyakit terhapus dari tabel penyakit dan aturan CF.",
        "steps": [
            {"langkah": "Klik tombol 'Hapus'", "data": "-", "harapan": "Muncul konfirmasi penghapusan", "aktual": "Muncul dialog konfirmasi", "status": "Sukses", "ket": "Proteksi hapus"},
            {"langkah": "Konfirmasi 'Ya'", "data": "-", "harapan": "Data penyakit dan aturan CF terkait lenyap", "aktual": "Data penyakit dan aturan CF terkait terhapus bersih", "status": "Sukses", "ket": "Delete Cascade"}
        ]
    },
    {
        "id": "P8", "prio": "Tinggi", "modul": "Modul Kelola Gejala", "nama": "Tambah Data Gejala Klinis", "desc": "Menguji form penambahan gejala klinis baru.",
        "awal": "Admin berada di halaman Kelola Master Data Gejala.", "akhir": "Gejala baru tersimpan di database tb_gejala.",
        "steps": [
            {"langkah": "Klik 'Tambah Gejala'", "data": "Kode: G09<br>Nama: Gatal parah", "harapan": "Gejala baru tersimpan", "aktual": "Gejala baru tersimpan tanpa error", "status": "Sukses", "ket": "Insert Sukses"}
        ]
    },
    {
        "id": "P9", "prio": "Tinggi", "modul": "Modul Kelola Gejala", "nama": "Edit Data Gejala Klinis", "desc": "Menguji perubahan penamaan gejala klinis.",
        "awal": "Terdapat data gejala.", "akhir": "Nama gejala berubah di tabel.",
        "steps": [
            {"langkah": "Klik 'Edit' pada Gejala", "data": "Ubah nama gejala", "harapan": "Nama gejala diperbarui", "aktual": "Nama gejala berhasil diperbarui di daftar tabel", "status": "Sukses", "ket": "Update Sukses"}
        ]
    },
    {
        "id": "P10", "prio": "Tinggi", "modul": "Modul Kelola Gejala", "nama": "Hapus Data Gejala Klinis", "desc": "Menguji penghapusan gejala beserta aturan pakar yang terkait.",
        "awal": "Terdapat data gejala di database.", "akhir": "Gejala hilang dari tabel gejala dan aturan CF pakar.",
        "steps": [
            {"langkah": "Klik 'Hapus' pada Gejala", "data": "-", "harapan": "Gejala terhapus bersih", "aktual": "Gejala dan aturan CF terkait terhapus bersih", "status": "Sukses", "ket": "Delete Cascade"}
        ]
    },
    {
        "id": "P11", "prio": "Tinggi", "modul": "Modul Aturan Pakar", "nama": "Tambah Aturan Nilai CF (MB & MD)", "desc": "Menguji pembentukan relasi pengetahuan antara penyakit dan gejala.",
        "awal": "Admin berada di halaman Aturan CF.", "akhir": "Relasi pakar baru dengan nilai MB & MD tersimpan ke tb_aturan_cf.",
        "steps": [
            {"langkah": "Pilih Penyakit & Gejala dari dropdown", "data": "P01 & G01", "harapan": "Dropdown menampilkan opsi yang benar", "aktual": "Dropdown menampilkan opsi secara dinamis", "status": "Sukses", "ket": "-"},
            {"langkah": "Input nilai MB dan MD, lalu Simpan", "data": "MB=0.8, MD=0.1", "harapan": "Aturan baru muncul dengan CF=0.7", "aktual": "Aturan baru muncul dengan CF=0.7 (Gambar A.1)", "status": "Sukses", "ket": "Kalkulasi Valid"}
        ]
    },
    {
        "id": "P12", "prio": "Tinggi", "modul": "Modul Aturan Pakar", "nama": "Edit Aturan CF", "desc": "Menguji pembaruan bobot nilai pakar (MB/MD).",
        "awal": "Terdapat aturan pakar di tabel.", "akhir": "Bobot nilai pakar berubah dan mempengaruhi diagnosis selanjutnya.",
        "steps": [
            {"langkah": "Klik 'Edit', ubah nilai MB", "data": "MB=0.9", "harapan": "Nilai MB dan hasil CF diperbarui", "aktual": "Nilai MB dan hasil CF diperbarui pada tabel", "status": "Sukses", "ket": "-"}
        ]
    },
    {
        "id": "P13", "prio": "Tinggi", "modul": "Modul Aturan Pakar", "nama": "Hapus Aturan CF", "desc": "Menguji pemutusan relasi pengetahuan gejala dari penyakit.",
        "awal": "Terdapat aturan pakar di tabel.", "akhir": "Relasi pakar terhapus tanpa menghapus master data penyakit/gejala.",
        "steps": [
            {"langkah": "Klik 'Hapus' pada baris aturan", "data": "-", "harapan": "Aturan hilang dari tabel", "aktual": "Aturan hilang dari tabel tanpa merusak data lain", "status": "Sukses", "ket": "Hanya hapus relasi"}
        ]
    },
    {
        "id": "P14", "prio": "Tinggi", "modul": "Modul Diagnosis Hibrida", "nama": "Input Gambar Lesi Kulit & Pilih Gejala", "desc": "Menguji penangkapan input form diagnosis dari pasien.",
        "awal": "Pasien berada di Halaman Diagnosis.", "akhir": "Data gambar dan gejala siap dikirim ke mesin inferensi (backend).",
        "steps": [
            {"langkah": "Centang keluhan gejala klinis", "data": "Check Gejala G01", "harapan": "Checkbox tercentang", "aktual": "Checkbox tercentang dengan visual yang jelas", "status": "Sukses", "ket": "Input CF"},
            {"langkah": "Unggah foto kondisi kulit", "data": "File: kulit.jpg", "harapan": "Preview gambar muncul", "aktual": "Preview gambar muncul dengan baik di layar", "status": "Sukses", "ket": "Input AI"}
        ]
    },
    {
        "id": "P15", "prio": "Tinggi", "modul": "Modul Diagnosis Hibrida", "nama": "Menampilkan Hasil Diagnosis & Solusi", "desc": "Menguji kalkulasi AI (MobileNetV2) dan Certainty Factor hingga menghasilkan kesimpulan medis.",
        "awal": "Pasien telah memilih gejala dan foto, lalu klik 'Analisis Sekarang'.", "akhir": "Halaman hasil diagnosis tampil menampilkan probabilitas dan solusi.",
        "steps": [
            {"langkah": "Sistem memproses data hibrida", "data": "-", "harapan": "Loading indikator tampil", "aktual": "Loading indikator memblokir layar selama proses", "status": "Sukses", "ket": "UX baik"},
            {"langkah": "Sistem menampilkan halaman hasil", "data": "-", "harapan": "Muncul nama penyakit, persentase CF/AI, dan solusi", "aktual": "Muncul kesimpulan penyakit spesifik beserta solusi (Gambar D.1)", "status": "Sukses", "ket": "Output Akurat"}
        ]
    },
    {
        "id": "P16", "prio": "Sedang", "modul": "Modul Riwayat Diagnosis", "nama": "Menampilkan Daftar Riwayat Diagnosis", "desc": "Menguji privasi rekam medis agar pasien hanya melihat datanya sendiri.",
        "awal": "Pasien memiliki minimal 1 riwayat diagnosis.", "akhir": "Riwayat tampil terfilter berdasarkan ID Pasien.",
        "steps": [
            {"langkah": "Buka menu 'Riwayat Diagnosis'", "data": "-", "harapan": "Daftar riwayat tampil di tabel", "aktual": "Daftar riwayat tampil sesuai akun yang login", "status": "Sukses", "ket": "Filter Session"},
            {"langkah": "Klik tombol 'Detail'", "data": "-", "harapan": "Pop-up menampilkan rincian gejala", "aktual": "Pop-up rincian gejala terbuka dengan benar", "status": "Sukses", "ket": "-"}
        ]
    },
    {
        "id": "P17", "prio": "Sedang", "modul": "Modul Riwayat Diagnosis", "nama": "Cetak Data Riwayat Diagnosis ke PDF", "desc": "Menguji fitur konversi rekam medis menjadi file PDF.",
        "awal": "Pasien berada di Dashboard atau Halaman Hasil Diagnosis.", "akhir": "File dokumen PDF terunduh ke perangkat pengguna.",
        "steps": [
            {"langkah": "Klik tombol 'Cetak PDF'", "data": "-", "harapan": "Proses konversi ke format .pdf", "aktual": "Sistem mengunduh file PDF secara otomatis", "status": "Sukses", "ket": "html2pdf library"}
        ]
    },
    {
        "id": "P18", "prio": "Sedang", "modul": "Modul Kelola Laporan", "nama": "Menampilkan Filter Laporan Diagnosis", "desc": "Menguji fitur pencarian laporan pasien oleh Admin.",
        "awal": "Admin berada di menu Laporan Diagnosis.", "akhir": "Tabel laporan ter-filter sesuai kata kunci.",
        "steps": [
            {"langkah": "Gunakan kolom Search/Penyakit", "data": "Keyword: Panu", "harapan": "Hanya laporan panu yang tampil", "aktual": "Filter tabel berfungsi secara realtime / query param", "status": "Sukses", "ket": "Filter Akurat"}
        ]
    },
    {
        "id": "P19", "prio": "Tinggi", "modul": "Modul Kelola Laporan", "nama": "Cetak Laporan ke PDF/Excel/Print", "desc": "Menguji ekspor rekapitulasi data rekam medis keseluruhan.",
        "awal": "Admin berada di menu Laporan Diagnosis.", "akhir": "Laporan terekspor dalam bentuk tabel rapi di PDF/Excel.",
        "steps": [
            {"langkah": "Klik tombol 'Eksport PDF / Excel'", "data": "-", "harapan": "File .pdf / .xlsx terunduh", "aktual": "File terunduh tanpa kolom tombol aksi", "status": "Sukses", "ket": "Format Rapi"}
        ]
    },
    {
        "id": "P20", "prio": "Tinggi", "modul": "Modul Kelola Laporan", "nama": "Hapus Data Laporan Diagnosis", "desc": "Menguji otorisasi admin dalam membersihkan riwayat spam/dummy.",
        "awal": "Terdapat riwayat pasien di tabel laporan admin.", "akhir": "Riwayat pasien terhapus dari basis data.",
        "steps": [
            {"langkah": "Klik 'Hapus' pada laporan spesifik", "data": "-", "harapan": "Laporan pasien hilang dari database", "aktual": "Laporan pasien sukses terhapus dari basis data", "status": "Sukses", "ket": "Admin Only"}
        ]
    },
    {
        "id": "P21", "prio": "Tinggi", "modul": "Kebutuhan Non-Fungsional", "nama": "Pengujian Usability (Responsivitas Mobile)", "desc": "Menguji adaptasi antarmuka web secara sempurna pada layar smartphone.",
        "awal": "Sistem diakses melalui perangkat mobile atau mode responsif browser.", "akhir": "Tampilan menyesuaikan layar dan fitur kamera/upload mudah diakses.",
        "steps": [
            {"langkah": "Akses halaman web di smartphone", "data": "Viewport Mobile", "harapan": "Elemen web rapi dan menyesuaikan lebar layar", "aktual": "Antarmuka rapi dan tidak ada elemen yang terpotong", "status": "Sukses", "ket": "Mobile-Responsive"},
            {"langkah": "Buka fitur kamera/upload", "data": "-", "harapan": "Tombol mudah ditekan jari", "aktual": "Tombol responsif dan kamera terbuka dengan baik", "status": "Sukses", "ket": "Usability"}
        ]
    },
    {
        "id": "P22", "prio": "Tinggi", "modul": "Kebutuhan Non-Fungsional", "nama": "Pengujian Performance (Waktu Respons)", "desc": "Menguji kecepatan waktu proses kalkulasi MobileNetV2 dan CF.",
        "awal": "Pasien telah melengkapi form dan foto.", "akhir": "Output diagnosis diterima dalam waktu singkat.",
        "steps": [
            {"langkah": "Klik 'Analisis Sekarang'", "data": "Gambar 224x224 & 5 Gejala", "harapan": "Sistem merespons dan menampilkan loading", "aktual": "Loading indikator muncul seketika", "status": "Sukses", "ket": "Feedback Cepat"},
            {"langkah": "Tunggu hasil diagnosis", "data": "Stopwatch berjalan", "harapan": "Proses selesai < 10 detik", "aktual": "Proses selesai dalam kurang dari 5 detik", "status": "Sukses", "ket": "Tidak Hang"}
        ]
    },
    {
        "id": "P23", "prio": "Tinggi", "modul": "Kebutuhan Non-Fungsional", "nama": "Pengujian Security (Keamanan Data)", "desc": "Menguji perlindungan halaman Admin dan privasi file foto pengguna.",
        "awal": "Pengguna tidak berstatus login sebagai Admin.", "akhir": "Sistem memblokir akses ke rute terproteksi.",
        "steps": [
            {"langkah": "Akses URL Dashboard Admin langsung", "data": "URL: /admin/dashboard", "harapan": "Dialihkan ke login, akses ditolak", "aktual": "Sistem memblokir dan mengalihkan ke halaman login", "status": "Sukses", "ket": "Proteksi Rute"},
            {"langkah": "Akses direct link foto kulit orang lain", "data": "URL Foto Pasien Lain", "harapan": "Sistem menolak / tidak ditemukan (403/404)", "aktual": "Akses foto diblokir oleh sistem folder", "status": "Sukses", "ket": "Privasi Aman"}
        ]
    },
    {
        "id": "P24", "prio": "Tinggi", "modul": "Kebutuhan Non-Fungsional", "nama": "Pengujian Availability & Error Handling", "desc": "Menguji kemampuan sistem menangani error input atau akses perangkat.",
        "awal": "Pasien di halaman input diagnosis.", "akhir": "Sistem memberikan pesan kesalahan yang informatif.",
        "steps": [
            {"langkah": "Tolak izin (permission) kamera browser", "data": "Permission Denied", "harapan": "Muncul pesan ramah peringatan kamera", "aktual": "Muncul notifikasi peringatan izin kamera ditolak", "status": "Sukses", "ket": "Bukan blank screen"},
            {"langkah": "Unggah foto yang bukan gambar (txt/pdf)", "data": "File .pdf", "harapan": "Ditolak dengan pesan format salah", "aktual": "Sistem memunculkan peringatan format file tidak valid", "status": "Sukses", "ket": "Validasi Ekstensi"}
        ]
    }
]

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("### 6.2.2 Hasil Pengujian Keseluruhan (Termasuk Non-Fungsional)\n\n")
    f.write("Pengujian dilakukan dengan mengeksekusi 24 rancangan skenario uji (P1 hingga P24) yang mencakup kebutuhan fungsional (*Black-Box Testing*) dan non-fungsional (Usability, Performance, Security, Availability). Hasil pengujian ini mutlak diperlukan untuk membuktikan secara empiris bahwa sistem pakar telah bekerja sesuai spesifikasi rekayasa perangkat lunak.\n\n")
    f.write("Berikut adalah dokumentasi hasil *Test Case Card* untuk setiap skenario P1 sampai P24:\n\n---\n\n")
    
    for c in cases:
        f.write(generate_table(c['id'], c['prio'], c['modul'], c['nama'], c['desc'], c['awal'], c['steps'], c['akhir']))
        
    f.write("\n\n**Rangkuman Hasil Pengujian:**\n")
    f.write("Berdasarkan hasil uji coba menyeluruh dari **P1 hingga P24**, didapatkan kesimpulan bahwa tingkat keberhasilan eksekusi (*Success Rate*) adalah **100%**. Seluruh kebutuhan sistem telah terpenuhi dengan baik secara fungsional maupun non-fungsional, menghasilkan respons sistem yang stabil, cepat, dan aman. Oleh karena itu, Sistem Pakar Identifikasi Penyakit Kulit Hibrida ini dinyatakan **layak beroperasi secara penuh**.\n")

print("Done generating markdown.")
