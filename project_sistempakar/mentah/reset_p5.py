import pymysql

try:
    conn = pymysql.connect(host='localhost', user='root', password='', db='db_pakar_kulit')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tb_penyakit WHERE kode_penyakit='P05'")
    conn.commit()
    conn.close()
    print("Penyakit P05 deleted")
except Exception as e:
    print(f"Error: {e}")
