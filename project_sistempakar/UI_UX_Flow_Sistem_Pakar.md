# UI/UX Flow (Alur Pengguna & Antarmuka)
**Sistem Pakar Identifikasi Penyakit Kulit Menggunakan AI MobileNetV2 dan Metode Certainty Factor Berbasis Web**

---

## BAB 1: PENDAHULUAN

Dokumen UI/UX Flow ini merangkum perjalanan pengguna (*User Journey*) dan struktur halaman (*Screen Flow*) dari awal pengguna masuk hingga mendapatkan hasil akhir. Desain antarmuka difokuskan pada kemudahan penggunaan (*user-friendly*), terutama pada proses input dua tahap (unggahan foto dan pemilihan gejala).

---

## BAB 2: USER FLOW (ALUR PENGGUNA)

### 2.1 Alur Pengguna: Pasien (User)
Alur ini dirancang sesederhana mungkin agar pasien awam dapat menggunakan sistem tanpa kebingungan.

1. **Start:** Pasien membuka aplikasi (Halaman *Landing Page*).
2. **Autentikasi:** Pasien melakukan *Login* (atau *Register* jika belum punya akun).
3. **Dasbor Pasien:** Sistem menampilkan beranda pasien (Info singkat & Tombol "Mulai Diagnosa").
4. **Proses Diagnosa (Tahap 1 - AI):** * Pasien diarahkan ke halaman unggah foto.
   * Pasien memotret atau mengunggah (*drag & drop*) foto area kulit yang terinfeksi.
   * Klik "Lanjut".
5. **Proses Diagnosa (Tahap 2 - Gejala):** * Sistem menampilkan daftar periksa (*checklist*) gejala.
   * Pasien mencentang gejala yang dirasakan dan memilih tingkat keyakinan (misal: "Sedikit Yakin", "Sangat Yakin").
   * Klik "Proses Analisis".
6. **Loading Screen:** Menampilkan animasi pemrosesan (Sistem sedang menggabungkan MobileNetV2 dan *Certainty Factor*).
7. **Halaman Hasil:** * Sistem menampilkan persentase kecocokan penyakit.
   * Menampilkan saran penanganan dini medis.
8. **End:** Pasien dapat mencetak hasil (PDF) atau kembali ke Beranda/Riwayat.

### 2.2 Alur Pengguna: Admin (Pakar)
Alur ini difokuskan pada efisiensi manajemen data dan pemantauan sistem.

1. **Start:** Admin membuka halaman *Login* khusus Admin.
2. **Dasbor Admin:** Menampilkan statistik (Total Pasien, Total Penyakit, Grafik Diagnosa Bulan Ini).
3. **Manajemen Data (Bercabang):**
   * **Jalur A (Kelola Penyakit):** Admin -> Menu Penyakit -> Tambah/Edit/Hapus data penyakit & solusi.
   * **Jalur B (Kelola Gejala):** Admin -> Menu Gejala -> Tambah/Edit/Hapus data gejala.
   * **Jalur C (Kelola Aturan CF):** Admin -> Menu Basis Aturan -> Pilih Penyakit -> Pilih Gejala -> Input Nilai MB & MD -> Simpan.
4. **Pemantauan (Jalur D):** Admin -> Menu Laporan -> Lihat Riwayat Pasien -> Filter Tanggal -> Ekspor Data (Excel/PDF).
5. **End:** Admin *Logout*.

---

## BAB 3: SCREEN FLOW & WIREFRAME STRUCTURE

Berikut adalah gambaran kasar elemen-elemen UI (Antarmuka) yang wajib ada di setiap halaman utama:

### 3.1 Halaman Diagnosa (Core UI - Pasien)
Halaman ini dibagi menjadi dua *step* agar layar tidak terlihat penuh (Konsep *Wizard Form*).

**Step 1: Input Visual (MobileNetV2)**
* **Header:** Judul "Tahap 1: Unggah Foto Lesi Kulit"
* **Komponen Utama:** * Kotak putus-putus besar untuk *Drag & Drop* atau *Klik untuk Unggah*.
  * *Preview* Gambar (muncul setelah foto diunggah).
  * Tombol "Lanjut ke Gejala" (Hanya aktif jika foto sudah masuk).

**Step 2: Input Gejala (Certainty Factor)**
* **Header:** Judul "Tahap 2: Kondisi yang Dirasakan"
* **Komponen Utama:**
  * Tabel/Daftar gejala interaktif.
  * Setiap baris gejala memiliki *Checkbox* (Centang).
  * Jika dicentang, muncul *Dropdown* Bobot User (0.2 = Tidak Tahu, 0.4 = Sedikit Yakin, 0.6 = Cukup Yakin, 0.8 = Yakin, 1.0 = Sangat Yakin).
  * Tombol "Proses Diagnosa".

### 3.2 Halaman Hasil Diagnosa (Result Page)
* **Visual Aid:** Menampilkan ulang foto yang diunggah pengguna (di pojok kiri).
* **Diagnosa Utama:** Teks besar berbunyi "Anda teridentifikasi mengalami: [NAMA PENYAKIT]".
* **Tingkat Keyakinan:** *Progress Bar* melingkar atau horizontal (misal: **89.5%**).
* **Rincian Perhitungan (Opsional/Accordion):** * Tab "Hasil AI (Gambar)" -> Menampilkan probabilitas dari MobileNetV2.
  * Tab "Hasil Pakar (Gejala)" -> Menampilkan hitungan CF Combine.
* **Solusi & Rekomendasi:** Kotak peringatan/informasi berisi saran medis dan anjuran ke dokter.
* **Action Buttons:** Tombol "Cetak PDF" dan "Selesai".

### 3.3 Dasbor Admin (Pakar)
* **Sidebar (Kiri):** Beranda, Data Penyakit, Data Gejala, Basis Aturan CF, Laporan, Pengaturan.
* **Topbar (Atas):** Profil Admin, Tanggal, Tombol *Logout*.
* **Area Konten (Kanan):** * **Halaman Aturan CF:** Tabel matriks yang mempertemukan baris (Gejala) dan kolom (Penyakit). Admin dapat mengklik sel tabel untuk mengedit nilai MB dan MD secara *pop-up (modal)*.

---

## BAB 4: PANDUAN PENGALAMAN PENGGUNA (UX GUIDELINES)

1. **Responsivitas:** Semua desain form, tabel gejala, dan tombol harus mudah di-*tap* menggunakan jempol saat diakses dari *smartphone*.
2. **Pencegahan Error (*Error Prevention*):** * Jika pengguna mengunggah file selain gambar (PDF/Word), munculkan peringatan *pop-up* "Harap unggah file JPG/PNG".
   * Jangan biarkan pengguna menekan "Proses Diagnosa" jika tidak ada satupun gejala yang dicentang.
3. **Status Sistem Terlihat:** Saat AI memproses gambar (yang mungkin memakan waktu 2-4 detik), wajib tampilkan indikator *loading* seperti "Sedang menganalisis gambar..." agar pengguna tidak mengira web sedang *hang* atau *error*.
