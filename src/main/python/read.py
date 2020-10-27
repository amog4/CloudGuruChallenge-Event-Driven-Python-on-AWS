import requests
from requests.exceptions import HTTPError
import pandas as pd

def Request(put_url,put_header):
    """
    returns content
    :param put_url:- Url to be processed 
    :param put_header:- Authentication token
    """
    try:
        response = requests.get(url = put_url,headers = put_header )
        response.raise_for_status()
    except HTTPError as httperr:
        print(f'HTTPError: {httperr}')
    except Exception as e:
        print(f'Error: {e}')
    else:
        if response.headers['Content-Type'].split(';')[0] == 'text/plain':
            data = response.text
            print('Response Loaded')
            return data
        else:
            data = response.content
            return data



def data_frame(data):
    columns =data.split("\n")[0].split(',')
    df = pd.DataFrame( data=list(map(lambda x: str(x).replace(', ',' ').split(','), data.split('\n')[1:] )),columns=columns)
    return df




def send_request(body,arn,sns):

    # create an sns client

    try:
        sns.publish(TopicArn=arn, 
            Message=body,)
    except Exception as e:
        print("Error {}".format(e))