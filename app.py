import streamlit as st
import time

try:
    from openai import OpenAI
except ImportError:
    st.error("Error: Librería 'openai' no instalada.")

try:
    import google.generativeai as genai
    from google.api_core import exceptions as google_exceptions
except ImportError:
    st.error("Error: Librería 'google-generativeai' no instalada.")


# ==========================================
# HELPERS Y GESTIÓN DE BUFFER DE MEMORIA
# ==========================================
def apply_memory_buffer(messages, window_size):
    """
    Simula LangChain's ConversationBufferWindowMemory.
    Retiene el system prompt (índice 0) y los últimos N * 2 mensajes (ida y vuelta del usuario + IA).
    """
    if not messages:
        return []
    system_msg = [messages[0]]
    chat_history = messages[1:]
    # Un "turno" son 2 mensajes: pregunta del user + respuesta de IA
    limit = window_size * 2
    
    if len(chat_history) > limit:
        chat_history = chat_history[-limit:]
        
    return system_msg + chat_history

def estimate_context_size(messages, window_size):
    """
    Estima el número de caracteres y palabras que se enviarán en el búfer de contexto.
    """
    if not messages:
        return 0, 0
    buffer = apply_memory_buffer(messages, window_size)
    total_chars = sum(len(msg["content"]) for msg in buffer)
    total_words = sum(len(msg["content"].split()) for msg in buffer)
    return total_chars, total_words

# ==========================================
# UI/UX STYLING (Tema Inmersivo Oscuro)
# ==========================================
st.set_page_config(page_title="AI Dungeon Master", page_icon="🐉", layout="centered")

st.markdown("""
<style>
    /* Estilo inmersivo RPG */
    .stApp {
        background-color: #0b0f19;
        color: #d8c29e;
        font-family: 'Georgia', serif;
    }
    h1 {
        color: #e6b333;
        font-family: 'Courier New', Courier, monospace;
        text-align: center;
        text-shadow: 2px 2px 4px #000000;
    }
    .stButton>button {
        background: border-box #8b0000; 
        color: white; border: 1px solid #ff4500; border-radius: 4px;
        transition: 0.3s; width: 100%;
    }
    .stButton>button:hover {
        background-color: #ff0000;
        box-shadow: 0 0 10px #ff4500;
        transform: scale(1.02);
    }
    /* Panel lateral oscuro */
    [data-testid="stSidebar"] {
        background-color: #121016;
        border-right: 1px solid #3b3127;
    }
</style>
""", unsafe_allow_html=True)

st.title("🐉 El Abismo Infinito")
st.markdown("<p style='text-align:center;'><em>Una aventura de texto gobernada por las leyes de las IAs generativas y la inmensidad de tu imaginación.</em></p>", unsafe_allow_html=True)

# ==========================================
# SIDEBAR (Configuración y Explicación Teórica)
# ==========================================
with st.sidebar:
    st.header("⚙️ Grimorio del DM")
    proveedor = st.selectbox("Motor LLM (El cerebro del DM):", ["Google Gemini (Recomendado)", "OpenAI", "Groq"])
    
    model_gemini = "gemini-1.5-flash"
    if proveedor == "Google Gemini (Recomendado)":
        model_gemini = st.selectbox(
            "Modelo Gemini:",
            ["gemini-1.5-flash", "gemini-1.5-pro"],
            help="gemini-1.5-flash: Rápido y con límites gratuitos muy amplios (recomendado para evitar el error 429). gemini-1.5-pro: Más inteligente pero con límites muy estrictos."
        )
        
    # IMPORTANTE: Nunca subas a GitHub tu clave real. Pégala aquí solo temporalmente o usa st.secrets.
    api_key = st.text_input("Ingresa tu API Key (No se guarda):", value="TU_API_KEY_AQUI", type="password")
    
    st.markdown("---")
    st.subheader("📚 Gestión de Memoria")
    
    memoria_turns = st.slider("Tamaño del Buffer (Turnos recordados):", min_value=1, max_value=6, value=3)
    
    st.markdown("""
    **¿Qué es el Memory Buffer?**
    La IA normalmente "no tiene memoria". Pierde el contexto tras cada mensaje. 
    Aquí aplicamos un *ConversationBufferWindowMemory*: Recortamos el historial a los últimos X turnos para evitar saturar el límite de *Tokens*.
    """)
    
    # Indicador dinámico de memoria
    st.markdown("---")
    st.subheader("📊 Consumo de Memoria")
    if "messages" in st.session_state:
        buffer_actual = apply_memory_buffer(st.session_state.messages, memoria_turns)
        total_chars, total_words = estimate_context_size(st.session_state.messages, memoria_turns)
        
        if total_chars < 3000:
            color = "#2ecc71"
            estado = "🟢 Seguro (Bajo consumo de tokens)"
        elif total_chars < 7000:
            color = "#f1c40f"
            estado = "🟡 Moderado (Riesgo bajo de 429)"
        else:
            color = "#e74c3c"
            estado = "🔴 Alto (Riesgo de error 429 en plan gratuito)"
            
        st.markdown(f"""
        * **Mensajes en memoria:** {max(0, len(buffer_actual) - 1)} (más prompt)
        * **Caracteres estimados:** `{total_chars}`
        * **Palabras estimadas:** `{total_words}`
        
        <div style="background-color: #161520; padding: 10px; border-radius: 5px; border-left: 5px solid {color}; margin-top: 5px; border: 1px solid #3b3127;">
            <span style="color: {color}; font-weight: bold; font-size: 0.9em;">{estado}</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    if st.button("🔄 Reiniciar Aventura"):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# CONVERSATIONAL BUFFER & SYSTEM PROMPT
# ==========================================
SYSTEM_PROMPT = """Eres el Dungeon Master (DM) definitivo de un juego de rol de mesa de fantasía oscura asombroso.
Tu deber es narrar el entorno con lenguaje épico, descriptivo e inmersivo. Siempre hablas en segunda persona hacia el jugador.
REGLA 1: NUNCA decidas las acciones del jugador, descríbele la situación o las consecuencias de sus actos únicamente.
REGLA 2: Eres libre de ser creativo, inventar personajes, monstruos y armas increíbles.
REGLA 3: Al final de CADA una de tus narraciones, dale al usuario 3 opciones pregeneradas de lo que podría tomar como acción estructurado en una lista (viñetas). Aclara que también puede hacer lo que se le ocurra.
REGLA 4: El usuario empieza en las Puertas de la Cripta de Hierro. Ofrece una entrada dramática.
"""

# Inicializar sesión
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

def call_llm(context_messages, apiKey, prov, gemini_model="gemini-1.5-flash"):
    if "Groq" in prov or "OpenAI" in prov:
        base_url = "https://api.groq.com/openai/v1" if "Groq" in prov else None
        model_name = "llama3-8b-8192" if "Groq" in prov else "gpt-3.5-turbo"
        client = OpenAI(api_key=apiKey, base_url=base_url)
        response = client.chat.completions.create(
            model=model_name,
            messages=context_messages,
            temperature=0.85 # Temperatura alta para máxima narrativa RPG
        )
        return response.choices[0].message.content
        
    elif "Gemini" in prov:
        genai.configure(api_key=apiKey)
        # Gemini usa 'user' y 'model' en los turnos
        gemini_messages = []
        for msg in context_messages:
            if msg["role"] == "system": continue # Ya config en la instance
            role = "model" if msg["role"] == "assistant" else "user"
            gemini_messages.append({"role": role, "parts": [msg["content"]]})
             
        try:
            model = genai.GenerativeModel(
                 gemini_model,
                 system_instruction=SYSTEM_PROMPT
            )
            response = model.generate_content(
                gemini_messages,
                generation_config=genai.types.GenerationConfig(temperature=0.85)
            )
            return response.text
        except Exception as e:
            # Capturar errores 429 para que no haga fallback inútil y confunda al usuario
            err_str = str(e).lower()
            if "resourceexhausted" in err_str or "429" in err_str or "quota" in err_str:
                raise e
                
            # Si es otro error (por ejemplo, modelo no disponible), intentamos fallback al otro modelo 1.5
            fallback_model = "gemini-1.5-pro" if gemini_model == "gemini-1.5-flash" else "gemini-1.5-flash"
            try:
                model = genai.GenerativeModel(
                     fallback_model,
                     system_instruction=SYSTEM_PROMPT
                )
                response = model.generate_content(
                    gemini_messages,
                    generation_config=genai.types.GenerationConfig(temperature=0.85)
                )
                return response.text
            except Exception:
                # Si el fallback también falla, lanzar el error original
                raise e

# ==========================================
# RENDERIZADO DEL CHAT EN PANTALLA
# ==========================================
# Mostrar del buffer todos MENOS el system
for msg in st.session_state.messages:
    if msg["role"] == "system": continue
    avatar_icon = "🐉" if msg["role"]=="assistant" else "🧙‍♂️"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])

# Verificación de inicio (Si solo hay sistema, incitamos a la IA a que envíe la introducción solita)
if len(st.session_state.messages) == 1:
    if api_key:
        st.session_state.messages.append({"role": "user", "content": "Estoy preparado. Da inicio a la partida."})
        st.rerun()
    else:
        st.info("👈 ¡Introduce tu API Key en el panel izquierdo y preparate para bajar al abismo! (Puedes usar APIs gratuitas como Gemini O Groq)")

# ==========================================
# INTERACCIÓN DEL JUGADOR
# ==========================================
if prompt := st.chat_input("Escribe tu próxima acción o conjuro (ej: Ataco al orco con mi espada)..."):
    if not api_key:
        st.warning("El portal mágico necesita de una llave de acceso (API Key).")
    else:
        # Añade lo que teclea el jugador al historial general
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧙‍♂️"):
            st.markdown(prompt)
            
        with st.chat_message("assistant", avatar="🐉"):
            with st.spinner("El Dungeon Master tira los dados detrás de su pantalla..."):
                try:
                    # Aplicamos el Buffer Window Memory para mandar al LLM (Reto 100% conseguido)
                    context_optimizado = apply_memory_buffer(st.session_state.messages, memoria_turns)
                    
                    # Llamada pasándole el modelo de Gemini seleccionado
                    respuesta = call_llm(context_optimizado, api_key, proveedor, model_gemini)
                    st.markdown(respuesta)
                    
                    # Archivar respuesta
                    st.session_state.messages.append({"role": "assistant", "content": respuesta})
                except Exception as e:
                    # Detectar si es un error 429 (Resource Exhausted / Rate Limit / Too Many Requests)
                    err_str = str(e).lower()
                    is_rate_limit = False
                    
                    if "resourceexhausted" in err_str or "429" in err_str or "quota" in err_str or "rate limit" in err_str:
                        is_rate_limit = True
                    
                    if is_rate_limit:
                        st.markdown(f"""
                        <div style="background-color: #1e1315; border: 2px solid #8b0000; border-radius: 8px; padding: 20px; color: #f2dede; margin-top: 10px; border-left: 5px solid #ff4d4d; font-family: 'Georgia', serif;">
                            <h3 style="color: #ff4d4d; margin-top: 0; font-family: 'Courier New', monospace; text-shadow: 1px 1px 2px #000; font-size: 1.3em;">
                                🛑 EL DUNGEON MASTER ESTÁ AGOTADO (Error 429 / Cuota Excedida)
                            </h3>
                            <p style="font-size: 1.05em; line-height: 1.5; margin-bottom: 15px;">
                                <em>"La energía arcana del portal se ha distorsionado. El Dungeon Master ha narrado demasiados universos seguidos y necesita un breve descanso para recuperar su maná y consultar sus pergaminos."</em>
                            </p>
                            <hr style="border: 0; border-top: 1px solid #5a1a1a; margin: 15px 0;">
                            <h4 style="color: #e6b333; margin-bottom: 8px; font-family: 'Courier New', monospace;">🔮 ¿Por qué ha ocurrido esto en tu plan gratuito?</h4>
                            <ul style="margin-left: 20px; padding-left: 0; line-height: 1.5; font-size: 0.95em;">
                                <li><b>Límite de Consultas por Minuto/Día:</b> Has realizado demasiadas acciones seguidas o has alcanzado el tope diario del plan gratuito de Google Gemini.</li>
                                <li><b>Saturación del Búfer de Memoria:</b> El historial actual es muy extenso. Al enviar muchos mensajes pasados a la vez, se consumen rápidamente los tokens de entrada permitidos por Google.</li>
                            </ul>
                            <h4 style="color: #e6b333; margin-top: 15px; margin-bottom: 8px; font-family: 'Courier New', monospace;">🛡️ ¿Cómo puedes solucionarlo ahora mismo?</h4>
                            <ol style="margin-left: 20px; padding-left: 0; line-height: 1.5; font-size: 0.95em;">
                                <li><b>Reduce la memoria en el panel izquierdo:</b> Mueve el control deslizante de <i>"Tamaño del Buffer (Turnos recordados)"</i> a <b>1 o 2</b> para consumir menos recursos arcanos (tokens).</li>
                                <li><b>Cambia el modelo a Gemini 1.5 Flash:</b> Si estabas usando <i>gemini-1.5-pro</i>, cámbialo a <b>gemini-1.5-flash</b> en la barra lateral; es mucho más rápido y tiene límites de cuota significativamente más altos.</li>
                                <li><b>Espera un momento:</b> Los límites por minuto se restablecen solos. Espera <b>30-60 segundos</b> y realiza tu próxima acción.</li>
                                <li><b>Usa un proveedor alternativo:</b> Si tienes una clave de <b>Groq</b> (también gratis), puedes cambiar de motor en el menú izquierdo para continuar tu partida sin pausas.</li>
                            </ol>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"Se ha roto una cuerda del telar del tiempo: {e}")
