import pymysql

def _mysql(sql):
    # 打开并配置数据库
    #conn = pymysql.connect(
    #    host='localhost',
    #    db='sql_order',
    #    port=3306,
    #    user='root',
    #    passwd='123456',
    #    charset='utf8'
    #)
    conn = pymysql.connect(
        host='115.159.198.77',
        db='AiTaoDB',
        port=3306,
        user='root',
        passwd='jlmz208',
        charset='utf8'
    )
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        # 提交数据库
        conn.commit()
        print('数据保存成功')
    except Exception as e:
        print(e)
        print('数据保存失败')
    else:
        return cursor.fetchall()
    finally:
        conn.close()