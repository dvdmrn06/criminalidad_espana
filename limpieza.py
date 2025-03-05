#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

import pandas as pd

df_1 = pd.read_excel("./df1_nacionales_extranjeros.xlsx")
df_2 = pd.read_excel("./mapeo_poblacional_nacional_extranjero.xlsx")

#LIMPIEZA Y CREACIÓN DE DATASET FINAL (1)

# Melt del dataset principal
df_1 = df_1.melt(
    id_vars=['comunidad', 'nacionalidad', 'tipo_delito', 'violencia'],
    var_name='año',
    value_name='total_delincuentes'
)

#Convertir columna año a tipo numérico
df_1['año'] = df_1['año'].astype(int)

df_1.dtypes

# Melt del dataset de mapeo poblacional
df_2 = df_2.melt(
    id_vars=['comunidad', 'nacionalidad'],
    var_name='año',
    value_name='población_total'
)

# Convertir la columna 'año' y población_total a tipo numérico
df_2['año'] = df_2['año'].astype(int)
df_2['población_total'] = df_2['población_total'].astype(int)

df_2.dtypes

#Revisamos nulos
df_1.isnull().sum()
df_2.isnull().sum()


# Realizar el merge con df_1 en base a comunidad, nacionalidad y año
df_final = df_1.merge(
    df_2,
    on=['comunidad', 'nacionalidad', 'año'],
    how='left'
)

#Añadir tasa 100K
df_final["tasa_por_100k"] = (df_final["total_delincuentes"] / df_final["población_total"]) * 100000
df_final.isnull().sum()
df_final.dtypes

df_final.to_excel("./dataset_final.xlsx", index=False)


df_3 = pd.read_excel("./df_1_pais.xlsx")
df_4 = pd.read_excel("./df_2_mapeo_pais.xlsx")

#LIMPIEZA Y CREACIÓN DE DATASET FINAL (2)

# Melt del dataset principal
df_3 = df_3.melt(
    id_vars=['comunidad', 'país'],
    var_name='año',
    value_name='total_delincuentes'
)

#Convertir columna año a tipo numérico
df_3['año'] = df_3['año'].astype(int)

df_3.dtypes

# Melt del dataset de mapeo poblacional
df_4 = df_4.melt(
    id_vars=['comunidad', 'país'],
    var_name='año',
    value_name='población_total'
)

# Convertir la columna 'año' y población_total a tipo numérico
df_4['año'] = df_4['año'].astype(int)
df_4['población_total'] = df_4['población_total'].astype(int)

df_4.dtypes

#Revisamos nulos
df_3.isnull().sum()
df_4.isnull().sum()


# Realizar el merge con df_3 en base a comunidad, nacionalidad y año
df_final_2 = df_3.merge(
    df_4,
    on=['comunidad', 'país', 'año'],
    how='left'
)

#Añadir tasa 100K
df_final_2.loc[df_final_2['población_total'] == 0, 'población_total'] = 1
df_final_2["tasa_por_100k"] = (df_final_2["total_delincuentes"] / df_final_2["población_total"]) * 100000

df_final_2.isnull().sum()
df_final_2.dtypes

df_final_2 = df_final_2[df_final_2['país'] != 'España']
df_final_2.to_excel("./dataset_final_2.xlsx", index=False)

