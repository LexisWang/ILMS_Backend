import os

import pymysql


def _clear_invalid_file():
    # 创建连接对象
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456-abc', database='ILMS',
                           charset='utf8')

    # 获取游标对象
    cursor = conn.cursor()

    sql1 = 'select file_path from b_files where owner is null'
    sql2 = 'delete from b_files where owner is null '

    try:
        cursor.execute(sql1)
        for row in cursor.fetchall():
            os.remove(row[0])
        cursor.execute(sql2)
    except Exception as e:
        conn.rollback()  # 事务回滚
        print('事务处理失败', e)
    else:
        conn.commit()  # 事务提交
        cursor.close()
        conn.close()
        print('事务处理成功')  # 关闭连接


if __name__ == '__main__':
    _clear_invalid_file()
