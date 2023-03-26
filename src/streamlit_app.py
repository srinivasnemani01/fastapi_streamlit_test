# Use below code and enhance following requirements. 
# Create a streamlit line chart. Use the features of streamlit only as much as possible.
# The data frame has 3 columns. "StrikePrice", "OptionPrice", "OptionType"
# generate a dummy pandas data frame of 8 entries.
# Use the unique OptionType to create radio buttons
# On X-axis plot StrikePrice
# On Y-axis plot OptionPrice
# Add another Y-axis on the right side, show the CurrentPrice as dotted line.


import streamlit as st
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LinearAxis, Range1d
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show
from bokeh.models import LinearAxis, Range1d
from bokeh.io import output_notebook
import random

# Generate a dummy Pandas DataFrame with 8 entries
data = {
    "StrikePrice": [100, 105, 110, 115, 120, 125, 130, 135],
    "OptionPrice": [12, 10, 8, 6, 4, 2, 1, 0.5],
    "OptionType": ['Call', 'Put', 'Call', 'Put', 'Call', 'Put', 'Call', 'Put'],
    "CurrentPrice": [120, 120, 120, 120, 120, 120, 120, 120]
}

df = pd.DataFrame(data)
df = df.reset_index(drop=True)


# Streamlit app title
st.title("Option Price Line Chart")
# Create radio buttons using unique OptionTypes
option_types = df['OptionType'].unique()
selected_option_type = st.radio("Select Option Type", options=option_types)

filtered_data = df[df['OptionType'] == selected_option_type]
number_of_rows = filtered_data.shape[0]
# Generate random data for the chart
x = list(range(number_of_rows ))
y1 = [random.randint(number_of_rows , 50) for _ in range(number_of_rows )]
y2 = [random.randint(150, 550) for _ in range(number_of_rows )]
y1  =   filtered_data["OptionPrice"].tolist()
y2  =   filtered_data["CurrentPrice"].tolist()
x1 = filtered_data["StrikePrice"].tolist()

# Filter data based on selected OptionType
# Create a Bokeh figure
p = figure(title="Multi Y-Axis Bokeh Chart", x_axis_label='X-axis', y_axis_label='Y1-axis',  y_range=(0, 30) )

# Add the first line (Y1-axis)
# p.line(x, y1, color="orange", legend_label=selected_option_type, line_width=3)
p.line(x, y1, color="#C00000", legend_label=selected_option_type + " Price", line_width=3)
p.legend.label_text_font_style = 'bold'

# Add the second Y-axis (Y2-axis) on the right side
p.extra_y_ranges = {"Y2_axis": Range1d(start=min(y2) - number_of_rows , end=max(y2) + number_of_rows )}
p.add_layout(LinearAxis(y_range_name="Y2_axis", axis_label="Y2-axis"), 'right')

# Add the second line (Y2-axis)
p.line(x, y2, color="green", y_range_name="Y2_axis", legend_label="Current Price")

# Show the chart



# Display the custom chart in Streamlit
st.bokeh_chart(p, use_container_width=True)
