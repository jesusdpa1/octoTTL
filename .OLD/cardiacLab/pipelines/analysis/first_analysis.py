# %%
import plotly.graph_objects as go
import plotly.io as pio
import os
import pandas as pd
from pathlib import Path

# %%

path_val = r'C:\Users\jesus.penalozaa\Documents\DSI_Test_21-8-20\test01_2hz_15s.csv'
path_val = Path(path_val)
print(path_val)
# %%
df = pd.read_csv(path_val)
# df = pd.read_excel(path_val, sheet_name='Parameters_916')
# df = df.drop([0], axis=0)
# df.rename(columns=df.iloc[0], inplace=True)
# df.drop(df.index[0], inplace=True)
# df = df.reset_index(drop=True)
# df.head()
# %%
pio.renderers.default = "browser"

# %%

fig = go.Figure(
    data=[go.Bar(y=[2, 1, 3])],
    layout_title_text="A Figure Displayed with the 'png' Renderer"
)
fig.show()
# %%

fig = go.Figure()

fig.add_trace(go.Scatter(x=df['ElapsedTime'], y=df['parameter_value'],
                         mode='lines',
                         name='Sys'))
fig.add_trace(go.Scatter(x=df['ElapsedTime'], y=df['laser']*200,
                         mode='lines',
                         name='Dia'))

fig.show()

# %%
