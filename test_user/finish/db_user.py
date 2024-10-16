import pymysql

conn = pymysql.connect(host="localhost",database="MYSQL",user='root',
                       password='shudong123',charset='utf8')

cursor = conn.cursor()


def save_in_user_details(data):
    conn = pymysql.connect(host="localhost", database="MYSQL", user='root',
                           password='shudong123', charset='utf8mb4')

    cursor = conn.cursor()
    #达人个人信息表
    insert_sql = ("INSERT INTO user_details_1 VALUES (%s, %s, %s, %s, %s, "
                  "%s,%s, %s, %s, %s,"
                  "%s,%s, %s, %s, %s,  %s)")

    try:
        cursor.execute("USE shudong;")
        cursor.execute(insert_sql, data)
        conn.commit()
        print("数据插入成功！")
    except pymysql.Error as e:
        print(f"数据插入失败：{e}")
    finally:
        cursor.close()
        conn.close()

