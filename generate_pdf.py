import os
from fpdf import FPDF

class ProyectoPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            # Encabezado
            self.set_font("helvetica", "I", 8)
            self.set_text_color(140, 110, 80) # Beige RPG
            self.cell(0, 10, "EL ABISMO INFINITO - AI DUNGEON MASTER | DOCUMENTACION DEL PROYECTO", border=0, ln=1, align="R")
            # Linea decorativa
            self.set_draw_color(139, 0, 0) # Rojo oscuro
            self.set_line_width(0.4)
            self.line(15, 22, 195, 22)
            self.ln(5)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font("helvetica", "I", 8)
            self.set_text_color(140, 110, 80)
            self.set_draw_color(59, 49, 39)
            self.set_line_width(0.2)
            self.line(15, 280, 195, 280)
            self.cell(0, 10, f"Pagina {self.page_no()}", border=0, align="C")

def crear_pdf():
    pdf = ProyectoPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(15, 20, 15)
    
    # ----------------------------------------------------
    # PAGINA DE PORTADA (COVER PAGE)
    # ----------------------------------------------------
    pdf.add_page()
    
    # Fondo oscuro de la portada (Bloque superior decorativo)
    pdf.set_fill_color(11, 15, 25) # Azul oscuro de la app
    pdf.rect(0, 0, 210, 297, "F")
    
    # Bordes dorados de portada
    pdf.set_draw_color(230, 179, 51) # Dorado RPG
    pdf.set_line_width(1.5)
    pdf.rect(10, 10, 190, 277)
    
    pdf.ln(30)
    
    # Titulo de Portada
    pdf.set_font("helvetica", "B", 36)
    pdf.set_text_color(230, 179, 51) # Dorado
    pdf.cell(0, 15, "EL ABISMO INFINITO", border=0, ln=1, align="C")
    
    pdf.ln(5)
    
    # Subtitulo
    pdf.set_font("helvetica", "B", 18)
    pdf.set_text_color(216, 194, 158) # Beige
    pdf.cell(0, 10, "Juego de Rol de Texto y Dungeon Master Inteligente", border=0, ln=1, align="C")
    
    pdf.ln(25)
    
    # Bloque de Enlaces de Acceso y Credenciales
    pdf.set_fill_color(18, 16, 22) # Fondo gris-purpura oscuro
    pdf.rect(20, 100, 170, 75, "DF")
    
    pdf.set_y(105)
    pdf.set_font("helvetica", "B", 13)
    pdf.set_text_color(255, 77, 77) # Rojo
    pdf.cell(0, 8, "   CREDENCIALES Y ACCESO DEL PROYECTO", border=0, ln=1, align="C")
    
    pdf.ln(5)
    
    # Enlace de la app
    pdf.set_x(25)
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(216, 194, 158)
    pdf.write(8, "Aplicacion Desplegada: ")
    pdf.set_text_color(52, 152, 219) # Azul brillante
    pdf.write(8, "https://juegoiaizanmoros.streamlit.app/\n")
    
    # API Key
    pdf.set_x(25)
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(216, 194, 158)
    pdf.write(8, "API Key de Acceso (Google Gemini): \n")
    pdf.set_x(25)
    pdf.set_font("courier", "B", 11)
    pdf.set_text_color(46, 204, 113) # Verde brillante
    pdf.write(8, "AIzaSyAdJoPY7Q-ZyBEJWMXVvDffzeMCkVs2Mzw\n")
    
    pdf.ln(35)
    
    # Informacion del Autor/Curso
    pdf.set_font("helvetica", "I", 12)
    pdf.set_text_color(216, 194, 158)
    pdf.cell(0, 8, "Proyecto de Inteligencia Artificial Avanzada", border=0, ln=1, align="C")
    pdf.cell(0, 8, "Dungeon Master Generativo con Arquitectura Streamlit", border=0, ln=1, align="C")
    
    pdf.ln(25)
    
    # Pie de portada
    pdf.set_font("helvetica", "B", 10)
    pdf.set_text_color(230, 179, 51)
    pdf.cell(0, 10, "MAY 2026", border=0, ln=1, align="C")
    
    # ----------------------------------------------------
    # PAGINA 2: INTRODUCCION Y PROPÓSITO (PARTE 1)
    # ----------------------------------------------------
    pdf.add_page()
    pdf.set_text_color(0, 0, 0) # Reset color a negro para lectura comoda
    
    # Titulo de Seccion
    pdf.set_font("helvetica", "B", 16)
    pdf.set_text_color(139, 0, 0) # Rojo oscuro
    pdf.cell(0, 10, "PARTE 1: INTRODUCCION Y PROPÓSITO DEL PROYECTO", border=0, ln=1)
    pdf.ln(5)
    
    # Contenido
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    
    texto_p1 = (
        "El Abismo Infinito es un Producto Minimo Viable (MVP) innovador que automatiza el rol de un "
        "Dungeon Master (DM) en juegos de rol de mesa clasicos (como Dungeons & Dragons), utilizando modelos de "
        "lenguaje de ultima generacion (LLM) a traves de una interfaz web interactiva e inmersiva.\n\n"
        "El objetivo principal es ofrecer una experiencia de juego narrativa infinita y personalizada, gobernada "
        "por la imaginacion del usuario, pero guiada de forma coherente, balanceada y descriptiva por la IA. "
        "El sistema interactua directamente con el jugador, describiendo el entorno con un lenguaje epico de fantasia "
        "oscura, evaluando las acciones del usuario y proponiendo alternativas estructuradas sin arrebatarle el "
        "control sobre sus propias decisiones.\n\n"
        "Este proyecto destaca por aplicar tecnicas avanzadas de optimizacion de contexto e ingenieria de prompts "
        "para solucionar las dos barreras mas comunes en el uso gratuito de APIs de inteligencia artificial:\n"
        "1. La perdida de coherencia o memoria a corto plazo tras varios turnos de conversacion.\n"
        "2. El bloqueo de servicios por exceder los limites de cuotas en planes gratuitos (Error 429)."
    )
    pdf.multi_cell(0, 6, texto_p1)
    
    pdf.ln(10)
    
    # ----------------------------------------------------
    # ARQUITECTURA Y INTEGRACIONES (PARTE 2)
    # ----------------------------------------------------
    pdf.set_font("helvetica", "B", 16)
    pdf.set_text_color(139, 0, 0)
    pdf.cell(0, 10, "PARTE 2: ARQUITECTURA Y INTEGRACIONES DE MODELOS (2026)", border=0, ln=1)
    pdf.ln(5)
    
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    
    texto_p2 = (
        "El core de la aplicacion esta construido sobre Python 3.x y Streamlit, lo que permite un renderizado reactivo "
        "y fluido de la interfaz de chat. La arquitectura de conexion de modelos de lenguaje esta diseñada de forma "
        "modular, permitiendo al usuario cambiar en tiempo real entre tres motores LLM distintos:\n\n"
        "A) Google Gemini (Recomendado): Integra el SDK oficial de Google. En el año 2026, la plataforma ha "
        "actualizado sus modelos e interfaces de v1beta, por lo que el sistema esta optimizado para trabajar con:\n"
        "  - gemini-2.5-flash: El modelo de alta velocidad, ultra eficiente y con cuotas amplias en la capa gratuita.\n"
        "  - gemini-2.5-pro: Modelo altamente analitico, excelente para campañas complejas pero con cuotas estrictas.\n"
        "  - gemini-3.5-flash: Modelo de ultima generacion con un balance superior entre latencia y coherencia narrativa.\n"
        "  - gemini-3.1-pro: Variante avanzada para deducciones detalladas y tramas profundas.\n\n"
        "B) Groq: Proporciona respuestas ultrarrapidas de baja latencia utilizando el modelo de codigo abierto "
        "llama3-8b-8192, ideal para mantener un flujo de chat instantaneo sin coste alguno.\n\n"
        "C) OpenAI: Conector compatible con GPT-3.5 Turbo o superior para jugadores que prefieren la consistencia "
        "del ecosistema de OpenAI."
    )
    pdf.multi_cell(0, 6, texto_p2)
    
    # ----------------------------------------------------
    # SECCION 3: GESTION DE MEMORIA (PARTE 3)
    # ----------------------------------------------------
    pdf.add_page()
    
    pdf.set_font("helvetica", "B", 16)
    pdf.set_text_color(139, 0, 0)
    pdf.cell(0, 10, "PARTE 3: GESTION DE MEMORIA (CONVERSATION BUFFER WINDOW)", border=0, ln=1)
    pdf.ln(5)
    
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    
    texto_p3 = (
        "Los modelos de lenguaje son apastridas (stateless); no recuerdan el contenido de los mensajes anteriores. "
        "Para simular memoria, los sistemas tradicionales reinyectan todo el historial en cada turno. Sin embargo, en el "
        "plan gratuito de las APIs (como Gemini o OpenAI), esto causa una saturacion veloz de los limites de tokens de entrada "
        "disponibles por minuto, resultando en bloqueos constantes.\n\n"
        "Para solucionar este reto, El Abismo Infinito implementa un algoritmo personalizado de "
        "ConversationBufferWindowMemory (inspirado en frameworks como LangChain):\n\n"
        "1. Estructura de Mensajes Fija: Se mantiene permanentemente el primer mensaje (System Prompt) en la posicion 0. "
        "Este prompt le enseña a la IA su rol estricto como Dungeon Master, las reglas de interaccion (no actuar por el "
        "usuario y ofrecer 3 opciones de viñetas al final).\n"
        "2. Ventana Deslizante (Slider de Memoria): El usuario puede elegir a traves de un control deslizante interactivo "
        "en la barra lateral el numero de turnos recordados (N). Un turno consta de un par de mensajes (Accion del usuario + "
        "Respuesta del DM).\n"
        "3. Filtro Dinamico de Contexto: La funcion apply_memory_buffer recorta el historial para mantener solo el System Prompt "
        "y los ultimos N*2 mensajes. Todos los mensajes intermedios mas antiguos se descartan del buffer arrojado al LLM. "
        "Esto garantiza que el consumo de tokens sea lineal y controlado, extendiendo infinitamente la partida sin "
        "sobrecargar los limites de la API."
    )
    pdf.multi_cell(0, 6, texto_p3)
    
    pdf.ln(10)
    
    # ----------------------------------------------------
    # SECCION 4: MITIGACION DE ERRORES 429 (PARTE 4)
    # ----------------------------------------------------
    pdf.set_font("helvetica", "B", 16)
    pdf.set_text_color(139, 0, 0)
    pdf.cell(0, 10, "PARTE 4: MITIGACION DE ERRORES 429 Y MEJORAS DE UX", border=0, ln=1)
    pdf.ln(5)
    
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    
    texto_p4 = (
        "Cuando multiples peticiones rapidas o cargas extensas saturan la cuota del nivel gratuito, la API de Google "
        "retorna un codigo de estado 429 (Too Many Requests / Resource Exhausted). Para solventar esto y ofrecer una "
        "experiencia premium, se han desarrollado dos componentes criticos:\n\n"
        "A) Monitor de Consumo de Memoria en Barra Lateral:\n"
        "A traves de la funcion estimate_context_size, el sistema calcula en tiempo real el tamaño en caracteres y palabras "
        "del historial que se enviara en el siguiente turno. El usuario recibe un feedback visual inmersivo:\n"
        "  - Verde (Bajo/Seguro): Menos de 3000 caracteres. Garantiza partidas estables.\n"
        "  - Amarillo (Moderado): De 3000 a 7000 caracteres. Riesgo bajo de saturacion.\n"
        "  - Rojo (Alto/Peligroso): Mas de 7000 caracteres. Alerta al usuario para reducir el buffer antes del error.\n\n"
        "B) Tarjeta de Error Tematizada RPG:\n"
        "Si a pesar de todo la API arroja un error 429, el codigo intercepta la excepcion (google_exceptions.ResourceExhausted) "
        "y la transforma en un pergamino digital estilizado mediante HTML y CSS. El error deja de ser un traceback tecnico "
        "hostil y se convierte en un evento de rol: 'El Dungeon Master esta agotado y necesita recuperar mana'."
    )
    pdf.multi_cell(0, 6, texto_p4)
    
    # ----------------------------------------------------
    # SECCION 5: CREDENCIALES (PARTE 5)
    # ----------------------------------------------------
    pdf.add_page()
    
    pdf.set_font("helvetica", "B", 16)
    pdf.set_text_color(139, 0, 0)
    pdf.cell(0, 10, "PARTE 5: CREDENCIALES DE ACCESO Y ENLACES", border=0, ln=1)
    pdf.ln(5)
    
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    
    texto_p5 = (
        "Para facilitar la evaluacion e interaccion directa con el MVP del Dungeon Master de IA, se disponen "
        "de los siguientes recursos clave de acceso libre:\n\n"
        "1. APLICACION DESPLEGADA (URL STREAMLIT SHARE):\n"
        "La aplicacion esta hosteada de forma publica y es accesible desde cualquier navegador moderno en:\n"
        "https://juegoiaizanmoros.streamlit.app/\n\n"
        "2. CREDENCIAL DE ACCESO (GOOGLE AI STUDIO API KEY):\n"
        "Para que la aplicacion cobre vida, se requiere una llave de acceso. Puedes pegar la siguiente clave directamente "
        "en el panel lateral 'Grimorio del DM' en el campo 'Ingresa tu API Key' para activar los motores de Gemini:\n"
        "API KEY: AIzaSyAdJoPY7Q-ZyBEJWMXVvDffzeMCkVs2Mzw\n\n"
        "Esta llave esta configurada en el plan gratuito para propositos de testeo. Se recomienda usar el modelo "
        "gemini-2.5-flash para maxima velocidad y estabilidad."
    )
    pdf.multi_cell(0, 6, texto_p5)
    
    pdf.ln(10)
    
    # ----------------------------------------------------
    # SECCION 6: GUIA DE INSTALACION (PARTE 6)
    # ----------------------------------------------------
    pdf.set_font("helvetica", "B", 16)
    pdf.set_text_color(139, 0, 0)
    pdf.cell(0, 10, "PARTE 6: GUIA DE INSTALACION Y EJECUCION LOCAL", border=0, ln=1)
    pdf.ln(5)
    
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    
    texto_p6 = (
        "Si deseas clonar y ejecutar este proyecto en tu propia maquina, sigue estos pasos:\n\n"
        "Paso 1: Clonar el repositorio de GitHub:\n"
        "  git clone https://github.com/IzanMoros/JuegoIa.git\n"
        "  cd JuegoIa/proyecto_ia_mvp\n\n"
        "Paso 2: Instalar las dependencias de Python necesarias:\n"
        "  pip install -r requirements.txt\n\n"
        "Paso 3: Arrancar la aplicacion con Streamlit:\n"
        "  En Windows, ejecuta:\n"
        "  py -m streamlit run app.py\n\n"
        "  En MacOS/Linux, ejecuta:\n"
        "  python -m streamlit run app.py\n\n"
        "Paso 4: Abre tu navegador en la direccion local suministrada (normalmente http://localhost:8501), ingresa la API Key "
        "suministrada en este documento en la barra izquierda, selecciona tu modelo preferido y ¡da inicio a tu aventura!"
    )
    pdf.multi_cell(0, 6, texto_p6)

    # Guardar
    output_filename = "proyecto_dungeon_master_ia.pdf"
    pdf.output(output_filename)
    print(f"PDF generado exitosamente como '{output_filename}'")

if __name__ == "__main__":
    crear_pdf()
