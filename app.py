import streamlit as st
import pandas as pd
import urllib.parse
import time

st.set_page_config(page_title="Gestor Bienestar Xalapa", page_icon="📱", layout="centered")

st.markdown("### Gestor de Mensajes Bienestar Xalapa (BVP)")
st.markdown("*Versión Web para Celulares y Tablets*")

# Inicialización de estados
if 'df' not in st.session_state:
    st.session_state.df = None

uploaded_file = st.file_uploader("📁 Cargar Archivo Excel de Beneficiarios", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        if st.session_state.df is None:
            df_temp = pd.read_excel(uploaded_file, dtype=str)
            df_temp.columns = df_temp.columns.str.strip().str.upper()
            columnas_necesarias = ['ID_PADRON', 'PATERNO', 'MATERNO', 'NOMBRE', 'NO_ACUSE', 'TEL_CELULAR', 'TEL_FIJO']
            faltantes = [col for col in columnas_necesarias if col not in df_temp.columns]
            
            if faltantes:
                st.error(f"Error: Al archivo le faltan columnas: {', '.join(faltantes)}")
            else:
                st.session_state.df = df_temp
                st.success(f"¡Archivo cargado! ({len(df_temp)} registros)")
    except Exception as e:
        st.error(f"No se pudo leer el archivo Excel: {e}")

if st.session_state.df is not None:
    st.divider()
    col1, col2 = st.columns([2, 1])
    with col1:
        id_buscado = st.text_input("🔍 ID de Padrón:")
    with col2:
        hora_ingresada = st.text_input("⏰ Hora de cita:", value="9:00 hrs")

    if st.button("Buscar Persona", type="primary") and id_buscado:
        resultado = st.session_state.df[st.session_state.df['ID_PADRON'].str.strip() == id_buscado.strip()]
        if resultado.empty:
            st.warning("No se encontró ningún registro con ese ID.")
            st.session_state.persona_encontrada = None
        else:
            st.session_state.persona_encontrada = resultado.iloc[0]

    if 'persona_encontrada' in st.session_state and st.session_state.persona_encontrada is not None:
        fila = st.session_state.persona_encontrada
        paterno = str(fila.get('PATERNO', '')).strip()
        materno = str(fila.get('MATERNO', '')).strip()
        nombres = str(fila.get('NOMBRE', '')).strip()
        nombre_completo = f"{paterno} {materno} {nombres}"
        no_acuse = str(fila.get('NO_ACUSE', '')).strip()
        celular = str(fila.get('TEL_CELULAR', '')).strip()
        fijo = str(fila.get('TEL_FIJO', '')).strip()

        st.info(f"**Nombre:** {nombre_completo} \n**Acuse:** {no_acuse} \n**Celular:** {celular} | **Fijo:** {fijo}")

        mensaje = f"""BUEN DÍA, ME COMUNICO DE LA SECRETARÍA DEL BIENESTAR PARA LA ENTREGA DE SU TARJETA A NOMBRE DE
{nombre_completo}
*ACUSE*: {no_acuse}

Le notificamos que debe pasar a *recoger* su *tarjeta* el día
*26 de AGOSTO 2026.*
En horario de *{hora_ingresada}*
*Escuela Bachilleres Antonio Ma de Rivera*
En calle: Circuito Universitario Gonzalo Aguirre Beltran S/N
Zona Universitaria

 Requisitos: 
- INE vigente
- 1 copias de INE (anotar número de ACUSE que se menciona arriba y 2 números telefónicos )
- 1 copia de CURP reciente DE PREFERENCIA CERTIFICADA POR EL REGISTRO CIVIL
https://maps.app.goo.gl/Eu9iKcpUoyuZiYve9

*FAVOR DE CONFIRMAR ASISTENCIA*."""

        st.text_area("📋 Vista Previa del Mensaje:", value=mensaje, height=180)
        st.divider()

        st.success("🟢 **Estado:** ¡Listo para enviar!")
        
        if celular and celular != "nan":
            tel_limpio_cel = ''.join(filter(str.isdigit, celular))
            link_cel = f"https://wa.me/52{tel_limpio_cel}?text={urllib.parse.quote(mensaje)}"
            st.link_button("💬 Enviar a Celular vía WhatsApp", url=link_cel)
        
        if fijo and fijo != "nan":
            tel_limpio_fijo = ''.join(filter(str.isdigit, fijo))
            link_fijo = f"https://wa.me/52{tel_limpio_fijo}?text={urllib.parse.quote(mensaje)}"
            st.link_button("📞 Enviar a Teléfono Fijo/Alt. vía WhatsApp", url=link_fijo)
