from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from app.models.db import Database
from app.utils.settings import get_settings, save_settings

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            flash("Akses ditolak! Anda harus login sebagai Admin.", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# ==========================================
# RUTING HALAMAN ADMIN
# ==========================================

@admin_bp.route('/admin')
@admin_required
def admin_dashboard():
    conn = Database.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tb_penyakit")
    penyakit_list = cursor.fetchall()
    
    cursor.execute("SELECT * FROM tb_gejala")
    gejala_list = cursor.fetchall()
    
    conn.close()
    return render_template('admin/admin.html', penyakit=penyakit_list, gejala=gejala_list, active_page='master')

# --- CRUD PENYAKIT ---

@admin_bp.route('/admin/penyakit/add', methods=['POST'])
@admin_required
def add_penyakit():
    kode = request.form.get('kode_penyakit')
    nama = request.form.get('nama_penyakit')
    desc = request.form.get('deskripsi')
    solusi = request.form.get('solusi_pengobatan')
    
    conn = Database.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO tb_penyakit (kode_penyakit, nama_penyakit, deskripsi, solusi_pengobatan) VALUES (%s, %s, %s, %s)", (kode, nama, desc, solusi))
        conn.commit()
        flash("Penyakit berhasil ditambahkan!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Gagal menambah penyakit: {str(e)}", "danger")
    finally:
        conn.close()
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/penyakit/edit/<kode>', methods=['POST'])
@admin_required
def edit_penyakit(kode):
    nama = request.form.get('nama_penyakit')
    desc = request.form.get('deskripsi')
    solusi = request.form.get('solusi_pengobatan')
    
    conn = Database.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE tb_penyakit SET nama_penyakit=%s, deskripsi=%s, solusi_pengobatan=%s WHERE kode_penyakit=%s", (nama, desc, solusi, kode))
        conn.commit()
        flash("Penyakit berhasil diperbarui!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Gagal memperbarui penyakit: {str(e)}", "danger")
    finally:
        conn.close()
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/penyakit/delete/<kode>', methods=['POST'])
@admin_required
def delete_penyakit(kode):
    conn = Database.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tb_penyakit WHERE kode_penyakit=%s", (kode,))
        conn.commit()
        flash("Penyakit berhasil dihapus!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Gagal menghapus penyakit: {str(e)}", "danger")
    finally:
        conn.close()
    return redirect(url_for('admin.admin_dashboard'))

# --- CRUD GEJALA ---

@admin_bp.route('/admin/gejala/add', methods=['POST'])
@admin_required
def add_gejala():
    kode = request.form.get('kode_gejala')
    nama = request.form.get('nama_gejala')
    
    conn = Database.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO tb_gejala (kode_gejala, nama_gejala) VALUES (%s, %s)", (kode, nama))
        conn.commit()
        flash("Gejala berhasil ditambahkan!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Gagal menambah gejala: {str(e)}", "danger")
    finally:
        conn.close()
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/gejala/edit/<kode>', methods=['POST'])
@admin_required
def edit_gejala(kode):
    nama = request.form.get('nama_gejala')
    
    conn = Database.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE tb_gejala SET nama_gejala=%s WHERE kode_gejala=%s", (nama, kode))
        conn.commit()
        flash("Gejala berhasil diperbarui!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Gagal memperbarui gejala: {str(e)}", "danger")
    finally:
        conn.close()
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/gejala/delete/<kode>', methods=['POST'])
@admin_required
def delete_gejala(kode):
    conn = Database.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tb_gejala WHERE kode_gejala=%s", (kode,))
        conn.commit()
        flash("Gejala berhasil dihapus!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Gagal menghapus gejala: {str(e)}", "danger")
    finally:
        conn.close()
    return redirect(url_for('admin.admin_dashboard'))

# --- CRUD ATURAN CF ---

@admin_bp.route('/admin/cf')
@admin_required
def admin_cf():
    conn = Database.get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT a.id_rule, p.kode_penyakit, p.nama_penyakit, g.kode_gejala, g.nama_gejala, a.mb, a.md
        FROM tb_aturan_cf a
        JOIN tb_penyakit p ON a.kode_penyakit = p.kode_penyakit
        JOIN tb_gejala g ON a.kode_gejala = g.kode_gejala
        ORDER BY p.kode_penyakit, g.kode_gejala
    """
    cursor.execute(query)
    rules_list = cursor.fetchall()
    
    cursor.execute("SELECT kode_penyakit, nama_penyakit FROM tb_penyakit")
    penyakit_list = cursor.fetchall()
    
    cursor.execute("SELECT kode_gejala, nama_gejala FROM tb_gejala")
    gejala_list = cursor.fetchall()
    
    conn.close()
    return render_template('admin/admin_cf.html', rules=rules_list, penyakit=penyakit_list, gejala=gejala_list, active_page='cf')

@admin_bp.route('/admin/cf/add', methods=['POST'])
@admin_required
def add_cf():
    kode_penyakit = request.form.get('kode_penyakit')
    kode_gejala = request.form.get('kode_gejala')
    mb = float(request.form.get('mb'))
    md = float(request.form.get('md'))
    
    conn = Database.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO tb_aturan_cf (kode_penyakit, kode_gejala, mb, md) VALUES (%s, %s, %s, %s)", (kode_penyakit, kode_gejala, mb, md))
        conn.commit()
        flash("Aturan CF berhasil ditambahkan!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Gagal menambah aturan: {str(e)}", "danger")
    finally:
        conn.close()
    return redirect(url_for('admin.admin_cf'))

@admin_bp.route('/admin/cf/edit/<int:id_rule>', methods=['POST'])
@admin_required
def edit_cf(id_rule):
    kode_penyakit = request.form.get('kode_penyakit')
    kode_gejala = request.form.get('kode_gejala')
    mb = float(request.form.get('mb'))
    md = float(request.form.get('md'))
    
    conn = Database.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE tb_aturan_cf SET kode_penyakit=%s, kode_gejala=%s, mb=%s, md=%s WHERE id_rule=%s", (kode_penyakit, kode_gejala, mb, md, id_rule))
        conn.commit()
        flash("Aturan CF berhasil diperbarui!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Gagal memperbarui aturan: {str(e)}", "danger")
    finally:
        conn.close()
    return redirect(url_for('admin.admin_cf'))

@admin_bp.route('/admin/cf/delete/<int:id_rule>', methods=['POST'])
@admin_required
def delete_cf(id_rule):
    conn = Database.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tb_aturan_cf WHERE id_rule=%s", (id_rule,))
        conn.commit()
        flash("Aturan CF berhasil dihapus!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Gagal menghapus aturan: {str(e)}", "danger")
    finally:
        conn.close()
    return redirect(url_for('admin.admin_cf'))

@admin_bp.route('/admin/laporan/cetak')
@admin_required
def cetak_laporan():
    filter_penyakit = request.args.get('penyakit', '')
    search = request.args.get('search', '')
    
    conn = Database.get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT r.id_riwayat as id, r.id_user as id_user, u.nama_lengkap as user, DATE_FORMAT(r.tanggal, '%%Y-%%m-%%d') as tanggal, 
               p.nama_penyakit as penyakit, r.persentase_akhir as final
        FROM tb_riwayat_diagnosis r
        JOIN tb_user u ON r.id_user = u.id_user
        JOIN tb_penyakit p ON r.kode_penyakit_hasil = p.kode_penyakit
        WHERE 1=1
    """
    params = []
    
    if filter_penyakit:
        query += " AND p.kode_penyakit = %s"
        params.append(filter_penyakit)
        
    if search:
        query += " AND (u.nama_lengkap LIKE %s OR r.id_riwayat LIKE %s)"
        params.extend(['%' + search + '%', '%' + search + '%'])
        
    query += " ORDER BY r.tanggal DESC"
    
    cursor.execute(query, tuple(params))
    laporan = cursor.fetchall()
    conn.close()
    
    return render_template('admin/admin_laporan_cetak.html', laporan=laporan)

@admin_bp.route('/admin/laporan')
@admin_required
def admin_laporan():
    filter_penyakit = request.args.get('penyakit', '')
    search = request.args.get('search', '')
    
    conn = Database.get_connection()
    cursor = conn.cursor()
    
    # Query riwayat
    query = """
        SELECT r.id_riwayat as id, r.id_user as id_user, u.nama_lengkap as user, DATE_FORMAT(r.tanggal, '%%Y-%%m-%%d') as tanggal, 
               p.nama_penyakit as penyakit, r.persentase_akhir as final
        FROM tb_riwayat_diagnosis r
        JOIN tb_user u ON r.id_user = u.id_user
        JOIN tb_penyakit p ON r.kode_penyakit_hasil = p.kode_penyakit
        WHERE 1=1
    """
    params = []
    
    if filter_penyakit:
        query += " AND p.kode_penyakit = %s"
        params.append(filter_penyakit)
        
    if search:
        query += " AND (u.nama_lengkap LIKE %s OR r.id_riwayat LIKE %s)"
        params.extend(['%' + search + '%', '%' + search + '%'])
        
    query += " ORDER BY r.tanggal DESC"
    
    cursor.execute(query, tuple(params))
    laporan = cursor.fetchall()
    
    # Ambil daftar penyakit untuk dropdown
    cursor.execute("SELECT kode_penyakit, nama_penyakit FROM tb_penyakit")
    penyakit_list = cursor.fetchall()
    
    # Ambil daftar user pasien untuk Modal Tambah Laporan
    cursor.execute("SELECT id_user, nama_lengkap FROM tb_user WHERE role='pasien'")
    user_list = cursor.fetchall()
    
    # Hitung Statistik
    cursor.execute("SELECT COUNT(*) as total FROM tb_riwayat_diagnosis")
    total_laporan = cursor.fetchone()['total']
    
    cursor.execute("""
        SELECT p.nama_penyakit, COUNT(*) as count 
        FROM tb_riwayat_diagnosis r
        JOIN tb_penyakit p ON r.kode_penyakit_hasil = p.kode_penyakit
        GROUP BY p.kode_penyakit
        ORDER BY count DESC LIMIT 1
    """)
    top_penyakit = cursor.fetchone()
    
    cursor.execute("SELECT AVG(persentase_akhir) as avg_cf FROM tb_riwayat_diagnosis")
    avg_cf = cursor.fetchone()['avg_cf']
    
    stats = {
        'total': total_laporan,
        'teratas': top_penyakit['nama_penyakit'] if top_penyakit else '-',
        'rata_rata': round(avg_cf, 1) if avg_cf else 0
    }
    
    # Data Grafik 1: Distribusi Penyakit (Pie)
    cursor.execute("""
        SELECT p.nama_penyakit, COUNT(*) as count 
        FROM tb_riwayat_diagnosis r
        JOIN tb_penyakit p ON r.kode_penyakit_hasil = p.kode_penyakit
        GROUP BY p.kode_penyakit
    """)
    chart_dist = cursor.fetchall()
    
    # Data Grafik 2: Tren (Line)
    cursor.execute("""
        SELECT DATE_FORMAT(tanggal, '%%Y-%%m-%%d') as tgl, COUNT(*) as count
        FROM tb_riwayat_diagnosis
        GROUP BY DATE_FORMAT(tanggal, '%%Y-%%m-%%d')
        ORDER BY tgl ASC LIMIT 7
    """)
    chart_trend = cursor.fetchall()
    
    # Data Grafik 3: Rata-rata CF (Bar)
    cursor.execute("""
        SELECT p.nama_penyakit, ROUND(AVG(r.persentase_akhir), 1) as avg_cf 
        FROM tb_riwayat_diagnosis r
        JOIN tb_penyakit p ON r.kode_penyakit_hasil = p.kode_penyakit
        GROUP BY p.kode_penyakit
    """)
    chart_avg = cursor.fetchall()
    
    conn.close()
    
    import json
    return render_template('admin/admin_laporan.html', 
                          laporan=laporan, 
                          penyakit_list=penyakit_list,
                          user_list=user_list,
                          stats=stats,
                          chart_dist=json.dumps(chart_dist),
                          chart_trend=json.dumps(chart_trend),
                          chart_avg=json.dumps(chart_avg),
                          active_page='laporan')

    # Fitur add dan edit laporan diagnosis oleh admin telah dihapus 
    # karena riwayat harusnya digenerate secara otomatis oleh sistem saat pasien tes.


@admin_bp.route('/admin/laporan/delete/<id_riwayat>', methods=['POST'])
@admin_required
def delete_laporan(id_riwayat):
    conn = Database.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tb_riwayat_diagnosis WHERE id_riwayat=%s", (id_riwayat,))
        conn.commit()
        flash("Laporan berhasil dihapus!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Gagal menghapus laporan: {str(e)}", "danger")
    finally:
        conn.close()
        
    return redirect(url_for('admin.admin_laporan'))

# --- FUNGSI SIDEBAR LAINNYA ---

@admin_bp.route('/admin/dashboard')
@admin_required
def admin_dashboard_view():
    conn = Database.get_connection()
    cursor = conn.cursor()
    
    # Hitung metrik
    cursor.execute("SELECT COUNT(*) as total FROM tb_penyakit")
    total_penyakit = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM tb_gejala")
    total_gejala = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM tb_aturan_cf")
    total_aturan = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM tb_user")
    total_user = cursor.fetchone()['total']
    
    conn.close()
    
    return render_template('admin/admin_dashboard.html', 
                           total_penyakit=total_penyakit,
                           total_gejala=total_gejala,
                           total_aturan=total_aturan,
                           total_user=total_user,
                           active_page='dashboard')

@admin_bp.route('/admin/profile', methods=['GET', 'POST'])
@admin_required
def admin_profile():
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
                        upload_folder = os.path.join('static', 'uploads', 'profiles')
                        if not os.path.exists(upload_folder):
                            os.makedirs(upload_folder)
                            
                        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
                        filename = f"profile_{id_user}_{uuid.uuid4().hex[:8]}.{ext}"
                        filepath = os.path.join(upload_folder, filename)
                        
                        file.save(filepath)
                        
                        old_photo = session.get('foto_profil')
                        if old_photo:
                            old_path = os.path.join('static', 'uploads', 'profiles', old_photo)
                            if os.path.exists(old_path):
                                os.remove(old_path)
                                
                        cursor.execute("UPDATE tb_user SET foto_profil=%s WHERE id_user=%s", (filename, id_user))
                        conn.commit()
                        
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
        return redirect(url_for('admin.admin_profile'))
        
    return render_template('admin/admin_profile.html', active_page='profile')

@admin_bp.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    if request.method == 'POST':
        new_settings = {
            "nama_sistem": request.form.get('nama_sistem'),
            "email_admin": request.form.get('email_admin'),
            "dark_mode": request.form.get('dark_mode') == 'on',
            "maintenance_mode": request.form.get('maintenance_mode') == 'on'
        }
        save_settings(new_settings)
        flash("Pengaturan sistem berhasil disimpan!", "success")
        return redirect(url_for('admin.admin_settings'))
        
    return render_template('admin/admin_settings.html', active_page='settings')