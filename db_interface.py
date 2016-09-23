__author__ = 'aschwartz - Schwartz210@gmail.com'
from sqlite3 import connect
DATABASE = 'test.db'

def execute_sql(SQL_request):
    '''
    Alter database. Does not query data.
    '''
    conn = connect(DATABASE)
    c = conn.cursor()
    c.execute(SQL_request)
    conn.commit()
    conn.close()

def exists(sql_request):
    '''
    Evualuate if record exists. Returns boolean.
    '''
    conn = connect(DATABASE)
    c = conn.cursor()
    count = len(list(c.execute(sql_request)))
    if count > 0:
        out = True
    else:
        out = False
    conn.commit()
    conn.close()
    return out

def pull_data(SQL_request):
    conn = connect(DATABASE)
    c = conn.cursor()
    try:
        out = list(c.execute(SQL_request))
        conn.commit()
        conn.close()
        return out
    except:
        raise Exception('Not able to fulfill request')

def add_record(record):
    text = 'INSERT INTO test_table4 VALUES(NULL, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7])
    execute_sql(text)


def update_record(values):
    sql_request = 'UPDATE test_table4 SET First_name="%s", Last_name="%s", Address1="%s", Address2="%s", City="%s", ' \
                  'State="%s", Zip="%s", Phone="%s" WHERE ID="%s"' % (values[0],
                                                                      values[1],
                                                                      values[2],
                                                                      values[3],
                                                                      values[4],
                                                                      values[5],
                                                                      values[6],
                                                                      values[7],
                                                                      values[8])
    execute_sql(sql_request)

'''
conn = connect(DATABASE)
c = conn.cursor()
text = 'UPDATE test_table4 SET Phone="555555" WHERE ID="2"'
c.execute(text)
conn.commit()
conn.close()
'''