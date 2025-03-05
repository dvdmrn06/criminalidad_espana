#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos
df_final = pd.read_excel("./dataset_final.xlsx")
df_final_2 = pd.read_excel("./dataset_final_2.xlsx")

# Título de la App
st.title("🚨 Criminalidad en España")

# Filtros en la barra lateral
st.sidebar.header("Filtros")

# Opciones dinámicas para cada filtro
comunidades_disponibles = sorted(df_final["comunidad"].unique().tolist())
comunidades = ["Todos"] + comunidades_disponibles
tipos_delito = ["Todos"] + sorted(df_final["tipo_delito"].unique().tolist())
violencias = ["Todos"] + ["T", "F"]
años = sorted(df_final["año"].unique().tolist())
paises_disponibles = sorted(df_final_2["país"].unique().tolist())
paises = ["Todos"] + paises_disponibles

# Selección de filtros
comunidad_seleccionada = st.sidebar.multiselect("Selecciona Comunidad", comunidades, default=["Todos"])
tipo_delito_seleccionado = st.sidebar.selectbox("Selecciona Tipo de Delito", tipos_delito)
violencia_seleccionada = st.sidebar.selectbox("Selecciona Violencia", violencias)
años_seleccionados = st.sidebar.slider("Selecciona Rango de Años", min_value=min(años), max_value=max(años), value=(min(años), max(años)))
país_seleccionado = st.sidebar.selectbox("Selecciona País", paises)

# Filtrado de datos (df_final)
df_filtrado = df_final[(df_final["año"] >= años_seleccionados[0]) & (df_final["año"] <= años_seleccionados[1])]
if "Todos" not in comunidad_seleccionada:
    df_filtrado = df_filtrado[df_filtrado["comunidad"].isin(comunidad_seleccionada)]
if tipo_delito_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["tipo_delito"] == tipo_delito_seleccionado]
if violencia_seleccionada != "Todos":
    df_filtrado = df_filtrado[df_filtrado["violencia"] == violencia_seleccionada]

# Cálculo de tasas para df_final
df_delincuentes = df_filtrado.groupby(["año", "nacionalidad"], as_index=False)["total_delincuentes"].sum()
df_poblacion = df_filtrado.groupby(["año", "nacionalidad", "comunidad"], as_index=False)["población_total"].mean()
df_poblacion['población_total'] = df_poblacion['población_total'].astype(int)
df_poblacion_total = df_poblacion.groupby(["año", "nacionalidad"], as_index=False)["población_total"].sum()
df_tasa = df_delincuentes.merge(df_poblacion_total, on=["año", "nacionalidad"], how="left")
df_tasa["tasa_por_100k"] = (df_tasa["total_delincuentes"] / df_tasa["población_total"]) * 100000
df_tasa["tasa_crecimiento"] = df_tasa.groupby("nacionalidad")["tasa_por_100k"].pct_change() * 100
df_tasa["tasa_crecimiento_poblacion"] = df_tasa.groupby("nacionalidad")["población_total"].pct_change() * 100

st.header("Detenidos y tipo de delito")

# Gráfico 1
fig_tasa = px.line(df_tasa, x="año", y="tasa_por_100k", color="nacionalidad", title="Evolución de la Tasa de Detenidos por 100k habitantes")
st.plotly_chart(fig_tasa)
# Grafíco 2
fig_crecimiento_delitos = px.line(df_tasa, x="año", y="tasa_crecimiento", color="nacionalidad", title="Evolución de la Tasa de Crecimiento de Detenidos (%)")
st.plotly_chart(fig_crecimiento_delitos)

df_tasa["crecimiento_total_delitos"] = df_tasa.groupby("nacionalidad")["total_delincuentes"].pct_change() * 100
fig_crecimiento_total_delitos = px.line(df_tasa, x="año", y="crecimiento_total_delitos", color="nacionalidad", title="Evolución del Crecimiento del Total de Detenidos (%)")
st.plotly_chart(fig_crecimiento_total_delitos)

df_comunidad_agrupado = df_filtrado.groupby(["comunidad", "año"], as_index=False).agg({
    "total_delincuentes": "sum",
    "población_total": "first"
})
df_comunidad_agrupado["tasa_por_100k"] = (df_comunidad_agrupado["total_delincuentes"] / df_comunidad_agrupado["población_total"]) * 100000
fig_comunidades = px.line(df_comunidad_agrupado, x="año", y="tasa_por_100k", color="comunidad", title="Comparación de la Tasa de Detenidos entre Comunidades")
st.plotly_chart(fig_comunidades)
#Gráfico 3
fig_crecimiento_poblacion = px.line(df_tasa, x="año", y="tasa_crecimiento_poblacion", color="nacionalidad", title="Evolución de la Tasa de Crecimiento de la Población (%)")
st.plotly_chart(fig_crecimiento_poblacion)

# Filtrado de datos (df_final_2)
df_filtrado_2 = df_final_2[(df_final_2["año"] >= años_seleccionados[0]) & (df_final_2["año"] <= años_seleccionados[1])]
if "Todos" not in comunidad_seleccionada:
    df_filtrado_2 = df_filtrado_2[df_filtrado_2["comunidad"].isin(comunidad_seleccionada)]
if país_seleccionado != "Todos":
    df_filtrado_2 = df_filtrado_2[df_filtrado_2["país"] == país_seleccionado]

# Cálculo de tasas para df_final_2
df_agrupado_2 = df_filtrado_2.groupby(["año", "país"], as_index=False).sum()
df_agrupado_2["tasa_por_100k"] = (df_agrupado_2["total_delincuentes"] / df_agrupado_2["población_total"]) * 100000

st.header("Detenidos y país de procedencia (no España)")

# Gráfico 4
fig_tasa_pais = px.line(df_agrupado_2, x="año", y="tasa_por_100k", color="país", title="Evolución de la Tasa de Detenidos por 100k habitantes (por País)")
st.plotly_chart(fig_tasa_pais)

# Gráfico 5
fig_poblacion_pais = px.line(df_agrupado_2, x="año", y="población_total", color="país", title="Evolución de la Población Total (por País)")
st.plotly_chart(fig_poblacion_pais)

#Gráfico 6
fig_total_delincuentes_pais = px.line(df_agrupado_2, x="año", y="total_delincuentes", color="país", title="Evolución del Total de Detenidos (por País)")
st.plotly_chart(fig_total_delincuentes_pais)

st.header("Datasets filtrados en este momento")

# Mostrar tabla con datos
st.dataframe(df_tasa)
st.dataframe(df_agrupado_2)
