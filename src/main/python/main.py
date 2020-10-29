from transform import transform_df
from table_queries import *
from write import *
import configparser
import numpy as np
import sys
import boto3
sys.path.insert(1, 'src/main')
import boto3
import os

config = configparser.ConfigParser()
config.read(os.environ['config_file'])

TIMESERIES = config['URL']['TIMESERIES']
NYT = config['URL']['NYT']


arn = os.environ['sns_topic']

Access_key_ID = config['ARN']['Access_key_ID']
Secret_access_key = config['ARN']['Secret_access_key']
sns = boto3.client('sns',aws_access_key_id =Access_key_ID ,
aws_secret_access_key =Secret_access_key )

def main(event, context):
    
    dbconfig = config['DB']
    
    conn ,cur =db_connect(dbconfig=dbconfig)
    

    values = select_query(conn =conn,cur=cur,query=table_if_exists)

    if not values[0][0]:
        execute_query(conn = conn,cur=cur,query = create_table)
    else:
        row = select_query(conn = conn,cur = cur,query = select_table)

    df = transform_df(NYT =NYT,headers =None,TIMESERIES=TIMESERIES,arn=arn,sns= sns)
    insert_update_rows(cur = cur,conn = conn,row= row,df = df,arn=arn,sns= sns)



if __name__ == "__main__":
    main(event=None, context=None)