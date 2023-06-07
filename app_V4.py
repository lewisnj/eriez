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


df = pd.melt(raw, 
             id_vars='Distance',
             value_vars=col_names,
             var_name='Magnet',
             value_name='Gauss'
            )

#Add in a safety factor e.g. for a 5% reduction set sf = 5
sf = 5
sf = ((100-sf)/100)

df['Gauss'] = df['Gauss'].apply(lambda x: x*10000*sf)


#convert Gauss column from decimal to interger type
df = df.astype({'Gauss':'int'})

#filter the magnet models to include only the standard range
mag_range = df_range[df_range['include']==1]

#filter the list to only have data points at every int e.g. every 5 mm. This help to smooth the data and reduces the points when hovering over the graph.
min = 0
max = 5000
int = 5

pts = list(range(min,max+int,int))

#st.dataframe(mag_range)

df['Force Density']= np.NaN

for i in range(int,len(df)-1-int):
    df.loc[i,'Force Density'] = 0.01*df.loc[i,'Gauss']*((df.loc[i-int,'Gauss']-df.loc[i+int,'Gauss'])/(2*int))
    

# Applying the condition
df.loc[df["Force Density"] < 0, "Force Density"] = np.NaN
df.loc[df["Distance"] == 5, "Force Density"] = np.NaN

df['Force Density'] = df['Force Density'].round(decimals = 1)


mag_include = mag_range['magnet']

df = df[(df['Magnet'].isin(mag_include)) & (df['Distance'].isin(pts))]

#st.markdown(mag_include)

#st.dataframe(df)

st.sidebar.header("Please Filter Here:")

magnet = st.sidebar.multiselect(
    "Select Magnet:",
    options=df["Magnet"].unique(),
)

df_selection = df.query(
    "Magnet == @magnet"
)
#df_selection = df_selection[["distance","gauss"]]

#st.dataframe(df_selection.style.format(precision=1))

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
    df_selection, 
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





