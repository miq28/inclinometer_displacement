import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt 
import seaborn as sns

TZ_ORIGIN='Asia/Makassar'

def my_date_parser_2(dt_naive):
    dt_aware = pd.to_datetime(dt_naive, errors='coerce', utc=False).tz_localize(TZ_ORIGIN)
    return dt_aware

num_of_ipis=15
base_row=4

start_column=34
end_skip_row=200


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


# COMBINE WITH B-Axis
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


# fig = df.plot.line(
#     x='Displacement',
#     y='Depth',
#     color='TIMESTAMP',
#     facet_col='Axis',
#     facet_col_spacing=0.11,
#     title="Cummulative"
# )
# fig.update_yaxes(matches=None,showticklabels=True,autorange='reversed')
# fig.show()

# df.plot(kind = 'scatter', x='Displacement', y='Depth')
# plt.show()

sns.set_theme()

# seaborn.FacetGrid(data, *, row=None, col=None, hue=None, col_wrap=None, sharex=True, sharey=True, height=3, aspect=1, palette=None, row_order=None, col_order=None, hue_order=None, hue_kws=None, dropna=False, legend_out=True, despine=True, margin_titles=False, xlim=None, ylim=None, subplot_kws=None, gridspec_kws=None)

# df = df.sort_values('Axis')
              


# graph = sns.FacetGrid(df,
#                       sharey=False,
#                       col ="Axis", 
#                       hue ="TIMESTAMP")

# # map the above form facetgrid with some attributes 
# graph.map_dataframe(sns.scatterplot, "Displacement", "Depth", edgecolor ="w").add_legend() 
# graph.map(sns.lineplot, "Displacement", "Depth", sort=False,).add_legend() 

# sns.catplot(
#     data=df,
#     kind="point",
#     sharey=False,
#     x="Displacement", y="Depth", hue="TIMESTAMP",
# )

# sns.pointplot(
#     data=df,
#     x="Displacement", y="Depth", hue="TIMESTAMP",
#     markers=["o", "s"], linestyles=["-", "--"],
# )

# g = sns.catplot(x='Displacement',
#             y='Depth',
#             col="Axis",
#             hue='TIMESTAMP',
            
#             # sharex=False,
#             # sharey=False,
#             data=df,
#             kind='point',
#             # height=6,
#             # aspect=13/6,
#             legend=True, palette='hls',
#             # facet_kws={'sharey':False},
#             )

palette = sns.color_palette("mako_r", 6)
df=df.reset_index()
g = sns.relplot(data=df,
            x='Displacement',
            y='Depth',
            hue='TIMESTAMP',
            # hue_norm=mpl.colors.LogNorm(),
            # palette=palette,
            palette='hls',
            col="Axis",
            # sharex=False,
            # sharey=False,            
            kind='line',
            sort=False,
            style="TIMESTAMP",
            markers=True,
            dashes=False,
            errorbar=None,
            # size='index',
            # sizes=(.25, 2.5),
            height=6,
            aspect=5/6,
            # legend=True,
            legend=True,
            estimator=None,
            facet_kws={'sharey':False},
            # kwargs={'s':10}
            )

# g.sharey = False

# sns.lineplot(
#     data=df,
#     x='Displacement', 
#     y='Depth', 
#     sort=False,
#     hue='TIMESTAMP',
#     # facet_kws='Axis',
#     # facet_kws={'sharey':False},
#     )

g.set(xlabel ="Displacement (mm)", ylabel = "Depth (m)")
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=None)
# plt.tight_layout()
plt.show() 