# %%
import heartpy as hp
from pyedflib import highlevel
import plotly.io as pio
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
pio.renderers.default = "browser"
# %%
# read an edf file
signals, signal_headers, header = highlevel.read_edf(
    r'/home/jesusdpa/Documents/Rat BP.edf')

# %%
random_x = np.arange(0, 44000) / 1000

# Create traces
fig = go.Figure()
fig.add_trace(go.Scatter(x=random_x[0:5000], y=signals[1][0:5000],
                         mode='lines',
                         name='lines'))

# %%

data = signals[1]
fs = 1000.0
working_data, measures = hp.process(data, fs, report_time=True)
print('breathing rate is: %s Hz' % measures['breathingrate'])
# %%
wd, m = hp.process(data, sample_rate=1000.0)
# %%
# set large figure
plt.figure(figsize=(12, 4))

# call plotter
hp.plotter(wd, m)

# display measures computed
for measure in m.keys():
    print('%s: %f' % (measure, m[measure]))
# %%
