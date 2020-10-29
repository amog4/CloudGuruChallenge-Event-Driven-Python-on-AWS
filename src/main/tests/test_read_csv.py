import unittest
import sys
from cloudguru.transform import transform_df


class TestTransformDf(unittest.TestCase):

    def test_df(self):
        
        df = transform_df(NYT = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv1'
                        ,TIMESERIES ='https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv1' ,arn=None,sns=None,headers=None)
        if not df.empty:
            empt = 'False'
        else:
            empt = 'True'
        
        self.assertEqual(df['date'].dtypes,'datetime64[ns]')
        self.assertEqual(empt,'False')

    

if __name__ == '__main__':
     unittest.main()