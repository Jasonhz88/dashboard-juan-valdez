# Script: app.py
# Descripción: Script de automatización de limpieza con NumPy/Pandas e interfaz interactiva.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Configuración de la interfaz del Dashboard
st.set_page_config(page_title="Data Master - Juan Valdez", page_icon="☕", layout="wide")

st.title("☕ Sistema de Auditoría Automática - Juan Valdez")
st.markdown("Herramienta de producción para la limpieza y análisis de registros de venta diarios.")
st.markdown("---")

# 2. El Motor de Automatización (Funciones lógicas)
def procesar_limpieza_ia(df):
    """Aplica las reglas de limpieza automáticas al dataset cargado"""
    # Eliminar registros duplicados idénticos
    df = df.drop_duplicates()
    
    # Corregir cantidades negativas utilizando NumPy (Convertir a valor absoluto)
    if 'cantidad' in df.columns:
        df['cantidad'] = np.abs(df['cantidad'])
        # Reemplazar valores nulos (vacíos) por la cantidad mínima de 1 unidad
        df['cantidad'] = df['cantidad'].fillna(1)
        
    # Corregir precios unitarios con signo negativo por fallas del sistema
    if 'precio_unitario' in df.columns:
        df['precio_unitario'] = np.abs(df['precio_unitario'])
        
    # Lógica de negocio avanzada: Calcular la métrica de ingreso total por registro
    df['ingreso_total'] = df['cantidad'] * df['precio_unitario']
    return df

# 3. Componentes de la Interfaz Web
st.sidebar.header("📥 Carga de Archivos")
archivo_cargado = st.sidebar.file_uploader("Sube el reporte de ventas diario (.csv)", type=["csv"])

if archivo_cargado is not None:
    # Leer el archivo que el usuario arrastró a la web
    df_crudo = pd.read_csv(archivo_cargado)
    
    # Crear pestañas organizacionales para la visualización de los datos
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard de Ventas", "❌ Datos Crudos (Sucios)", "✅ Datos Auditados (Limpios)"])
    
    with tab2:
        st.warning("⚠️ Registros originales recibidos con anomalías operacionales desde la tienda:")
        st.dataframe(df_crudo, use_container_width=True)
        
    # Ejecución del Script .py en segundo plano de manera automática
    df_limpio = procesar_limpieza_ia(df_crudo)
    
    with tab3:
        st.success("🎉 ¡El motor de automatización corrigió el archivo con éxito!")
        st.dataframe(df_limpio, use_container_width=True)
        
        # Generar un botón para descargar el archivo ya limpio a la computadora
        csv_descarga = df_limpio.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Reporte Auditado (.csv)",
            data=csv_descarga,
            file_name="ventas_limpias_auditoría.csv",
            mime="text/csv"
        )

    with tab1:
        st.subheader("📈 Indicadores Clave de Rendimiento (KPIs)")
        
        # Calcular variables en tiempo real basándose en los datos limpios
        ingresos_totales = df_limpio['ingreso_total'].sum()
        unidades_vendidas = df_limpio['cantidad'].sum()
        ticket_promedio = df_limpio['ingreso_total'].mean()
        
        # Mostrar métricas en formato de tarjetas profesionales
        col1, col2, col3 = st.columns(3)
        col1.metric("Ingresos Netos Auditados", f"${ingresos_totales:,.0f} COP")
        col2.metric("Volumen de Productos", f"{unidades_vendidas:.0f} Uds")
        col3.metric("Ticket Promedio de Compra", f"${ticket_promedio:,.0f} COP")
        
        st.markdown(" quick_reply=False---")
        
        # Construcción del gráfico interactivo dinámico con Plotly
        st.subheader("🛒 Distribución de Ingresos por Tipo de Producto")
        grafico = px.bar(
            df_limpio, 
            x='producto', 
            y='ingreso_total', 
            color='producto',
            title="Ingresos reales tras remover duplicados y corregir valores atípicos",
            labels={'ingreso_total': 'Total de Ingresos ($)', 'producto': 'Línea de Producto'}
        )
        st.plotly_chart(grafico, use_container_width=True)

else:
    st.info("💡 Esperando archivo. Sube el reporte 'ventas_sucias.csv' en el panel izquierdo para iniciar la auditoría.")
