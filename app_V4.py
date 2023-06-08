import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import numpy as np
from PIL import Image

#Display float with 2 decimal values
#pd.options.display.float_format = '{:.0f}'.format

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Field Strength Dashboard", 
                   page_icon=":chart_with_downwards_trend:", 
                   layout="wide"
)

#Import data

# This is the fea data for overband magnets
#Import the magnet data from the csv file
#raw = pd.read_csv("H:/APPLICATIONS DATA\Apps and Calculators/Data/fea_magnet_field_data_master.csv")

raw = pd.read_csv("fea_magnet_field_data_master.csv")

#Import the list of standard magnets. These are the ones that will be included in the chart
#df_range = pd.read_csv("H:/APPLICATIONS DATA\Apps and Calculators/Data/standard_magnet_range.csv")

df_range = pd.read_csv("standard_magnet_range.csv")

#clean and tidy up the data

col_names = list(raw.columns)

#convert the gauss table to long format
df = pd.melt(raw, 
             id_vars='Distance',
             value_vars=col_names,
             var_name='Magnet',
             value_name='Gauss'
            )

raw = pd.read_csv("fd_from_master_minus5pct.csv")

#convert the force density table to long format
df2 = pd.melt(raw, 
             id_vars='Distance',
             value_vars=col_names,
             var_name='Magnet',
             value_name='Force Density'
            )

#Add in a safety factor e.g. for a 5% reduction set sf = 5
sf = 5
sf = ((100-sf)/100)

df['Gauss'] = df['Gauss'].apply(lambda x: x*10000*sf)



#convert Gauss column from decimal to interger type
df = df.astype({'Gauss':'int'})

#round the force density data to 1dp
df2['Force Density'] = df2['Force Density'].round(decimals = 1)

#filter the magnet models to include only the standard range
mag_range = df_range[df_range['include']==1]

#filter the list to only have data points at every int e.g. every 5 mm. This help to smooth the data and reduces the points when hovering over the graph.
min = 0
max = 5000
int = 5

pts = list(range(min,max+int,int))

mag_include = mag_range['magnet']

#Data frame for the gauss values
df = df[(df['Magnet'].isin(mag_include)) & (df['Distance'].isin(pts))]
#Data frame for the force density values
df2 = df2[(df2['Magnet'].isin(mag_include)) & (df2['Distance'].isin(pts))]


st.sidebar.header("Please Filter Here:")

magnet = st.sidebar.multiselect(
    "Select Magnet:",
    options=df["Magnet"].unique(),
)

#data frame including the selected models 
df_selection = df.query(
    "Magnet == @magnet"
)

df_selection2 = df2.query(
    "Magnet == @magnet"
)
#df_selection = df_selection[["distance","gauss"]]

#st.dataframe(df_selection.style.format(precision=1))
#st.dataframe(df_selection2.style.format(precision=1))

## ---- MAINPAGE ----
st.title(":chart_with_downwards_trend: Magnet Field Charts")
#st.header("Magnetic Field Strength")
#st.markdown("")
#
#
## Gauss Chart - line chart
st.header("Magnetic Field Strength")
#st.markdown("")
fig_gauss = px.line(
    df_selection, 
    x='Distance', 
    y='Gauss',
    color='Magnet',
    labels={
        "Distance":"Distance from face plate (mm)",
    "Gauss":"Field Strength (Gauss)",
    "Magnet":"Magnet Model"
    }
    )

axis_template=dict(showgrid=True,nticks=25)


fig_gauss.update_layout(
    font_color="Black",
    font_size=26,
    xaxis = axis_template,
    yaxis = axis_template
    )


from PIL import Image
#img = Image.open("H:/APPLICATIONS DATA/Apps and Calculators/Field Chart App/ERIEZ_orange_logo.png")

img = Image.open("ERIEZ_orange_logo.png")

# Add Eriez logo as background image
fig_gauss.add_layout_image(
        dict(
            source=img,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            sizex=0.5, sizey=0.6,
            xanchor="center",
            yanchor="middle",
            opacity=0.5)
)

st.plotly_chart(fig_gauss, use_container_width=True)

## Force Density Chart - line chart
st.header("Force Density")
#st.markdown("")
fig_fd = px.line(
    df_selection2, 
    x='Distance', 
    y='Force Density',
    color='Magnet',
    labels={
        "Distance":"Distance from face plate (mm)",
    "Force Density":"Force Density (kdynes/cm3)",
    "Magnet":"Magnet Model"
    }
    )

fig_fd.update_layout(
    font_color="Black",
    font_size=26,
    xaxis = axis_template,
    yaxis = axis_template
    )

# Add Eriez logo as background image
fig_fd.add_layout_image(
        dict(
            source=img,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            sizex=0.5, sizey=0.6,
            xanchor="center",
            yanchor="middle",
            opacity=0.5)
)

    
st.plotly_chart(fig_fd, use_container_width=True)





