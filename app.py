import streamlit as st
import time

try:
    from openai import OpenAI
except ImportError:
    st.error("Error: Librería 'openai' no instalada.")

try:
    import google.generativeai as genai
except ImportError:
    st.error("Error: Librería 'google-generativeai' no instalada.")


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
    # IMPORTANTE: Nunca subas a GitHub tu clave real. Pégala aquí solo temporalmente o usa st.secrets.
    api_key = st.text_input("Ingresa tu API Key (No se guarda):", value="TU_API_KEY_AQUI", type="password")
    
    st.markdown("---")
    st.subheader("📚 Gestión de Memoria")
    
    memoria_turns = st.slider("Tamaño del Buffer (Turnos recordados):", min_value=1, max_value=6, value=3)
    
    st.markdown("""
    **¿Qué es el Memory Buffer?**
    La IA normalmente "no tiene memoria". Pierde el contexto tras cada mensaje. 
    Aquí aplicamos un *ConversationBufferWindowMemory*: Recortamos el historial a los últimos X mensajes para evitar saturar el límite de *Tokens* y lo inyectamos junto al System Prompt cada vez que hablas.
    """)
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

def apply_memory_buffer(messages, window_size):
    """
    Simula LangChain's ConversationBufferWindowMemory.
    Retiene el system prompt (índice 0) y los últimos N * 2 mensajes (ida y vuelta del usuario + IA).
    """
    system_msg = [messages[0]]
    chat_history = messages[1:]
    # Un "turno" son 2 mensajes: pregunta del user + respuesta de IA
    limit = window_size * 2
    
    if len(chat_history) > limit:
        chat_history = chat_history[-limit:]
        
    return system_msg + chat_history

def call_llm(context_messages, apiKey, prov):
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
                 'gemini-flash-latest',
                 system_instruction=SYSTEM_PROMPT
            )
            response = model.generate_content(
                gemini_messages,
                generation_config=genai.types.GenerationConfig(temperature=0.85)
            )
        except Exception:
            model = genai.GenerativeModel(
                 'gemini-pro-latest',
                 system_instruction=SYSTEM_PROMPT
            )
            response = model.generate_content(
                gemini_messages,
                generation_config=genai.types.GenerationConfig(temperature=0.85)
            )
        return response.text

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
                    
                    # Llamada
                    respuesta = call_llm(context_optimizado, api_key, proveedor)
                    st.markdown(respuesta)
                    
                    # Archivar respuesta
                    st.session_state.messages.append({"role": "assistant", "content": respuesta})
                except Exception as e:
                    st.error(f"Se ha roto una cuerda del telar del tiempo: {e}")
