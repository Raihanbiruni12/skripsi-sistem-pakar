import pymysql

try:
    conn = pymysql.connect(host='localhost', user='root', password='', db='db_pakar_kulit')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tb_user WHERE username='pasien1'")
    conn.commit()
    conn.close()
    print("User pasien1 deleted")
except Exception as e:
    print(f"Error: {e}")
