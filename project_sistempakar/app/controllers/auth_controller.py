from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from app.models.db import Database
from app.models.user import UserFactory

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'role' in session:
        if session['role'] == 'admin':
            return redirect(url_for('admin.admin_dashboard_view'))
        elif session['role'] == 'pasien':
            return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        nama_lengkap = request.form.get('nama_lengkap')
        username = request.form.get('username')
        password = request.form.get('password')
        role = 'pasien' # Default role untuk semua registrasi publik

        hashed_password = generate_password_hash(password)

        conn = Database.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO tb_user (nama_lengkap, username, password, role) VALUES (%s, %s, %s, %s)", (nama_lengkap, username, hashed_password, role))
            conn.commit()
            flash("Registrasi berhasil! Silakan login.", "success")
            return redirect(url_for('auth.login'))
        except pymysql.err.IntegrityError:
            flash("Username sudah digunakan. Silakan pilih yang lain.", "danger")
        except Exception as e:
            conn.rollback()
            flash(f"Gagal registrasi: {str(e)}", "danger")
        finally:
            conn.close()
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'role' in session:
        if session['role'] == 'admin':
            return redirect(url_for('admin.admin_dashboard_view'))
        elif session['role'] == 'pasien':
            return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tb_user WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data and check_password_hash(user_data['password'], password):
            # Menggunakan OOP Factory untuk membuat objek user
            user_obj = UserFactory.create_user(user_data)
            
            # Simpan data ke session
            session['id_user'] = user_obj.id_user
            session['username'] = user_obj.username
            session['role'] = user_obj.role
            session['nama_lengkap'] = user_obj.nama_lengkap
            session['foto_profil'] = user_data.get('foto_profil')
            
            flash(f"Selamat datang, {user_obj.nama_lengkap}!", "success")
            
            # Polymorphic routing: rute ditentukan oleh class masing-masing (AdminUser/PasienUser)
            return redirect(url_for(user_obj.get_dashboard_url()))
        else:
            flash("Username atau password salah.", "danger")
            
    return render_template('auth/login.html', input_username=request.form.get('username') if request.method == 'POST' else '')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Anda berhasil logout.", "success")
    return redirect(url_for('auth.login'))

@auth_bp.route('/lupa_password', methods=['GET', 'POST'])
def lupa_password():
    # Jika sudah login, arahkan kembali ke dashboard (tidak boleh akses lupa password)
    if 'role' in session:
        if session['role'] == 'admin':
            return redirect(url_for('admin.admin_dashboard_view'))
        elif session['role'] == 'pasien':
            return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        nama_lengkap = request.form.get('nama_lengkap')
        new_password = request.form.get('new_password')

        conn = Database.get_connection()
        cursor = conn.cursor()
        
        try:
            # Cari user yang cocok
            cursor.execute("SELECT id_user FROM tb_user WHERE username = %s AND nama_lengkap = %s", (username, nama_lengkap))
            user = cursor.fetchone()
            
            if user:
                # Hash password baru
                hashed_password = generate_password_hash(new_password)
                
                # Update password
                cursor.execute("UPDATE tb_user SET password = %s WHERE id_user = %s", (hashed_password, user['id_user']))
                conn.commit()
                
                # Bersihkan session untuk memastikan harus login ulang dengan password baru
                session.clear()
                
                flash("Password berhasil diubah! Silakan login dengan password baru.", "success")
                return redirect(url_for('auth.login'))
            else:
                flash("Username atau Nama Lengkap tidak cocok dengan data kami.", "danger")
        except Exception as e:
            conn.rollback()
            flash(f"Terjadi kesalahan: {str(e)}", "danger")
        finally:
            conn.close()
            
    return render_template('auth/forgot_password.html')
