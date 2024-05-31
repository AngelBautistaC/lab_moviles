import pandas as pd
import altair as alt
import numpy as np
from altair_saver import save

# Read the CSV files into Pandas Dataframes
df_dia_sem = pd.read_csv('BD Min,Megas x Dia Sem.csv', delimiter=';')
df_clientes = pd.read_csv('BD Clientes.csv', delimiter=';')
df_franja_horaria = pd.read_csv('BD Min,Megas x Franja Horaria.csv', delimiter=';')
df_minutos_soles = pd.read_csv('Minutos Peru Soles.csv', delimiter=';')
df_megas_web = pd.read_csv('Megas Web (Soles).csv', delimiter=';')
df_megas_soles = pd.read_csv('BD Min,Megas Soles IN & OUT Peru.csv', delimiter=';')

# Display the first 5 rows of each DataFrame
print("Primeras 5 filas de df_dia_sem:")
print(df_dia_sem.head().to_markdown(index=False, numalign="left", stralign="left"))
print("\n")

print("Primeras 5 filas de df_clientes:")
print(df_clientes.head().to_markdown(index=False, numalign="left", stralign="left"))
print("\n")

print("Primeras 5 filas de df_franja_horaria:")
print(df_franja_horaria.head().to_markdown(index=False, numalign="left", stralign="left"))
print("\n")

print("Primeras 5 filas de df_minutos_soles:")
print(df_minutos_soles.head().to_markdown(index=False, numalign="left", stralign="left"))
print("\n")

print("Primeras 5 filas de df_megas_web:")
print(df_megas_web.head().to_markdown(index=False, numalign="left", stralign="left"))
print("\n")

print("Primeras 5 filas de df_megas_soles:")
print(df_megas_soles.head().to_markdown(index=False, numalign="left", stralign="left"))
print("\n")

# Print the column names and their data types for each DataFrame
print("Información de columnas de df_dia_sem:")
print(df_dia_sem.info())
print("\n")

print("Información de columnas de df_clientes:")
print(df_clientes.info())
print("\n")

print("Información de columnas de df_franja_horaria:")
print(df_franja_horaria.info())
print("\n")

print("Información de columnas de df_minutos_soles:")
print(df_minutos_soles.info())
print("\n")

print("Información de columnas de df_megas_web:")
print(df_megas_web.info())
print("\n")

print("Información de columnas de df_megas_soles:")
print(df_megas_soles.info())

# Eliminar columnas con 'Unnamed' en df_dia_sem
df_dia_sem = df_dia_sem.loc[:, ~df_dia_sem.columns.str.contains('Unnamed')]

# Eliminar columnas con 'Unnamed' en df_franja_horaria
df_franja_horaria = df_franja_horaria.loc[:, ~df_franja_horaria.columns.str.contains('Unnamed')]

# Agrupar por 'Dia Sem' y sumar las columnas relevantes
df_dia_sem_agg = df_dia_sem.groupby('Dia Sem')[['Minutos', 'Megas Web', 'Megas Whatsapp', 'Megas Facebook']].sum().reset_index()

# Ordenar por 'Minutos' en orden descendente
df_dia_sem_agg = df_dia_sem_agg.sort_values(by='Minutos',ascending=False)

# Transformar a formato largo para facilitar el gráfico
df_dia_sem_agg_long = df_dia_sem_agg.melt(id_vars='Dia Sem', var_name='Tipo de Consumo', value_name='Total')

# Crear gráfico de barras para consumo por día de la semana
chart1 = alt.Chart(df_dia_sem_agg_long, title='Consumo Total por Día de la Semana').mark_bar().encode(
    x=alt.X('Dia Sem:O', axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('Total:Q'),
    color='Tipo de Consumo:N',
    tooltip=['Dia Sem', 'Tipo de Consumo', 'Total']
).interactive()

# Agrupar por 'Franja Horaria' y sumar las columnas relevantes
df_franja_horaria_agg = df_franja_horaria.groupby('Franja Horaria')[['Minutos', 'Megas Web', 'Megas Whatsapp', 'Megas Facebook']].sum().reset_index()

# Transformar a formato largo para facilitar el gráfico
df_franja_horaria_agg_long = df_franja_horaria_agg.melt(id_vars='Franja Horaria', var_name='Tipo de Consumo', value_name='Total')

# Crear gráfico de barras para consumo por franja horaria
chart2 = alt.Chart(df_franja_horaria_agg_long, title='Consumo Total por Franja Horaria').mark_bar().encode(
    x=alt.X('Franja Horaria:O', axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('Total:Q'),
    color='Tipo de Consumo:N',
    tooltip=['Franja Horaria', 'Tipo de Consumo', 'Total']
).interactive()

# Mostrar ambos gráficos
chart1.save('consumo_dia_semana_bar_chart.json')
chart2.save('consumo_franja_horaria_bar_chart.json')
# Unir dataframes por DNI
df_combinado = df_clientes.merge(df_dia_sem, on='DNI', how='inner')

# Calcular la media de consumo por Edad
df_edad_agg = df_combinado.groupby('Edad')[['Minutos', 'Megas Web', 'Megas Whatsapp', 'Megas Facebook']].mean().reset_index()
df_edad_agg_long = df_edad_agg.melt(id_vars='Edad', var_name='Tipo de Consumo', value_name='Media')

# Crear gráfico de barras para consumo promedio por edad
chart3 = alt.Chart(df_edad_agg_long, title='Consumo Promedio por Edad').mark_bar().encode(
    x=alt.X('Edad:O', axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('Media:Q'),
    color='Tipo de Consumo:N',
    tooltip=['Edad', 'Tipo de Consumo', 'Media']
).interactive()

# Calcular la media de consumo por Género
df_genero_agg = df_combinado.groupby('Género')[['Minutos', 'Megas Web', 'Megas Whatsapp', 'Megas Facebook']].mean().reset_index()
df_genero_agg_long = df_genero_agg.melt(id_vars='Género', var_name='Tipo de Consumo', value_name='Media')

# Crear gráfico de barras para consumo promedio por género
chart4 = alt.Chart(df_genero_agg_long, title='Consumo Promedio por Género').mark_bar().encode(
    x=alt.X('Género:N', axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('Media:Q'),
    color='Tipo de Consumo:N',
    tooltip=['Género', 'Tipo de Consumo', 'Media']
).interactive()

# Calcular la media de consumo por Estado Civil
df_estado_agg = df_combinado.groupby('Estado Civil')[['Minutos', 'Megas Web', 'Megas Whatsapp', 'Megas Facebook']].mean().reset_index()
df_estado_agg_long = df_estado_agg.melt(id_vars='Estado Civil', var_name='Tipo de Consumo', value_name='Media')

# Crear gráfico de barras para consumo promedio por estado civil
chart5 = alt.Chart(df_estado_agg_long, title='Consumo Promedio por Estado Civil').mark_bar().encode(
    x=alt.X('Estado Civil:N', axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('Media:Q'),
    color='Tipo de Consumo:N',
    tooltip=['Estado Civil', 'Tipo de Consumo', 'Media']
).interactive()

# Mostrar los gráficos
chart3.save('consumo_promedio_edad_bar_chart.json')
chart4.save('consumo_promedio_genero_bar_chart.json')
chart5.save('consumo_promedio_estado_civil_bar_chart.json')
# Eliminar columnas con 'Unnamed' en df_minutos_soles
df_minutos_soles = df_minutos_soles.loc[:, ~df_minutos_soles.columns.str.contains('Unnamed')]

# Eliminar columnas con 'Unnamed' en df_megas_web
df_megas_web = df_megas_web.loc[:, ~df_megas_web.columns.str.contains('Unnamed')]

# Renombrar la columna 'Setiembre' a 'Septiembre' en df_megas_web
df_megas_web = df_megas_web.rename(columns={'Setiembre': 'Septiembre'})

# Función para limpiar y convertir a numérico
def clean_and_convert(df, columns):
    for col in columns:
        df[col] = df[col].astype(str).str.replace(r'[S/ ,]', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

# Columnas a limpiar y convertir
meses = ['Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre']

# Limpiar y convertir columnas en df_minutos_soles y df_megas_web
df_minutos_soles = clean_and_convert(df_minutos_soles, meses)
df_megas_web = clean_and_convert(df_megas_web, meses)

# Calcular el ingreso total por mes
df_minutos_soles_agg = df_minutos_soles[meses].sum(axis=0).reset_index().rename(columns={'index':'Mes', 0:'Ingreso_Minutos'})
df_megas_web_agg = df_megas_web[meses].sum(axis=0).reset_index().rename(columns={'index':'Mes', 0:'Ingreso_Megas'})

# Unir los resultados
df_ingresos_combinados = df_minutos_soles_agg.merge(df_megas_web_agg, on='Mes', how='outer')

# Transformar a formato largo para facilitar el gráfico
df_ingresos_combinados_long = df_ingresos_combinados.melt(id_vars='Mes', var_name='Tipo de Ingreso', value_name='Total')


# Diccionario para mapear meses en español a inglés
meses_dict = {'Abril': 'April', 'Mayo': 'May', 'Junio': 'June', 'Julio': 'July', 'Agosto': 'August', 'Septiembre': 'September'}

# Reemplazar nombres de meses en df_ingresos_combinados
df_ingresos_combinados['Mes'] = df_ingresos_combinados['Mes'].replace(meses_dict)

# Convertir 'Mes' a formato de fecha
df_ingresos_combinados['Mes'] = pd.to_datetime(df_ingresos_combinados['Mes'] + ' 2018', format='%B %Y')

# Transformar a formato largo para facilitar el gráfico
df_ingresos_combinados_long = df_ingresos_combinados.melt(id_vars='Mes', var_name='Tipo de Ingreso', value_name='Total')

# Crear gráfico de líneas para ingresos totales
chart6 = alt.Chart(df_ingresos_combinados_long,title='Ingresos Totales por Tipo y Mes').mark_line(point=True).encode(
    x=alt.X('Mes:T', axis=alt.Axis(title='Mes', labelAngle=-45)),
    y=alt.Y('Total:Q', axis=alt.Axis(title='Ingreso Total')),
    color='Tipo de Ingreso:N',
    tooltip=['Mes', 'Tipo de Ingreso', 'Total']
).interactive()

# Mostrar el gráfico
chart6.save('ingresos_totales_line_chart.json')


# Eliminar columnas con 'Unnamed' en df_megas_soles
df_megas_soles = df_megas_soles.loc[:, ~df_megas_soles.columns.str.contains('Unnamed')]

# Eliminar 'S/ ' y convertir 'Minutos Soles' a numérico
df_megas_soles['Minutos Soles'] = (
    df_megas_soles['Minutos Soles'].astype(str).str.replace(r'[S/ ,]', '', regex=True)
)
df_megas_soles['Minutos Soles'] = pd.to_numeric(df_megas_soles['Minutos Soles'], errors='coerce')

# Agrupar por 'Pais' y sumar las columnas relevantes
df_pais_agg = df_megas_soles.groupby('Pais')[['Min Out Perú', 'Minutos Soles']].sum().reset_index()

# Ordenar por 'Minutos Soles' en orden descendente
df_pais_agg = df_pais_agg.sort_values(by='Minutos Soles', ascending=False)

# Agrupar por 'DNI' y sumar 'Minutos Soles' (para llamadas internacionales)
df_megas_soles_agg = df_megas_soles.groupby('DNI')['Minutos Soles'].sum().reset_index()

# Unir con df_minutos_soles por DNI
df_combinado_intl = df_megas_soles_agg.merge(df_minutos_soles, on='DNI', how='left')

# Calcular correlación para cada mes y entre las columnas de minutos
correlation_results = {}
for mes in meses:
    correlation = np.corrcoef(df_combinado_intl['Minutos Soles'], df_combinado_intl[mes])[0, 1]
    correlation_results[mes] = correlation

# Imprimir resultados de correlación
print("Correlaciones entre Minutos Soles (Internacional) y cada mes:")
for mes, corr in correlation_results.items():
    print(f"{mes}: {corr:.3f}")



# Calcular correlación para cada mes y entre las columnas de minutos
correlation_results = {}
for mes in meses:
    correlation = np.corrcoef(df_combinado_intl['Minutos Soles'], df_combinado_intl[mes])[0, 1]
    correlation_results[mes] = correlation

# Imprimir resultados de correlación
print("Correlaciones entre Minutos Soles (Internacional) y cada mes:")
for mes, corr in correlation_results.items():
    print(f"{mes}: {corr:.3f}")

# Tomar los primeros 10 países
df_pais_agg_top10 = df_pais_agg.head(10)

# Transformar a formato largo para facilitar el gráfico
df_pais_agg_top10_long = df_pais_agg_top10.melt(id_vars='Pais', var_name='Tipo de Minutos', value_name='Total')

# Crear gráfico de barras para los primeros 10 países
chart7 = alt.Chart(df_pais_agg_top10_long, title='Minutos Totales (Locales y Out Perú) por País (Top 10)').mark_bar().encode(
    x=alt.X('Pais:N', sort='-y'),
    y=alt.Y('Total:Q'),
    color='Tipo de Minutos:N',
    tooltip=['Pais', 'Tipo de Minutos', 'Total']
).interactive()

# Guardar el gráfico
chart7.save('minutos_totales_pais_top10_bar_chart.json')

# Combinar todos los gráficos en una sola visualización
fig = chart1 | chart2 | chart3 | chart4 | chart5 | chart6 | chart7

# Guardar la visualización combinada en un archivo HTML
save(fig, "todas_las_graficas.html")