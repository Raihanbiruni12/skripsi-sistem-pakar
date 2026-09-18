# Task Breakdown & Project Plan
**Sistem Pakar Identifikasi Penyakit Kulit Menggunakan AI MobileNetV2 dan Metode Certainty Factor Berbasis Web**

---

## BAB 1: PENDAHULUAN
Dokumen ini merupakan rincian tugas (*Task Breakdown*) yang membagi proses pengerjaan skripsi dan pengembangan aplikasi menjadi fase-fase yang terukur. Dokumen ini dapat digunakan sebagai acuan *timeline* atau daftar periksa (*checklist*) harian bagi pengembang (Raihan Biruni).

---

## BAB 2: STRUKTUR PEMBAGIAN KERJA (WORK BREAKDOWN STRUCTURE)

Proyek ini dibagi menjadi 5 Fase Utama:
1.  **Fase 1: Persiapan & Riset Data (Selesai/On-going)**
2.  **Fase 2: Pengembangan Model AI (MobileNetV2)**
3.  **Fase 3: Pengembangan Sistem Pakar (Certainty Factor)**
4.  **Fase 4: Integrasi & Pembangunan Web (Flask)**
5.  **Fase 5: Pengujian & Penyelesaian Dokumen**

---

## BAB 3: RINCIAN TUGAS (TASK DETAILS)

### Fase 1: Persiapan & Riset Data (Estimasi: 1-2 Minggu)
Fokus: Mengumpulkan bahan baku utama untuk AI dan Sistem Pakar.
* [x] **1.1 Pengumpulan Dataset Citra:**
    * Mencari gambar penyakit kulit (Jerawat, Herpes, Kutil, Panu) dari Kaggle, DermNet, atau sumber medis lain.
    * Memastikan minimal ada 400 gambar per kelas (Total ~1600 gambar).
* [x] **1.2 Pra-pemrosesan Data Gambar:**
    * *Resize* gambar menjadi 224x224 piksel.
    * Melakukan augmentasi (rotasi, *zoom*, *flip*) jika data kurang.
    * Membagi dataset menjadi *Training*, *Validation*, dan *Testing*.
* [x] **1.3 Penyusunan Basis Pengetahuan Medis:**
    * Mewawancarai pakar (dokter) atau mencari jurnal literatur terkait 4 penyakit kulit.
    * Menyusun daftar tabel gejala untuk masing-masing penyakit.
    * Menentukan nilai MB (*Measure of Belief*) dan MD (*Measure of Disbelief*) pakar untuk setiap gejala.

### Fase 2: Pengembangan Model AI (Estimasi: 2 Minggu)
Fokus: Melatih model MobileNetV2 di Google Colab.
* [x] **2.1 Setup Environment:**
    * Menyiapkan Google Colab dan menyambungkan ke Google Drive.
    * *Import library* (TensorFlow, Keras, Matplotlib, dll).
* [x] **2.2 Arsitektur & Training MobileNetV2:**
    * Membangun arsitektur *Transfer Learning* MobileNetV2 (tambah lapisan *GlobalAveragePooling* dan *Dense* 4 kelas).
    * Mengatur parameter *training* (Epoch, *Learning Rate*, *Batch Size*, L2 Regularizer, Dropout).
    * Menjalankan proses *Training* hingga mencapai akurasi yang ideal (mencegah *overfitting*).
* [x] **2.3 Evaluasi & Ekspor Model:**
    * Mencetak grafik *Loss* dan *Accuracy*.
    * Menyimpan model terbaik dalam format `.keras` atau `.h5`.
    * **Tugas Krusial:** Mengonversi model `.keras` ke format **TensorFlow.js (TFJS)** (`model.json` dan `.bin`) dan mengunduhnya ke komputer lokal.

### Fase 3: Pembangunan Backend & Sistem Pakar (Estimasi: 2 Minggu)
Fokus: Membuat arsitektur *database* dan logika *Certainty Factor* menggunakan Python.
* [x] **3.1 Setup Database MySQL:**
    * Membuat *database* `db_pakar_kulit`.
    * Membuat tabel `tb_user`, `tb_penyakit`, `tb_gejala`, `tb_aturan_cf`, `tb_riwayat`.
    * Mengisi *dummy data* atau data pakar asli ke dalam tabel.
* [x] **3.2 Setup Flask & Struktur Folder:**
    * Membuat kerangka *project* Flask (`app.py`, folder `templates/`, folder `static/model/`).
    * Menghubungkan Flask ke *database* MySQL menggunakan konektor (misal: `pymysql` atau `flask_sqlalchemy`).
* [x] **3.3 Implementasi Algoritma Certainty Factor (Python):**
    * Membuat fungsi *query* untuk mengambil nilai MB dan MD berdasarkan gejala yang dipilih pasien.
    * Membuat fungsi matematika untuk menghitung CF Pakar `(MB - MD)`.
    * Membuat fungsi iterasi untuk rumus CF Combine `(CF_old + CF_new * (1 - CF_old))`.
    * Membuat fungsi untuk mengurutkan hasil dan mencari probabilitas tertinggi.

### Fase 4: Integrasi Frontend & Hibrida (Estimasi: 2-3 Minggu)
Fokus: Menyatukan web, AI (JS), dan Sistem Pakar (Python).
* [x] **4.1 Desain Antarmuka Pasien (HTML/CSS/Bootstrap):**
    * Membangun Halaman Beranda & *Login*.
    * Membangun Halaman Diagnosa (Area unggah foto & *checklist* gejala).
* [x] **4.2 Integrasi AI ke Web (Client-Side TFJS):**
    * Menambahkan *script* TensorFlow.js ke halaman HTML.
    * Membuat fungsi JavaScript `tf.loadLayersModel()` untuk membaca `model.json` dari folder `static`.
    * Membuat fungsi *preprocessing* gambar di *browser* (menyamakan ukuran jadi 224x224).
    * Mengirim *output* prediksi AI secara asinkron (AJAX/Fetch) ke *backend* Flask.
* [x] **4.3 Penyatuan Logika (Hybrid Logic):**
    * Flask menerima data (Hasil AI dari JS + *Array* gejala dari *form* HTML).
    * Flask menjalankan kalkulasi *Certainty Factor*.
    * Flask membandingkan dan menggabungkan hasil AI dan CF, lalu menyimpannya ke *database*.
* [ ] **4.4 Halaman Dasbor Admin & Laporan:**
    * [x] Membuat antarmuka CRUD (Tambah, Edit, Hapus) untuk Kelola Penyakit dan Gejala.
    * [ ] Membuat halaman Matriks Aturan CF untuk Admin mengubah nilai kepakaran.
    * [ ] Membuat fitur Laporan Diagnosis (Admin) dan Riwayat Diagnosis (Pasien).

### Fase 5: Pengujian & Penyelesaian (Estimasi: 1-2 Minggu)
Fokus: Uji coba aplikasi dan penulisan Bab 4 & 5 Skripsi.
* [ ] **5.1 *Black-Box Testing*:**
    * Menguji semua tombol, *form*, dan sistem *login* untuk memastikan tidak ada *error* (bug).
    * Mencoba mengunggah gambar yang bukan kulit, atau mengisi *form* kosong untuk menguji validasi.
* [ ] **5.2 Uji Validitas Pakar (UAT):**
    * Membandingkan hasil diagnosa sistem dengan diagnosa pakar/dokter asli menggunakan data uji.
* [ ] **5.3 Penyusunan Naskah Skripsi:**
    * Menyusun Bab 4 (Implementasi Antarmuka & Pembahasan Hasil Pengujian).
    * Menyusun Bab 5 (Kesimpulan dan Saran).
    * Menyiapkan dokumen *source code* dan presentasi sidang.

---

## BAB 4: CATATAN PRIORITAS MINGGU INI
*Berdasarkan progres terakhir (Berhasil mengonversi dan mengunduh model TFJS), fokus selanjutnya adalah:*
1. **Fase 3.2:** Menyusun struktur direktori proyek web Flask lokal.
2. **Fase 4.2:** Mengintegrasikan model `model.json` menggunakan JavaScript agar dapat berjalan di browser (*offline* tanpa ngoding AI di Flask).
