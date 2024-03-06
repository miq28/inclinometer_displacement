import pandas as pd
pd.options.plotting.backend = "plotly"
import plotly.graph_objs as go
import plotly.express as px
import numpy as np

TZ_ORIGIN='Asia/Makassar'

def my_date_parser_2(dt_naive):
    dt_aware = pd.to_datetime(dt_naive, errors='coerce', utc=False).tz_localize(TZ_ORIGIN)
    return dt_aware

num_of_ipis=15
base_row=4

start_column=34
end_skip_row=165


skip_row = list(range(2, base_row))
skip_rows = list(range(base_row+1, end_skip_row))

skip_rows = skip_rows+skip_row

#------------
# A-Axis
#------------

used_cols= list(range(start_column, start_column+num_of_ipis))
used_cols.insert(0,0)


df_a = pd.read_csv(
    'sample_data.dat',
    skiprows=skip_rows,
    index_col='TIMESTAMP',    
    parse_dates=True,
    header=1,
    # usecols=lambda x: x != 'RECORD',
    usecols=used_cols,
    na_values='NAN',
    # error_bad_lines=False,
    # warn_bad_lines=True,
    on_bad_lines='skip',
    date_format = my_date_parser_2,
)

df_incremental_a = df_a.sub(df_a.iloc[0,:],axis=1)
df_cum_a = df_incremental_a.iloc[:, ::-1].cumsum(axis=1).iloc[:, ::-1]
print(df_cum_a)

#------------
# B-Axis
#------------

used_cols= list(range(start_column+num_of_ipis, start_column+num_of_ipis+num_of_ipis))
used_cols.insert(0,0)

df_b = pd.read_csv(
    'sample_data.dat',
    skiprows=skip_rows,
    index_col='TIMESTAMP',    
    parse_dates=True,
    header=1,
    # usecols=lambda x: x != 'RECORD',
    usecols=used_cols,
    na_values='NAN',
    # error_bad_lines=False,
    # warn_bad_lines=True,
    on_bad_lines='skip',
    date_format = my_date_parser_2,
)

df_incremental_b = df_b.sub(df_b.iloc[0,:],axis=1)
df_cum_b = df_incremental_b.iloc[:, ::-1].cumsum(axis=1).iloc[:, ::-1]
print(df_cum_b)

# df_cum_b = df_cum_b.transpose()
df_cum_b = df_cum_b.T
# df_cum_b = pd.MultiIndex.from_frame(df_cum_b)
# df_cum_b = df_cum_b.set_index(df_cum_b.columns[0])
# print(df_cum_b[df_cum_b.columns[1]])
# data_top = df_cum_b.head() 

list_depth = list(df_cum_b.index.values)
list_date = list(df_cum_b.columns)
# fig = df_cum_b.plot()
fig = df_cum_b.plot.line(
    x=list_date,
    y=list_depth
)
fig['layout']['yaxis']['autorange'] = "reversed"
# fig.show()

# MELT METHOD
# https://stackoverflow.com/questions/60477982/plotly-dataframe-with-multiple-rows




# df = pd.DataFrame({'Date1': {'A1': 10,'A2': 20,'A3': 30},
#                    'Date2': {'A1': 10,'A2': 25,'A3': 30},
#                    'Date3': {'A1': 15,'A2': 30,'A3': 33},
#                   })
# print(df)
# fig = df.plot.line(x=['Date1','Date2','Date3'], y=['A','B','C'])

# df = px.data.gapminder()
# print(df)
# fig.show()