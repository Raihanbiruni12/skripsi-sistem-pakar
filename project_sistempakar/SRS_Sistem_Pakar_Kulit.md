# Software Requirements Specification (SRS)
**Sistem Pakar Identifikasi Penyakit Kulit Menggunakan AI MobileNetV2 dan Metode Certainty Factor Berbasis Web**

---

## BAB 1: PENDAHULUAN

### 1.1 Tujuan Dokumen
Dokumen *Software Requirements Specification* (SRS) ini bertujuan untuk mendefinisikan secara rinci spesifikasi kebutuhan perangkat lunak untuk "Sistem Pakar Identifikasi Penyakit Kulit". Dokumen ini akan menjadi acuan utama bagi pengembang, penguji, dan pemangku kepentingan (stakeholder) dalam merancang, membangun, dan memvalidasi sistem agar sesuai dengan kebutuhan yang telah disepakati.

### 1.2 Ruang Lingkup Produk
Sistem ini adalah aplikasi berbasis web yang berfungsi sebagai alat bantu deteksi dini (*early screening*) penyakit kulit menggunakan pendekatan hibrida (hybrid).
* **Identifikasi Gambar:** Memanfaatkan kecerdasan buatan (*Deep Learning*) dengan arsitektur MobileNetV2 untuk memindai citra visual lesi kulit.
* **Validasi Gejala:** Memanfaatkan mesin inferensi berbasis aturan (*Rule-Based*) dengan metode perhitungan probabilitas *Certainty Factor* (CF) untuk mengolah gejala klinis tekstual yang dialami pasien.
* **Batasan Medis:** Fokus pada 4 jenis penyakit kulit endemik: Panu (*Tinea Versikolor*), Herpes (*Herpes Simpleks Virus*), Kutil (*Warts*), dan Jerawat (*Acne Vulgaris*). Sistem tidak ditujukan sebagai pengganti diagnosis dokter spesialis, melainkan sebagai pendukung keputusan medis pra-klinis awal.

### 1.3 Definisi, Akronim, dan Singkatan
* **SRS:** *Software Requirements Specification*
* **AI:** *Artificial Intelligence* (Kecerdasan Buatan)
* **CNN:** *Convolutional Neural Network* (Metode untuk klasifikasi citra)
* **MobileNetV2:** Arsitektur CNN yang ringan dan efisien untuk pemrosesan citra.
* **CF:** *Certainty Factor* (Metode perhitungan persentase kepastian gejala)
* **MB & MD:** *Measure of Belief* (Tingkat Kepercayaan) & *Measure of Disbelief* (Tingkat Ketidakpercayaan)
* **Hybrid:** Integrasi dua metode (MobileNetV2 dan Certainty Factor) untuk menghasilkan satu diagnosis akhir.
* **Flask:** Framework micro web berbasis Python.

---

## BAB 2: DESKRIPSI KESELURUHAN (*OVERALL DESCRIPTION*)

### 2.1 Perspektif Produk
Aplikasi ini merupakan sistem mandiri (*standalone web application*) yang berjalan di atas server web (menggunakan arsitektur Flask/Python) dan terhubung ke basis data relasional (MySQL). Antarmuka pengguna akan merespons layar perangkat secara dinamis (*responsive design* menggunakan Bootstrap) sehingga dapat diakses melalui peramban (browser) di komputer maupun ponsel pintar.

### 2.2 Fungsi Produk Utama
* **Manajemen Akun:** Registrasi dan login pengguna dan admin.
* **Pemindaian Citra:** Mengunggah dan memproses foto penyakit kulit (format JPG/PNG).
* **Kuesioner Medis:** Memilih gejala yang dirasakan (checklist interaktif).
* **Kalkulasi Diagnostik Hibrida:** Pencocokan hasil ekstraksi fitur gambar dengan perhitungan aturan CF.
* **Output Penanganan Medis:** Menampilkan penyakit yang terdeteksi, persentase keyakinan, dan saran penanganan dini.
* **Manajemen Basis Pengetahuan (Admin):** Fungsi CRUD untuk master data penyakit, gejala, dan nilai bobot pakar (Aturan CF).
* **Pelaporan (Admin):** Melihat dan mencetak riwayat keseluruhan pengguna.

### 2.3 Karakteristik Pengguna (*User Characteristics*)
Terdapat dua entitas aktor utama:
1.  **Pasien (User):** Masyarakat umum yang ingin melakukan pemeriksaan kulit mandiri. Memiliki pemahaman teknologi dasar (bisa mengoperasikan web browser dan mengunggah foto).
2.  **Pakar / Admin:** Dokter spesialis kulit atau administrator sistem yang memiliki otoritas untuk memperbarui pengetahuan medis (gejala dan nilai bobot) serta mengontrol laporan medis keseluruhan. Memiliki pemahaman operasional dashboard web.

### 2.4 Lingkungan Operasi (*Operating Environment*)
* **Client (Pengguna Akhir):** Berjalan di semua modern web browser (Google Chrome, Mozilla Firefox, Safari, Edge) di PC/Laptop/Smartphone.
* **Server (Backend):** Python 3.x, Flask Web Server.
* **Database:** MySQL (dikelola via phpMyAdmin / Laragon).
* **Library AI:** TensorFlow / Keras (untuk arsitektur MobileNetV2).

---

## BAB 3: KEBUTUHAN SPESIFIK (*SPECIFIC REQUIREMENTS*)

### 3.1 Kebutuhan Fungsional (*Functional Requirements*)

**FR-01: Modul Autentikasi**
* FR-01.1: Sistem harus menyediakan halaman registrasi bagi Pasien baru.
* FR-01.2: Sistem harus menyediakan halaman login.
* FR-01.3: Sistem harus membedakan hak akses masuk antara Pasien dan Admin.

**FR-02: Modul Diagnosis Pasien**
* FR-02.1: Sistem harus dapat menerima input unggahan foto citra kulit dari Pasien.
* FR-02.2: Sistem harus menampilkan daftar gejala (checklist) untuk dipilih Pasien.
* FR-02.3: Sistem harus mengeksekusi fungsi MobileNetV2 dan *Certainty Factor* secara paralel dan mengintegrasikannya (Hybrid).
* FR-02.4: Sistem harus menampilkan hasil diagnosis yang memuat: nama penyakit, nilai persentase kecocokan, dan saran solusi pengobatan medis awal.
* FR-02.5: Sistem harus mencatat hasil diagnosis ke dalam database (tabel riwayat).
* FR-02.6: Sistem harus menyediakan halaman agar Pasien dapat melihat daftar tabel riwayat diagnosis pribadi miliknya.

**FR-03: Modul Dasbor Admin (Pakar)**
* FR-03.1: Sistem harus menyediakan dasbor pemantauan statistik utama bagi Admin.
* FR-03.2: Sistem harus menyediakan fitur kelola data (Tambah, Lihat, Ubah, Hapus) untuk Master Data Penyakit.
* FR-03.3: Sistem harus menyediakan fitur kelola data (Tambah, Lihat, Ubah, Hapus) untuk Master Data Gejala.
* FR-03.4: Sistem harus menyediakan antarmuka Kelola Basis Aturan CF (Menyambungkan penyakit dengan gejalanya, serta memasukkan nilai MB dan MD dari pakar).
* FR-03.5: Sistem harus menyediakan fitur Laporan Diagnosis untuk melihat dan mengekspor (PDF/Excel) rekapan rekam medis seluruh pasien.

### 3.2 Kebutuhan Non-Fungsional (*Non-Functional Requirements*)

* **NFR-01 (Kinerja):** Pemrosesan gambar oleh AI dan kalkulasi gejala harus selesai dalam waktu wajar (di bawah 10 detik) dan tidak memberatkan *thread* aplikasi (Non-blocking response).
* **NFR-02 (Keamanan):** Sandi pengguna di basis data (tb_user) harus dienkripsi. *Routing* khusus admin hanya boleh diakses setelah memvalidasi sesi (session ID) dan otorisasi *role* admin.
* **NFR-03 (Ketersediaan & Keandalan):** Basis data relasional (MySQL) harus mengimplementasikan relasi antar entitas (Foreign Key) agar jika ada data induk penyakit terhapus, sistem tetap memiliki integritas referensial.
* **NFR-04 (Antarmuka & Pengalaman Pengguna):** Frontend harus dirancang secara *responsive* (mobile-friendly) dengan bantuan library Bootstrap.

### 3.3 Struktur Basis Data (Entity Relationship)
Sistem ini ditopang oleh 6 tabel utama:
1.  **Tb_User:** Menyimpan kredensial pengguna dan admin (id_user, nama_lengkap, username, password, role).
2.  **Tb_Penyakit:** Menyimpan master (kode_penyakit, nama_penyakit, deskripsi, solusi).
3.  **Tb_Gejala:** Menyimpan master (kode_gejala, nama_gejala).
4.  **Tb_Aturan_CF:** Menghubungkan kepakaran (id_rule, kode_penyakit, kode_gejala, mb, md).
5.  **Tb_Riwayat_Diagnosis:** Mencatat hasil (id_riwayat, id_user, kode_penyakit, tanggal, foto_lesi, probabilitas_ai, persentase_akhir).
6.  **Tb_Detail_Diagnosis:** Menyimpan relasi gejala yang dipilih saat riwayat diagnosis terbentuk.
