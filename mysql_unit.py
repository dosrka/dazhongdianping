import pymysql


def connect_rule():
    """
    定义需要链接的数据库
    :return:
    """
    conn = pymysql.connect(host="192.168.2.137",
                           port=3306,
                           user="root",
                           passwd="123456",
                           db="dazhongdianping",
                           charset="utf8")
    return conn


def excute_sql(content):
    conn = connect_rule()
    cursor = conn.cursor()
    sql = "INSERT INTO dazhong (店名, 星级, 菜系, 人均价格, 点评人数, 所在区域) VALUES (%s, %s, %s, %s, %s, %s)"
    print(content)
    cursor.execute(sql, content)
    conn.commit()
    cursor.close()
    conn.close()


def insert_sql(s):
    for key in s:
        list_a = s[key]
        list_a.insert(0, key)
        try:
            excute_sql(list_a)
        except:
            print("插入失败")
