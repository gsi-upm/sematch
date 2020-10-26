import pandas as pd

#tables = pd.read_html("http://apps.sandiego.gov/sdfiredispatch/")

#calls_df, = pd.read_html("http://apps.sandiego.gov/sdfiredispatch/", header=0, parse_dates=["Call Date"])
#
# #print(calls_df)
#
# #print(calls_df.to_json(orient="records", date_format="iso"))
# #
import gdelt


def test_gdelt():
    gd1 = gdelt.gdelt(version=1)

    results= gd1.Search('2016 Nov 01',table='gkg')
    print(len(results))
    print(results[:10])


    results = gd1.Search(['2016 Oct 31','2016 Nov 2'], coverage=True,table='events')
    print(len(results))

