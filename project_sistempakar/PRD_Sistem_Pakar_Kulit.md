# Product Requirements Document (PRD)
**Sistem Pakar Identifikasi Penyakit Kulit Hybrid (MobileNetV2 & Certainty Factor)**

## 1. Ikhtisar Produk (Product Overview)
Sistem pakar berbasis web yang dirancang untuk membantu masyarakat mengidentifikasi penyakit kulit (Panu, Herpes, Kutil, dan Jerawat) secara mandiri. Sistem ini unik karena menggunakan pendekatan "hibrida" (hybrid): menggabungkan pemindaian gambar (*Artificial Intelligence* - MobileNetV2) dengan wawancara gejala (Sistem Pakar - *Certainty Factor*).

## 2. Latar Belakang & Masalah (Background & Problem)
* **Masalah:** Masyarakat sering salah melakukan diagnosis mandiri (*self-diagnosis*) karena kemiripan visual penyakit kulit. Akses ke dokter spesialis juga terbatas, terutama di daerah terpencil.
* **Kesenjangan Produk Saat Ini:** Aplikasi yang sudah ada biasanya hanya memindai gambar tanpa menanyakan gejala yang tak kasat mata (seperti rasa nyeri/gatal), atau sebaliknya, hanya bertanya gejala tanpa bisa melihat wujud fisik luka.
* **Solusi Produk:** Membuat platform web terpadu yang memvalidasi tebakan AI dengan perhitungan matematis gejala yang dialami pasien. Hal ini akan menghasilkan keputusan medis awal yang lebih objektif dan presisi, meniru cara kerja dokter asli.

## 3. Ruang Lingkup Produk (Product Scope)
Sistem ini difokuskan sebagai alat deteksi dini (*early screening*) untuk 4 jenis penyakit:
1. Panu (*Tinea Versikolor*)
2. Herpes (*Herpes Simpleks Virus*)
3. Kutil (*Warts*)
4. Jerawat (*Acne Vulgaris*)
*Catatan: Sistem tidak menggantikan diagnosis dokter, melainkan memberikan informasi awal dan solusi medikasi darurat secara mandiri.*

## 4. Target Pengguna (User Personas)
1. **Pasien (User):** Masyarakat umum yang memiliki keluhan kulit dan mencari layanan deteksi dini yang cepat dan mudah diakses.
2. **Admin (Pakar/Dokter):** Tenaga medis atau pengelola sistem yang bertugas mengelola sistem, memperbarui basis aturan medis, dan memantau lalu lintas diagnosis pasien.

## 5. Kebutuhan Fungsional (Functional Requirements)

### A. Fungsionalitas Pasien (User)
* **Registrasi & Login:** Pengguna dapat membuat akun baru dan masuk ke dalam sistem.
* **Diagnosis Hibrida:**
    * **Upload Gambar:** Pengguna dapat mengunggah foto area kulit yang bermasalah untuk dianalisis oleh AI MobileNetV2.
    * **Checklist Gejala:** Pengguna dapat memilih gejala fisik yang dirasakan beserta tingkat keyakinannya untuk dihitung menggunakan *Certainty Factor*.
* **Output Hasil & Solusi:** Sistem akan menampilkan hasil validasi silang berupa nama penyakit, persentase kepastian (CF Combine), dan rekomendasi solusi pengobatan.
* **Riwayat Diagnosis:** Pengguna dapat melihat kembali tabel rekam jejak riwayat pemeriksaan kulit yang pernah dilakukan sebelumnya.

### B. Fungsionalitas Admin (Pakar)
* **Login Khusus Admin:** Autentikasi masuk ke dasbor manajemen yang terpisah dari pasien.
* **Kelola Data Master (CRUD):** Admin dapat menambah, mengedit, melihat, dan menghapus (CRUD) data penyakit kulit beserta detail gejalanya.
* **Kelola Basis Aturan (Rule Base CF):** Admin dapat menyesuaikan dan memperbarui nilai bobot keyakinan pakar (*Measure of Belief* & *Measure of Disbelief*) yang menghubungkan sebuah penyakit dengan indikator gejalanya.
* **Laporan Diagnosis:** Admin dapat memantau, mencetak, atau mengekspor laporan seluruh aktivitas rekam medis yang dilakukan oleh para pengguna di dalam aplikasi.

## 6. Kebutuhan Non-Fungsional (Non-Functional Requirements)
* **Platform:** Berbasis Web (dapat diakses dari *browser* desktop maupun *mobile* tanpa perlu instalasi aplikasi).
* **Arsitektur & Teknologi:** * Backend & AI: Python, Framework Flask, MobileNetV2.
  * Frontend: HTML, CSS, Bootstrap.
  * Database: MySQL (dikelola via phpMyAdmin/Laragon).
* **Kinerja:** Pemrosesan ekstraksi fitur gambar (CNN) dan komputasi matematis gejala (*Rule-Based*) harus dapat dieksekusi secara paralel di latar belakang tanpa memberatkan antarmuka pengguna.

## 7. Alur Penggunaan Utama (Core User Journey)
1. Pasien masuk (login) dan menuju menu "Diagnosa".
2. Pasien mengunggah foto lesi kulit yang bermasalah.
3. Pasien menjawab pertanyaan (mencentang) gejala yang relevan yang dirasakan.
4. Sistem di latar belakang memproses gambar dan menghitung bobot gejala secara instan.
5. Sistem memvalidasi apakah hasil AI dan hasil hitungan gejala mengarah ke penyakit yang sama.
6. Pasien menerima laporan akhir di layar: *Misal, teridentifikasi Penyakit Herpes (95%) dengan saran pengobatan X.*
7. Data diagnosis otomatis tersimpan di riwayat pasien dan dasbor laporan Admin.
