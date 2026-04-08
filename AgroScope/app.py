import streamlit as st
import pandas as pd
from src.reader import read_csv
from folium import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

def main():
    st.title("AgroScope - Análise de Relatórios Agrícolas")
    
    st.write("Bem-vindo ao AgroScope! Este aplicativo permite que você importe, visualize e analise seus relatórios agrícolas de forma fácil e eficiente.")
    arquivo = st.file_uploader("Importe seu relatório agrícola aqui", type=["csv", "xlsx"])
    st.write("Depois de importar o arquivo, você pode visualizar e analisar seus dados de relatório agrícola.")
    if arquivo is not None:
        try:
            df = read_csv(arquivo)
            st.success("Arquivo lido com sucesso!")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")
        try:
            st.write("Mapa de Calor de Vigor (indice_vigor):")
            df_work = df.copy()
            df_work['latitude'] = pd.to_numeric(df_work['latitude'], errors='coerce')
            df_work['longitude'] = pd.to_numeric(df_work['longitude'], errors='coerce')
            df_work['indice_vigor'] = pd.to_numeric(df_work['indice_vigor'], errors='coerce')
            df_valid = df_work[['latitude', 'longitude', 'indice_vigor']].dropna()
            
            if not df_valid.empty:
                m = folium.Map(location=[df_valid['latitude'].mean(), df_valid['longitude'].mean()], zoom_start=6)
                heat_data = [[row['latitude'], row['longitude'], row['indice_vigor']] for _, row in df_valid.iterrows()]
                HeatMap(heat_data, min_opacity=0.4, radius=15, blur=10, gradient={0.2: 'red', 0.5: 'yellow', 0.8: 'limegreen'}).add_to(m)
                st_folium(m, width=700, height=500)
            else:
                st.warning("No valid lat/lon/vigor data for heatmap.")
        except Exception as e:
            st.error(f"Erro no mapa de calor: {e}")
if __name__ == "__main__":
    main()
