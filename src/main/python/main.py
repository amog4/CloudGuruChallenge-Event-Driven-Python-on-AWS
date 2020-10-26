from transform import transform_df
from table_queries import *
from write import *
import configparser
import numpy as np
import sys
sys.path.insert(1, 'src/main')


config = configparser.ConfigParser()
config.read('src/main/properties/config.cfg')

TIMESERIES = config['URL']['TIMESERIES']
NYT = config['URL']['NYT']
APIKEY = config['URL']['APIKEY']
headers = {'Authorization': 'Bearer %s' % APIKEY} 



def main():
    
    dbconfig = config['DB']
    
    conn ,cur =db_connect(dbconfig=dbconfig)
    

    values = select_query(conn =conn,cur=cur,query=table_if_exists)

    if not values[0][0]:
        execute_query(conn = conn,cur=cur,query = create_table)
    else:
        row = select_query(conn = conn,cur = cur,query = select_table)

    df = transform_df(NYT =NYT,headers =headers,TIMESERIES=TIMESERIES)
    insert_update_rows(cur = cur,conn = conn,row= row,df = df)



if __name__ == "__main__":
    main()