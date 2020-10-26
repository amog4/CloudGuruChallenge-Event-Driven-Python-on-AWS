from read import *



def object_change(data):

    for col in data.columns:
        if data[col].dtypes == 'object':
            data[col] = data[col].astype('float')



def transform_df(NYT,headers,TIMESERIES):
    df_nyt =  Request(put_url = NYT,put_header = headers)
    dff_nyt = data_frame(data = df_nyt)
    df_times = Request(put_url = TIMESERIES,put_header = headers)
    dff_times = data_frame(data = df_times)

    dff_nyt['date'] =dff_nyt['date'].astype('datetime64[ns]')
    dff_times['Date'] = dff_times['Date'].astype('datetime64[ns]')


    dff_times = dff_times[dff_times['Country/Region'] == 'US']
    dff_times = dff_times[['Date','Recovered']]
    dff_times.rename(columns = {'Date':'date'},inplace=True)
    #dff_times = dff_times[dff_times['date'] <= '2020-10-18']

    df = dff_nyt.merge(dff_times,how='left',left_on='date',right_on='date')
    df.loc[df.date == '2020-01-21','Recovered'] = 0

    df.rename(columns = {'Recovered':'recovered'},inplace=True)

    object_change(data=df)
    return df