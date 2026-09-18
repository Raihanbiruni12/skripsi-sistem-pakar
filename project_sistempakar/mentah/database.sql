-- Pembuatan Database
CREATE DATABASE IF NOT EXISTS db_pakar_kulit;
USE db_pakar_kulit;

-- 1. Tabel User (Manajemen Pengguna)
CREATE TABLE IF NOT EXISTS tb_user (
  id_user INT PRIMARY KEY AUTO_INCREMENT,
  nama_lengkap VARCHAR(100) NOT NULL,
  username VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  role ENUM('admin', 'pasien') NOT NULL
);

-- 2. Tabel Penyakit (Master Penyakit)
CREATE TABLE IF NOT EXISTS tb_penyakit (
  kode_penyakit VARCHAR(10) PRIMARY KEY,
  nama_penyakit VARCHAR(50) NOT NULL,
  deskripsi TEXT,
  solusi_pengobatan TEXT
);

-- 3. Tabel Gejala (Master Gejala)
CREATE TABLE IF NOT EXISTS tb_gejala (
  kode_gejala VARCHAR(10) PRIMARY KEY,
  nama_gejala VARCHAR(150) NOT NULL
);

-- 4. Tabel Aturan CF (Rule Base Pakar)
CREATE TABLE IF NOT EXISTS tb_aturan_cf (
  id_rule INT PRIMARY KEY AUTO_INCREMENT,
  kode_penyakit VARCHAR(10) NOT NULL,
  kode_gejala VARCHAR(10) NOT NULL,
  mb FLOAT NOT NULL,
  md FLOAT NOT NULL,
  FOREIGN KEY (kode_penyakit) REFERENCES tb_penyakit(kode_penyakit) ON DELETE CASCADE,
  FOREIGN KEY (kode_gejala) REFERENCES tb_gejala(kode_gejala) ON DELETE CASCADE
);

-- 5. Tabel Riwayat Diagnosis (Rekam Medis)
CREATE TABLE IF NOT EXISTS tb_riwayat_diagnosis (
  id_riwayat VARCHAR(20) PRIMARY KEY,
  id_user INT,
  tanggal DATETIME NOT NULL,
  foto_lesi VARCHAR(255),
  kode_penyakit_hasil VARCHAR(10),
  persentase_akhir FLOAT,
  FOREIGN KEY (id_user) REFERENCES tb_user(id_user) ON DELETE CASCADE,
  FOREIGN KEY (kode_penyakit_hasil) REFERENCES tb_penyakit(kode_penyakit) ON DELETE CASCADE
);

-- 6. Tabel Detail Diagnosis (Log Gejala Pasien)
CREATE TABLE IF NOT EXISTS tb_detail_diagnosis (
  id_detail INT PRIMARY KEY AUTO_INCREMENT,
  id_riwayat VARCHAR(20) NOT NULL,
  kode_gejala VARCHAR(10) NOT NULL,
  cf_user FLOAT NOT NULL,
  FOREIGN KEY (id_riwayat) REFERENCES tb_riwayat_diagnosis(id_riwayat) ON DELETE CASCADE
);


-- ==========================================
-- DUMMY DATA AWAL
-- ==========================================

-- Data Dummy User
INSERT INTO tb_user (nama_lengkap, username, password, role) VALUES 
('Administrator', 'admin', 'admin123', 'admin'),
('Pasien Dummy', 'pasien1', 'pasien123', 'pasien');

-- Data Dummy Penyakit
INSERT INTO tb_penyakit (kode_penyakit, nama_penyakit, deskripsi, solusi_pengobatan) VALUES 
('P01', 'Panu (Tinea Versikolor)', 'Infeksi jamur pada kulit yang ditandai dengan bercak berwarna lebih terang atau lebih gelap dari kulit sekitar.', 'Gunakan krim antijamur seperti clotrimazole atau miconazole.'),
('P02', 'Herpes (Herpes Simpleks)', 'Penyakit akibat infeksi virus HSV yang ditandai dengan lepuhan kecil berisi cairan.', 'Gunakan salep antivirus seperti acyclovir sesuai resep dokter.'),
('P03', 'Kutil (Warts)', 'Infeksi kulit akibat human papillomavirus (HPV) yang menyebabkan benjolan kasar pada kulit.', 'Gunakan obat kutil yang mengandung asam salisilat atau tindakan medis (krioterapi).'),
('P04', 'Jerawat (Acne Vulgaris)', 'Kondisi kulit yang terjadi ketika folikel rambut tersumbat oleh minyak dan sel kulit mati.', 'Bersihkan wajah secara rutin, gunakan krim benzoil peroksida atau asam salisilat.');

-- Data Dummy Gejala
INSERT INTO tb_gejala (kode_gejala, nama_gejala) VALUES 
('G01', 'Muncul bercak putih/coklat (Panu)'),
('G02', 'Kulit gatal saat berkeringat'),
('G03', 'Permukaan kulit tampak bersisik'),
('G04', 'Muncul lepuhan kecil berisi cairan (Herpes)'),
('G05', 'Lesi terasa nyeri, panas, terbakar'),
('G06', 'Muncul benjolan kecil kasar (Kutil)'),
('G07', 'Permukaan benjolan keras/menebal'),
('G08', 'Timbul komedo / jerawat papula');

-- Data Dummy Aturan CF (Pakar)
-- Rumus: CF Pakar = MB - MD
INSERT INTO tb_aturan_cf (kode_penyakit, kode_gejala, mb, md) VALUES 
-- Aturan Panu (P01)
('P01', 'G01', 0.8, 0.1),
('P01', 'G02', 0.7, 0.2),
('P01', 'G03', 0.6, 0.2),

-- Aturan Herpes (P02)
('P02', 'G04', 0.9, 0.1),
('P02', 'G05', 0.8, 0.2),

-- Aturan Kutil (P03)
('P03', 'G06', 0.8, 0.1),
('P03', 'G07', 0.7, 0.1),

-- Aturan Jerawat (P04)
('P04', 'G08', 0.9, 0.1);
