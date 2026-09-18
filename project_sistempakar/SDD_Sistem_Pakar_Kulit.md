# Software Design Document (SDD)
**Sistem Pakar Identifikasi Penyakit Kulit Menggunakan AI MobileNetV2 dan Metode Certainty Factor Berbasis Web**

---

## BAB 1: PENDAHULUAN

### 1.1 Tujuan Dokumen
Dokumen *Software Design Document* (SDD) ini memberikan deskripsi arsitektur dan rancangan teknis yang komprehensif untuk "Sistem Pakar Identifikasi Penyakit Kulit". Dokumen ini digunakan oleh tim pengembang (developer) sebagai panduan teknis dalam melakukan proses *coding*, integrasi AI, serta pembuatan antarmuka dan basis data.

### 1.2 Ruang Lingkup
Desain yang dibahas dalam dokumen ini mencakup:
* Arsitektur Sistem secara umum (Client-Server).
* Desain Basis Data (Skema dan Relasi).
* Desain Pemrosesan Logika Hibrida (MobileNetV2 + *Certainty Factor*).
* Desain Navigasi Antarmuka Pengguna (*User Interface*).

---

## BAB 2: ARSITEKTUR SISTEM

### 2.1 Pola Arsitektur (*Architectural Pattern*)
Sistem ini menggunakan arsitektur **Client-Server** dengan pola pendekatan **MVC (Model-View-Controller)** yang difasilitasi oleh *framework* Flask (Python).
* **View (Frontend):** Bertanggung jawab atas antarmuka pengguna. Dibangun menggunakan HTML5, CSS3 (Bootstrap), dan JavaScript.
* **Controller (Backend Routing):** Menangani logika aplikasi, menerima input (gambar dan *form* gejala), serta mengatur alur data antara antarmuka, *database*, dan mesin inferensi AI. Dibangun menggunakan Python dan Flask.
* **Model (Database & AI):** Terdiri dari penyimpanan data relasional (MySQL) dan model *Machine Learning* statis (MobileNetV2 format .h5 / .keras / .json).

### 2.2 Diagram Alur Sistem Terpadu (Hybrid Flow)
1. **Input:** *Client* mengirimkan Gambar Lesi Kulit + *Array* Gejala yang dipilih.
2. **Proses AI (MobileNetV2):** Gambar di-*resize* ke ukuran $224 \times 224$ piksel, diubah menjadi *array / tensor*, lalu dieksekusi oleh model AI untuk menghasilkan probabilitas 4 kelas penyakit (Jerawat, Herpes, Kutil, Panu).
3. **Proses Sistem Pakar (Certainty Factor):** *Array* gejala dicocokkan dengan basis aturan di *database* (Nilai *Measure of Belief* & *Measure of Disbelief*). Dihitung nilai *CF_Pakar*, dikalikan dengan *CF_User*, lalu digabungkan menggunakan rumus *CF_Combine*.
4. **Validasi Hibrida:** Sistem membandingkan hasil kelas prediksi AI tertinggi dengan hasil *Certainty Factor* tertinggi.
5. **Output:** Sistem mengembalikan respons berupa laporan diagnosis akhir (Penyakit dominan, Persentase Keyakinan, Solusi Medis) ke *View* (*Browser* pasien).

---

## BAB 3: DESAIN BASIS DATA (*DATABASE DESIGN*)

Sistem menggunakan RDBMS MySQL. Berikut adalah desain skema tabel dan propertinya:

### 3.1 Tabel `tb_user` (Manajemen Pengguna)
* `id_user` (INT, Primary Key, Auto Increment)
* `nama_lengkap` (VARCHAR 100)
* `username` (VARCHAR 50, Unique)
* `password` (VARCHAR 255, Hashed)
* `role` (ENUM: 'admin', 'pasien')

### 3.2 Tabel `tb_penyakit` (Master Penyakit)
* `kode_penyakit` (VARCHAR 10, Primary Key) *(contoh: P01, P02)*
* `nama_penyakit` (VARCHAR 50)
* `deskripsi` (TEXT)
* `solusi_pengobatan` (TEXT)

### 3.3 Tabel `tb_gejala` (Master Gejala)
* `kode_gejala` (VARCHAR 10, Primary Key) *(contoh: G01, G02)*
* `nama_gejala` (VARCHAR 150)

### 3.4 Tabel `tb_aturan_cf` (Rule Base Pakar)
* `id_rule` (INT, Primary Key, Auto Increment)
* `kode_penyakit` (VARCHAR 10, Foreign Key ke `tb_penyakit`)
* `kode_gejala` (VARCHAR 10, Foreign Key ke `tb_gejala`)
* `mb` (FLOAT) - *Measure of Belief* (0.0 s/d 1.0)
* `md` (FLOAT) - *Measure of Disbelief* (0.0 s/d 1.0)

### 3.5 Tabel `tb_riwayat_diagnosis` (Rekam Medis)
* `id_riwayat` (VARCHAR 20, Primary Key)
* `id_user` (INT, Foreign Key ke `tb_user`)
* `tanggal` (DATETIME)
* `foto_lesi` (VARCHAR 255) - Path file gambar
* `kode_penyakit_hasil` (VARCHAR 10, Foreign Key ke `tb_penyakit`)
* `persentase_akhir` (FLOAT)

### 3.6 Tabel `tb_detail_diagnosis` (Log Gejala Pasien)
* `id_detail` (INT, Primary Key, Auto Increment)
* `id_riwayat` (VARCHAR 20, Foreign Key ke `tb_riwayat_diagnosis`)
* `kode_gejala` (VARCHAR 10)
* `cf_user` (FLOAT) - Bobot yang dipilih pasien (misal: Sangat Yakin = 1.0)

---

## BAB 4: DESAIN ANTARMUKA (*USER INTERFACE*)

### 4.1 Peta Situs (Sitemap) / Struktur Navigasi
**A. Modul Publik / Pasien:**
* **Halaman Utama (Beranda):** Informasi sistem dan petunjuk penggunaan.
* **Halaman Login & Register:** Formulir autentikasi.
* **Halaman Diagnosa:** * Area *Drag & Drop / Upload File* (Input Foto).
  * Area Tabel *Checklist* Gejala (Input *Dropdown* tingkat keyakinan).
  * Tombol "Proses Diagnosis".
* **Halaman Hasil Diagnosis:** Menampilkan Gambar asli, Grafik probabilitas AI, Tabel perhitungan CF, Kesimpulan, dan Tombol Cetak PDF.
* **Halaman Riwayat:** Tabel *grid* daftar konsultasi masa lalu.

**B. Modul Admin (Dashboard):**
* **Dasbor Utama:** Statistik jumlah pasien, jumlah diagnosis hari ini.
* **Menu Master Penyakit:** Tabel Data (DataTables), Form Tambah/Edit.
* **Menu Master Gejala:** Tabel Data, Form Tambah/Edit.
* **Menu Basis Pengetahuan (Rules CF):** *Mapping* Gejala ke Penyakit beserta *input slider* nilai MB & MD.
* **Menu Laporan:** Tabel rekam jejak diagnosis semua user dengan fitur Filter Tanggal dan *Export Excel/PDF*.

---

## BAB 5: DESAIN KOMPONEN AI & SISTEM PAKAR

### 5.1 Spesifikasi Model MobileNetV2
* **Arsitektur Dasar:** *Pre-trained weights* ImageNet (Transfer Learning).
* **Ukuran Input:** $224 \times 224 \times 3$ (RGB).
* **Layer Tambahan (Top Layers):** * `GlobalAveragePooling2D`
  * `Dropout` (Mencegah *overfitting*)
  * `Dense` (4 neuron, aktivasi `softmax` untuk probabilitas 4 penyakit).
* **Format Output:** Kumpulan (array) nilai float yang jika dijumlahkan bernilai 1.0 (100%).

### 5.2 Spesifikasi Logika Certainty Factor
* **Rumus CF Pakar:** `CF(Pakar) = MB - MD`
* **Rumus CF Kondisi:** `CF(Gejala) = CF(Pakar) * CF(User)`
* **Rumus CF Kombinasi (Jika gejala > 1 untuk satu penyakit):**
  * `CF_Combine_1 = CF_1 + CF_2 * (1 - CF_1)`
  * `CF_Combine_2 = CF_Combine_1 + CF_3 * (1 - CF_Combine_1)`
  * *Dan seterusnya hingga seluruh gejala terkait iterasi selesai.*
* **Penentuan Penyakit CF:** Penyakit dengan nilai `CF_Combine` paling tinggi (mendekati 1.0) ditetapkan sebagai hasil dari sistem pakar.
