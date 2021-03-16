import psycopg2
import psycopg2.extras as ext 


def run_sql(sql, values = None):
    conn = None
    results = [] #results is a list of dictonary type items.

    try: 
        # connect creates a db connection
        conn = psycopg2.connect("dbname='task_manager'")
        # conn.cursor() creates a cursor responsible for executing our queries
        cur = conn.cursor(cursor_factory=ext.DictCursor)
        # execute will run the sql query with apropriate values
        cur.execute(sql, values)
        # commit will finalise our transaction created above
        conn.commit()
        # fetchall will return all results from our sql query above
        results = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)     
    finally:
        if conn is not None:
            conn.close()
    return results         