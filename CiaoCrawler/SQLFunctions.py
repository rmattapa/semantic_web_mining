import pymysql
import SQLConnect
pymysql.install_as_MySQLdb()


def add_user(conn, id, name, is_deleted, is_scanned):
        if is_deleted:
            del_str = "TRUE"
        else:
            del_str = "FALSE"
        if is_scanned:
            scan_str = "TRUE"
        else:
            scan_str = "FALSE"
        query = "insert into userinfo(id,name,deleted,scanned) "\
                " select * from(select "+str(id)+",'"+name+"',"+del_str+", "+scan_str+") as tmp "\
                " WHERE NOT EXISTS(select id from userinfo where id = "+str(id)+") LIMIT 1;"
        #print(query);
        SQLConnect.mysql_execute(conn, query)
        return conn


def add_new_user(conn, id, name, is_deleted, is_scanned):
        if is_deleted:
            del_str = "TRUE"
        else:
            del_str = "FALSE"
        if is_scanned:
            scan_str = "TRUE"
        else:
            scan_str = "FALSE"
        query = "INSERT into userinfo(id, name, deleted, scanned) values("+str(id)+",'"+str(name)\
                + "',"+del_str+","+scan_str+")"
        #print(query)
        SQLConnect.mysql_execute(conn, query)
        return conn



def getUserCount(conn):
    query = "select count(*) from userinfo;"
    cur = SQLConnect.mysql_select_query(conn, query)
    count = cur.fetchone()[0];
    cur.close()
    return count


def does_user_exists(conn, user_id):
    query = "select id from userinfo where id = "+str(user_id)
    cur = SQLConnect.mysql_select_query(conn, query)
    res = cur.fetchone()
    cur.close()
    if res is None:
        return False
    else:
        return True


def get_next_unused_id(conn, start_val=None):
    query = "SELECT MIN( t1.id +1 ) AS nextID\
    FROM userinfo t1\
    LEFT JOIN userinfo t2 ON t1.id +1 = t2.id\
    WHERE t2.id IS NULL"
    if start_val:
        query += " and t1.id > "+str(start_val)
    cur = SQLConnect.mysql_select_query(conn, query)
    next_free_id = cur.fetchone()[0]
    query = "select id from userinfo where id > "+str(next_free_id)+" order by id limit 1"
    cur = SQLConnect.mysql_select_query(conn,query)
    next_id = cur.fetchone()[0]
    cur.close()
    return next_free_id, next_id


def get_all_users(conn):
    query = "select id, name from userinfo"
    cur = SQLConnect.mysql_select_query(conn, query)
    res = cur.fetchall()
    cur.close()
    return res


def get_all_non_scanned_users(conn):
    query = "select id, name from userinfo where deleted=FALSE and scanned=FALSE"
    cur = SQLConnect.mysql_select_query(conn, query)
    res = cur.fetchall()
    cur.close()
    return res


def delete_user(conn, user_id):
    query = "delete from userinfo where id="+str(user_id)
    SQLConnect.mysql_execute(conn, query)
    return


def update_scanned(conn, user_id):
    query = "update userinfo set scanned=TRUE where id="+str(user_id)
    SQLConnect.mysql_execute(conn, query)
    return