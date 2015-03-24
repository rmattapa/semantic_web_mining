import pymysql
import SQLConnect
pymysql.install_as_MySQLdb()

def add_user(conn, id, name):
        query = "insert into userinfo(id,name) "\
                " select * from(select "+id+",'"+name+"') as tmp "\
                " WHERE NOT EXISTS(select id from userinfo where id = "+id+") LIMIT 1;";
        #print(query);
        SQLConnect.mysql_execute(conn,query);
        return conn


def getUserCount(conn):
    query = "select count(*) from userinfo;"
    cur = SQLConnect.mysql_select_query(conn,query)
    count = cur.fetchone()[0];
    cur.close()
    return count