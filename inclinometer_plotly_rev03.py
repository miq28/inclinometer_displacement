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
base_row=178

start_column=34
end_skip_row=179


skip_row = list(range(2, base_row))
skip_rows = list(range(base_row+1, end_skip_row))

skip_rows = skip_row+skip_rows
print(skip_rows)

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
df = df_incremental_a.iloc[:, ::-1].cumsum(axis=1).iloc[:, ::-1]
df=df.reset_index()
print(df)
df=pd.melt(
    df,
    id_vars=['TIMESTAMP'], value_vars=list(df.columns),
    # id_vars=list(df.columns), value_vars=['TIMESTAMP'],
    var_name='Depth', value_name='Displacement'
    )
# df = df.set_index(df.columns[0])
df.insert(1, 'Axis', 'A')
df_cum_a=df
print(df_cum_a)

#------------
# B-Axis
#------------

used_cols= list(range(start_column+num_of_ipis, start_column+num_of_ipis+num_of_ipis))
# used_cols= list(range(start_column, start_column+num_of_ipis+num_of_ipis))
used_cols.insert(0,0)

df = pd.read_csv(
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

print(df)
# INCREMENTAL
df = df.sub(df.iloc[0,:],axis=1)
# CUMMULATIVE
df = df.iloc[:, ::-1].cumsum(axis=1).iloc[:, ::-1]

print(df)
# 
# df = df.transpose()
# # df = df.T
df=df.reset_index()
print(df)
df=pd.melt(
    df,
    id_vars=['TIMESTAMP'], value_vars=list(df.columns),
    # id_vars=list(df.columns), value_vars=['TIMESTAMP'],
    var_name='Depth', value_name='Displacement'
    )
# df = df.set_index(df.columns[0])
df.insert(1, 'Axis', 'B')
df_cum_b=df
df=pd.concat([df_cum_a,df_cum_b])
# df = df.set_index(df.columns[0])
print(df)

# df_cum_b = pd.MultiIndex.from_frame(df_cum_b)
# df_cum_b = df_cum_b.set_index(df_cum_b.columns[0])
# print(df_cum_b[df_cum_b.columns[1]])
# data_top = df_cum_b.head() 
# print(df_cum_b)

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

fig = df.plot.line(
    x='Displacement',
    y='Depth',
    color='TIMESTAMP',
    facet_col='Axis',
    facet_col_spacing=0.11,
    title="Cummulative"
)
fig.update_yaxes(matches=None,showticklabels=True,autorange='reversed')
fig.show()