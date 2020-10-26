import psycopg2
from table_queries import *
  
def db_connect(dbconfig):

    try:
        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*dbconfig.values()) )
        cur = conn.cursor()
        return conn,cur
    except Exception as err:
        print(f'Exceptions as {err}')


        
def execute_query(conn,cur,query):

    try:
        cur.execute(query)
        conn.commit()
    except Exception as err:
        print(f'Exceptions as {err}')  

def select_query(conn,cur,query):

    try:
        cur.execute(query)
        values = cur.fetchall()
        return values
    except Exception as err:
        print(f'Exceptions as {err}')  

def execute_many(conn,cur,query,rows):

    try:
        cur.executemany(query,rows)
        conn.commit()
    except Exception as err:
        print(f'Exceptions as {err}')  
        




def insert_update_rows(cur,conn,row,df):
    if row == []:
        fields = df.apply(tuple,axis=1).to_list()
        execute_many(conn = conn,cur = cur,query=insert_into,rows=fields)
        cur.close()
        conn.close()
    elif row != [] :
        max_date = select_query(conn = conn,cur = cur,query = select_max_date)
        if max_date != None:
            df_fields = df[df['date'] > str(max_date[0][0])]
            print('no fields to insert')
            if not df_fields.empty:
                fields = df_fields.apply(tuple,axis=1).to_list()
                execute_many(conn = conn,cur = cur,query=insert_into,rows=fields)
                print('fields inserted')  
            recovered_nulls = select_query(conn = conn,cur = cur,query = select_null)
            if recovered_nulls != []:
                null_df = pd.DataFrame(recovered_nulls, 
                        columns = [ 'date', 'cases', 'deaths', 'recovered'])
                null_df['date'] = null_df['date'].astype('datetime64[ns]')

                
                null_df = null_df[['date','recovered']]

                df_null = null_df.merge(df,left_on='date',right_on='date',suffixes=('_left', '_right'))
                
                
                df_null = df_null[df_null['recovered_right'].notnull()]
                
                if not df_null.empty:
                    print('yes')
                    for index,_ in df_null.iterrows():
                        
                        update_query = f"""
                                        UPDATE covid_us
                                        SET recovered = {_['recovered_right']}
                                        WHERE final_date = '{_['date']}';
                    
                                """

                        execute_query(conn = conn,cur=cur,query = update_query  )
                    print('values updated')  
                else:
                    print('no values to update')
        cur.close()
        conn.close()
    else:
        cur.close()
        conn.close()