import pandas as pd
pd.options.plotting.backend = "plotly"
import plotly.graph_objs as go
import plotly.express as px

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
# print(df_cum_b)

# df_cum_b = df_cum_b.transpose()
# df_cum_b = df_cum_b.T
print(df_cum_b)

# fig = df_cum_b.plot()
# fig['layout']['xaxis']['autorange'] = "reversed"
# fig['layout']['yaxis']['autorange'] = "reversed"
# fig.update_yaxes(type='category')


# fig = px.scatter(df_cum_b, x = df_cum_b.iterrows(), y = ['IPI_1_Def_B(1)', 'IPI_1_Def_B(2)', 'IPI_1_Def_B(3)', 'IPI_1_Def_B(4)', 'IPI_1_Def_B(5)', 'IPI_1_Def_B(6)', 'IPI_1_Def_B(7)', 'IPI_1_Def_B(8)', 'IPI_1_Def_B(9)', 'IPI_1_Def_B(10)', 'IPI_1_Def_B(11)', 'IPI_1_Def_B(12)', 'IPI_1_Def_B(13)', 'IPI_1_Def_B(14)', 'IPI_1_Def_B(15)'])

# fig.update_yaxes(type='category', categoryorder='max descending')
# df_cum_b.set_index(df_cum_b.columns[0])
fig = go.Figure()
# for col in df_cum_b.iterrows():
    # fig.add_trace(go.Line(x=col))
    # fig.add_trace(go.Line(x=col, y = ['IPI_1_Def_B(1)', 'IPI_1_Def_B(2)', 'IPI_1_Def_B(3)', 'IPI_1_Def_B(4)', 'IPI_1_Def_B(5)', 'IPI_1_Def_B(6)', 'IPI_1_Def_B(7)', 'IPI_1_Def_B(8)', 'IPI_1_Def_B(9)', 'IPI_1_Def_B(10)', 'IPI_1_Def_B(11)', 'IPI_1_Def_B(12)', 'IPI_1_Def_B(13)', 'IPI_1_Def_B(14)', 'IPI_1_Def_B(15)']))
    # print(col)

# for col in df_cum_b.columns:
#     print(col)

# for rows in df_cum_b.itertuples():
#     print(rows)

    
for idx, rows in enumerate(df_cum_b.itertuples(index=False)):
    # print(index, rows)
    fig.add_trace(
        # name=df_cum_b.index[x],
        go.Scatter(
            mode='lines',
            name=df_cum_b.index[idx],
            x=rows,
            y = ['IPI_1_Def_B(1)', 'IPI_1_Def_B(2)', 'IPI_1_Def_B(3)', 'IPI_1_Def_B(4)', 'IPI_1_Def_B(5)', 'IPI_1_Def_B(6)', 'IPI_1_Def_B(7)', 'IPI_1_Def_B(8)', 'IPI_1_Def_B(9)', 'IPI_1_Def_B(10)', 'IPI_1_Def_B(11)', 'IPI_1_Def_B(12)', 'IPI_1_Def_B(13)', 'IPI_1_Def_B(14)', 'IPI_1_Def_B(15)']
        )
    )

    
fig['layout']['yaxis']['autorange'] = "reversed"
fig.update_layout(width = 600)
fig.show()

# MELT METHOD
# https://stackoverflow.com/questions/60477982/plotly-dataframe-with-multiple-rows