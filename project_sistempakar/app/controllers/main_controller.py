from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from functools import wraps
from app.models.db import Database

main_bp = Blueprint('main', __name__)

def pasien_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'pasien':
            flash("Akses ditolak! Anda harus login sebagai Pasien.", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def get_penyakit_info():
    """Mengambil data master penyakit dari database."""
    conn = Database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT kode_penyakit, nama_penyakit, solusi_pengobatan FROM tb_penyakit")
    result = cursor.fetchall()
    conn.close()
    return {row['kode_penyakit']: {"nama": row['nama_penyakit'], "solusi": row['solusi_pengobatan']} for row in result}

def get_aturan_cf():
    """Mengambil data aturan CF (MB dan MD) dari database."""
    conn = Database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT kode_penyakit, kode_gejala, mb, md FROM tb_aturan_cf")
    result = cursor.fetchall()
    conn.close()
    
    aturan_cf = {}
    for row in result:
        kp = row['kode_penyakit']
        kg = row['kode_gejala']
        mb = row['mb']
        md = row['md']
        if kp not in aturan_cf:
            aturan_cf[kp] = {}
        aturan_cf[kp][kg] = (mb, md)
    return aturan_cf

@main_bp.route('/')
def index():
    # Jika sudah login, arahkan ke dashboard masing-masing
    if 'role' in session:
        if session['role'] == 'admin':
            return redirect(url_for('admin.admin_dashboard_view'))
        elif session['role'] == 'pasien':
            return redirect(url_for('main.dashboard'))
            
    # Jika belum login, tampilkan landing page
    return render_template('main/landing.html')

@main_bp.route('/diagnosis')
def diagnosis():
    conn = Database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_gejala ORDER BY kode_gejala")
    gejala = cursor.fetchall()
    conn.close()
    return render_template('main/index.html', gejala=gejala)

@main_bp.route('/proses_diagnosis', methods=['POST'])
def proses_diagnosis():
    data = request.json
    
    # Menerima data dari JS (Fetch)
    ai_prediction = data.get('ai_prediction', {}) # Cth: {"P01": 0.8, "P02": 0.1, ...}
    gejala_user = data.get('gejala', []) # Cth: [{"kode_gejala": "G01", "cf_user": 0.8}, ...]

    # Ambil data dinamis dari database MySQL
    try:
        penyakit_info = get_penyakit_info()
        aturan_cf = get_aturan_cf()
    except Exception as e:
        print("Error koneksi database:", e)
        return jsonify({"status": "error", "message": "Gagal terhubung ke database. Pastikan MySQL berjalan."}), 500

    # ==========================================
    # 1. PERHITUNGAN CERTAINTY FACTOR (PAKAR)
    # ==========================================
    hasil_cf = {}
    for kode_penyakit, aturan in aturan_cf.items():
        cf_combine = 0.0
        is_first = True
        
        for g in gejala_user:
            kode_g = g['kode_gejala']
            cf_user = float(g['cf_user'])
            
            # Jika gejala yang dipilih user ada di aturan penyakit ini
            if kode_g in aturan:
                mb, md = aturan[kode_g]
                cf_pakar = mb - md
                cf_gejala = cf_pakar * cf_user
                
                # Rumus CF Combine
                if is_first:
                    cf_combine = cf_gejala
                    is_first = False
                else:
                    cf_combine = cf_combine + (cf_gejala * (1 - cf_combine))
                    
        hasil_cf[kode_penyakit] = cf_combine

    # Mencari penyakit dengan CF tertinggi
    if not hasil_cf or max(hasil_cf.values()) == 0:
        cf_tertinggi = 0
        penyakit_cf_kode = None
    else:
        penyakit_cf_kode = max(hasil_cf, key=hasil_cf.get)
        cf_tertinggi = hasil_cf[penyakit_cf_kode]

    # ==========================================
    # 2. PROSES HASIL AI
    # ==========================================
    if not ai_prediction:
        prob_ai_tertinggi = 0
        penyakit_ai_kode = None
    else:
        # Mencari probabilitas prediksi tertinggi dari MobileNetV2
        penyakit_ai_kode = max(ai_prediction, key=ai_prediction.get)
        prob_ai_tertinggi = ai_prediction[penyakit_ai_kode]

    # ==========================================
    # 3. VALIDASI HIBRIDA (AI & CF PAKAR)
    # ==========================================
    kesimpulan = ""
    persentase_akhir = 0.0
    
    if penyakit_cf_kode and penyakit_cf_kode == penyakit_ai_kode:
        kesimpulan = f"Validasi Kuat! AI dan Gejala Klinis mengarah pada penyakit yang sama: {penyakit_info[penyakit_cf_kode]['nama']}."
        # Rata-rata dari nilai CF dan AI
        persentase_akhir = (cf_tertinggi + prob_ai_tertinggi) / 2
    elif penyakit_cf_kode and penyakit_ai_kode:
        kesimpulan = f"Perbedaan Deteksi: AI mendeteksi {penyakit_info[penyakit_ai_kode]['nama']} ({prob_ai_tertinggi*100:.1f}%), sedangkan kondisi gejala menunjukkan kecenderungan {penyakit_info[penyakit_cf_kode]['nama']} ({cf_tertinggi*100:.1f}%)."
        # Ambil bobot dominan (Misal: 60% Pakar, 40% AI)
        persentase_akhir = (cf_tertinggi * 0.6) + (prob_ai_tertinggi * 0.4)
    else:
        kesimpulan = "Data tidak mencukupi untuk melakukan diagnosis hibrida."

    # ==========================================
    # 4. PENENTUAN PENYAKIT AKHIR (PRIORITAS PAKAR 60%)
    # ==========================================
    final_kode_penyakit = penyakit_cf_kode if penyakit_cf_kode else penyakit_ai_kode

    # ==========================================
    # 5. SIMPAN KE DATABASE
    # ==========================================
    try:
        from datetime import datetime
        import random
        from flask import session
        
        now = datetime.now()
        id_riwayat = f"R-{now.strftime('%Y%m%d')}-{random.randint(100,999)}"
        tanggal = now.strftime('%Y-%m-%d %H:%M:%S')
        id_user = session.get('id_user')
        
        if final_kode_penyakit:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            # Simpan data riwayat utama
            cursor.execute("""
                INSERT INTO tb_riwayat_diagnosis (id_riwayat, id_user, tanggal, kode_penyakit_hasil, persentase_akhir)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_riwayat, id_user, tanggal, final_kode_penyakit, round(persentase_akhir * 100, 2)))
            
            # Simpan detail gejala yang dipilih
            for g in gejala_user:
                cursor.execute("""
                    INSERT INTO tb_detail_diagnosis (id_riwayat, kode_gejala, cf_user)
                    VALUES (%s, %s, %s)
                """, (id_riwayat, g['kode_gejala'], g['cf_user']))
                
            conn.commit()
            conn.close()
    except Exception as e:
        print("Gagal menyimpan riwayat:", e)

    return jsonify({
        "status": "success",
        "cf_result": {
            "kode": penyakit_cf_kode,
            "nama": penyakit_info.get(penyakit_cf_kode, {}).get("nama", "Tidak Diketahui"),
            "persentase": round(cf_tertinggi * 100, 2)
        },
        "ai_result": {
            "kode": penyakit_ai_kode,
            "nama": penyakit_info.get(penyakit_ai_kode, {}).get("nama", "Tidak Diketahui"),
            "persentase": round(prob_ai_tertinggi * 100, 2)
        },
        "hybrid_result": {
            "kode_akhir": final_kode_penyakit,
            "nama_akhir": penyakit_info.get(final_kode_penyakit, {}).get("nama", "Tidak Diketahui"),
            "kesimpulan": kesimpulan,
            "solusi": penyakit_info.get(final_kode_penyakit, {}).get("solusi", "Silakan konsultasikan dengan dokter untuk penanganan lebih lanjut."),
            "persentase_akhir": round(persentase_akhir * 100, 2)
        }
    })
@main_bp.route('/dashboard')
@pasien_required
def dashboard():
    id_user = session.get('id_user')
    conn = Database.get_connection()
    cursor = conn.cursor()
    
    # Get total diagnosa
    cursor.execute("SELECT COUNT(*) as total FROM tb_riwayat_diagnosis WHERE id_user = %s", (id_user,))
    total_diagnosa = cursor.fetchone()['total']
    
    # Get rata-rata keyakinan
    cursor.execute("SELECT AVG(persentase_akhir) as avg_cf FROM tb_riwayat_diagnosis WHERE id_user = %s", (id_user,))
    avg_cf = cursor.fetchone()['avg_cf']
    avg_cf = round(avg_cf, 1) if avg_cf else 0
    
    # Get penyakit terbanyak
    cursor.execute("""
        SELECT p.nama_penyakit, COUNT(r.kode_penyakit_hasil) as count 
        FROM tb_riwayat_diagnosis r
        JOIN tb_penyakit p ON r.kode_penyakit_hasil = p.kode_penyakit
        WHERE r.id_user = %s
        GROUP BY r.kode_penyakit_hasil
        ORDER BY count DESC LIMIT 1
    """, (id_user,))
    penyakit_terbanyak = cursor.fetchone()
    penyakit_terbanyak_nama = penyakit_terbanyak['nama_penyakit'] if penyakit_terbanyak else '-'
    
    # Get tanggal diagnosa terakhir
    cursor.execute("SELECT DATE_FORMAT(tanggal, '%%d %%M %%Y') as last_date FROM tb_riwayat_diagnosis WHERE id_user = %s ORDER BY tanggal DESC LIMIT 1", (id_user,))
    last_date_row = cursor.fetchone()
    last_date = last_date_row['last_date'] if last_date_row else '-'
    
    # Get 10 riwayat terbaru
    cursor.execute("""
        SELECT r.id_riwayat, p.nama_penyakit, DATE_FORMAT(r.tanggal, '%%Y-%%m-%%d') as tanggal, r.persentase_akhir
        FROM tb_riwayat_diagnosis r
        JOIN tb_penyakit p ON r.kode_penyakit_hasil = p.kode_penyakit
        WHERE r.id_user = %s
        ORDER BY r.tanggal DESC LIMIT 10
    """, (id_user,))
    recent_history = cursor.fetchall()
    
    conn.close()
    
    stats = {
        'total': total_diagnosa,
        'avg_cf': avg_cf,
        'terbanyak': penyakit_terbanyak_nama,
        'last_date': last_date
    }
    
    return render_template('main/dashboard.html', stats=stats, recent_history=recent_history)

@main_bp.route('/riwayat')
@pasien_required
def history():
    id_user = session.get('id_user')
    conn = Database.get_connection()
    cursor = conn.cursor()
    
    # 1. Fetch all diagnosis history for the user
    cursor.execute("""
        SELECT r.id_riwayat, DATE_FORMAT(r.tanggal, '%%Y-%%m-%%d %%H:%%i') as tanggal_format,
               r.tanggal, p.nama_penyakit, r.persentase_akhir
        FROM tb_riwayat_diagnosis r
        JOIN tb_penyakit p ON r.kode_penyakit_hasil = p.kode_penyakit
        WHERE r.id_user = %s
        ORDER BY r.tanggal DESC
    """, (id_user,))
    riwayat_list = cursor.fetchall()
    
    # 2. Group details by id_riwayat to display in modals
    riwayat_details = {}
    if riwayat_list:
        # Get all details for these records
        ids = [row['id_riwayat'] for row in riwayat_list]
        format_strings = ','.join(['%s'] * len(ids))
        cursor.execute(f"""
            SELECT d.id_riwayat, g.nama_gejala, d.cf_user
            FROM tb_detail_diagnosis d
            JOIN tb_gejala g ON d.kode_gejala = g.kode_gejala
            WHERE d.id_riwayat IN ({format_strings})
        """, tuple(ids))
        details_list = cursor.fetchall()
        
        for det in details_list:
            r_id = det['id_riwayat']
            if r_id not in riwayat_details:
                riwayat_details[r_id] = []
            riwayat_details[r_id].append({
                'gejala': det['nama_gejala'],
                'cf_user': round(det['cf_user'] * 100, 1) # convert to percentage
            })
            
    conn.close()
    
    return render_template('main/history.html', riwayat_list=riwayat_list, riwayat_details=riwayat_details)

    # Fitur delete_history untuk pasien telah dinonaktifkan demi keamanan rekam medis

@main_bp.route('/profil', methods=['GET', 'POST'])
@pasien_required
def profil():
    from werkzeug.security import generate_password_hash
    if request.method == 'POST':
        action = request.form.get('action')
        id_user = session.get('id_user')
        
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        if action == 'update_profile':
            nama = request.form.get('nama_lengkap')
            username = request.form.get('username')
            try:
                cursor.execute("UPDATE tb_user SET nama_lengkap=%s, username=%s WHERE id_user=%s", (nama, username, id_user))
                conn.commit()
                # Update session
                session['nama_lengkap'] = nama
                session['username'] = username
                flash("Profil berhasil diperbarui!", "success")
            except Exception as e:
                conn.rollback()
                flash("Gagal memperbarui profil. Username mungkin sudah digunakan.", "danger")
                
        elif action == 'change_password':
            password_baru = request.form.get('password_baru')
            hashed_pw = generate_password_hash(password_baru)
            try:
                cursor.execute("UPDATE tb_user SET password=%s WHERE id_user=%s", (hashed_pw, id_user))
                conn.commit()
                flash("Kata sandi berhasil diubah! Silakan login kembali.", "success")
                session.clear()
                conn.close()
                return redirect(url_for('auth.login'))
            except Exception as e:
                conn.rollback()
                flash("Gagal mengubah kata sandi.", "danger")
                
        elif action == 'upload_photo':
            import os
            import uuid
            
            if 'foto_profil' in request.files:
                file = request.files['foto_profil']
                if file and file.filename != '':
                    try:
                        # Buat folder jika belum ada
                        upload_folder = os.path.join('static', 'uploads', 'profiles')
                        if not os.path.exists(upload_folder):
                            os.makedirs(upload_folder)
                            
                        # Generate nama file unik
                        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
                        filename = f"profile_{id_user}_{uuid.uuid4().hex[:8]}.{ext}"
                        filepath = os.path.join(upload_folder, filename)
                        
                        # Simpan file
                        file.save(filepath)
                        
                        # Hapus foto lama jika ada (opsional, tapi baik untuk storage)
                        old_photo = session.get('foto_profil')
                        if old_photo:
                            old_path = os.path.join('static', 'uploads', 'profiles', old_photo)
                            if os.path.exists(old_path):
                                os.remove(old_path)
                                
                        # Update database
                        cursor.execute("UPDATE tb_user SET foto_profil=%s WHERE id_user=%s", (filename, id_user))
                        conn.commit()
                        
                        # Update session
                        session['foto_profil'] = filename
                        
                        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                            return jsonify({'success': True, 'message': 'Foto profil berhasil diperbarui!', 'filename': filename})
                        else:
                            flash("Foto profil berhasil diperbarui!", "success")
                    except Exception as e:
                        conn.rollback()
                        print("Error uploading photo:", e)
                        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                            return jsonify({'success': False, 'message': 'Gagal mengunggah foto profil.'}), 500
                        else:
                            flash("Gagal mengunggah foto profil.", "danger")
                else:
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return jsonify({'success': False, 'message': 'File tidak valid.'}), 400
                        
        conn.close()
        return redirect(url_for('main.profil'))
        
    return render_template('main/profil.html', active_page='profil')

@main_bp.route('/pengaturan')
@pasien_required
def pengaturan():
    return render_template('main/pengaturan.html', active_page='pengaturan')

@main_bp.route('/api/notifications')
@pasien_required
def get_notifications():
    id_user = session.get('id_user')
    conn = Database.get_connection()
    cursor = conn.cursor(dictionary=True)
    notifications = []
    try:
        # Cari diagnosa terakhir
        cursor.execute("""
            SELECT r.id_riwayat, r.tanggal, p.nama_penyakit 
            FROM tb_riwayat_diagnosis r
            JOIN tb_penyakit p ON r.kode_penyakit_hasil = p.kode_penyakit
            WHERE r.id_user = %s
            ORDER BY r.tanggal DESC LIMIT 1
        """, (id_user,))
        last_diag = cursor.fetchone()
        
        if last_diag:
            from datetime import datetime, timedelta
            waktu_diagnosa = last_diag['tanggal']
            sekarang = datetime.now()
            
            # Jika sudah lebih dari 5 menit (untuk simulasi) -> 7 hari aslinya
            if sekarang - waktu_diagnosa > timedelta(minutes=5):
                notifications.append({
                    'id': last_diag['id_riwayat'],
                    'title': 'Evaluasi Kondisi Kulit',
                    'message': f"Halo! Anda terdiagnosis {last_diag['nama_penyakit']} beberapa waktu lalu. Bagaimana kondisi kulit Anda sekarang? Jangan lupa pengobatan rutin!",
                    'time': waktu_diagnosa.strftime('%d %b %Y, %H:%M')
                })
    except Exception as e:
        print("Error fetch notifications:", e)
    finally:
        conn.close()
        
    return jsonify(notifications)
