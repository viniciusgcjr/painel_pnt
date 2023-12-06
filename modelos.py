import datetime
from PIL import Image
import streamlit as st
import requests


st.sidebar.caption(':large_blue_circle:')
with st.sidebar.container():
    image = Image.open("./logo.png")
    st.image(image, use_column_width=True)

#Sidebar with Variables
data = {
    'Precipatação WRF': 'acu',
    'Precipitação ETA': 'ETA_precip6h',
    'Precipitação GEPS': 'acu_GEPS',
    'Precipitação GEM': 'acu_GEM',
    'Precipitação ICON': 'acu_ICON',
    'Precipitação GFSA': 'acu_GFSA',
    'Precipitação 24 Horas - WRF': 'ch',
    'Precipitação 24 Horas - ETA': 'ETA_precip',
    'Água Precipitável': 'apm',
    'Linhas de Corrente (950)': 'lc95',
    'Linhas de Corrente (850)': 'lc85',
    'Linhas de Corrente (750)': 'lc75',
    'Linhas de Corrente (500)': 'lc50',
    'Linhas de Corrente (200)': 'lc20',
    'Índice K': 'Ik',
    'Movimento Vertical': 'mv',
    'Umidade Relativa': 'rh',
    'Sensação Térmica': 'st',
}
st.sidebar.title("Variável Meteorológica")
selected_variable = st.sidebar.selectbox("Escolha uma variável", data.keys())

# Sidebar with hour selection
hour_limit = 73
selected_hours = list(range(0, hour_limit, 6))
selected_hours.remove(0)
st.sidebar.title("Hora da Previsão")
selected_hours = st.sidebar.multiselect("Horas apresentadas", selected_hours, selected_hours)

# Get the current date and time
current_datetime = datetime.datetime.now()

# Determine the time period (00 or 12) which the models finished running
current_hour = current_datetime.hour
if 0 <= current_hour < 17:
    time_period = "00"
else:
    time_period = "12"

# Construct the image URL
if 'ETA' in selected_variable:
    image_urls = {
        hour: f"http://200.238.105.69/imagens_modelo/{data[selected_variable]}_{current_datetime.strftime('%Y%m%d')}{time_period}_{hour:02}.png" for hour in range(hour_limit)
    }
elif 'Horas - WRF' in selected_variable:
    image_urls = {
        hour: f"http://200.238.105.69/imagens_modelo/{data[selected_variable]}{hour:02}_{current_datetime.strftime('%Y%m%d')}_{time_period}_1.png" for hour in range(hour_limit)
   }
elif 'Horas - ETA' in selected_variable:
    image_urls = {
        hour: f"http://200.238.105.69/imagens_modelo/{data[selected_variable]}_{current_datetime.strftime('%Y%m%d')}{time_period}_{hour:02}.png" for hour in range(hour_limit)
   }
elif 'GEPS' in selected_variable:
    image_urls = {
        hour: f"http://200.238.105.69/imagens_modelo/{data[selected_variable]}_{current_datetime.strftime('%Y%m%d')}_{time_period}_6em6_{hour}.png" for hour in range(hour_limit)
    }
elif 'GEM' in selected_variable:
    image_urls = {
        hour: f"http://200.238.105.69/imagens_modelo/{data[selected_variable]}_{current_datetime.strftime('%Y%m%d')}_{time_period}_6em6_{hour}.png" for hour in range(hour_limit)
    }
elif 'ICON' in selected_variable:
    image_urls = {
        hour: f"http://200.238.105.69/imagens_modelo/{data[selected_variable]}_{current_datetime.strftime('%Y%m%d')}_{time_period}_6em6_{hour}.png" for hour in range(hour_limit)
    }
elif 'GFSA' in selected_variable:
    image_urls = {
        hour: f"http://200.238.105.69/imagens_modelo/{data[selected_variable]}_{current_datetime.strftime('%Y%m%d')}_{time_period}_6em6_{hour}.png" for hour in range(hour_limit)
    }  
else:
    image_urls = {
        hour: f"http://200.238.105.69/imagens_modelo/{data[selected_variable]}_{current_datetime.strftime('%Y%m%d')}_{time_period}_{hour}.png" for hour in range(hour_limit)
    }

# Main window for plotting
st.title("Previsão Numérica do Tempo")
st.subheader(f"Variável selecionada: {selected_variable}")

# Initialize a list to keep track of the quantity of errors
hours_with_errors = []

# Plotting selected images
for hour in selected_hours:
    response = requests.get(image_urls.get(hour))
    try:
        if response.status_code == 200:
            st.image(image_urls.get(hour), use_column_width=True, caption=f"Hora: {hour}")
    except requests.exceptions.RequestException as e:
        # print(e)
        hours_with_errors.append(hour)


