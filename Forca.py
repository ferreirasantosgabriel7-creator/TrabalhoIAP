import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(
    page_title="Jogo da Forca Pro",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS AVANÇADO E ANIMAÇÕES ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800;900&family=JetBrains+Mono:wght@700;800&display=swap');

    /* Fundo animado sutil */
    .stApp {
        background: radial-gradient(circle at top right, #1e1b4b, #0f172a 60%, #090d16 100%);
        color: #f8fafc;
        font-family: 'Outfit', sans-serif;
    }

    /* Estilização da Barra Lateral */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Esconder barra superior padrão mas manter botão da sidebar acessível */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    #MainMenu, footer { visibility: hidden; }

    /* Cartões Glassmorphism */
    .glass-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        height: 100%;
    }

    /* Título Principal com Gradiente */
    .main-title {
        text-align: center;
        font-size: 3.4rem;
        font-weight: 900;
        letter-spacing: -1px;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
        text-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
    }

    .category-badge {
        display: inline-block;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(129, 140, 248, 0.4);
        color: #a5b4fc;
        padding: 6px 18px;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
    }

    /* Caixas individuais para as letras (Tiles) */
    .word-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
        margin: 20px 0 30px 0;
    }

    .letter-tile {
        width: 54px;
        height: 64px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 2rem;
        font-weight: 800;
        border-radius: 14px;
        background: rgba(15, 23, 42, 0.7);
        border: 2px solid rgba(56, 189, 248, 0.25);
        color: #38bdf8;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    .letter-tile.revealed {
        background: linear-gradient(145deg, rgba(56, 189, 248, 0.2), rgba(99, 102, 241, 0.2));
        border-color: #38bdf8;
        color: #ffffff;
        text-shadow: 0 0 15px rgba(56, 189, 248, 0.8);
        transform: translateY(-4px);
    }

    .letter-tile.missed {
        background: rgba(244, 63, 94, 0.15);
        border-color: #f43f5e;
        color: #fda4af;
    }

    /* Botões do Teclado */
    .stButton > button {
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #f8fafc;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.18s ease;
        min-height: 48px;
        padding: 0;
    }

    .stButton > button:hover:not(:disabled) {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-color: #a5b4fc;
        color: #ffffff;
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.45);
    }

    .stButton > button:active:not(:disabled) {
        transform: translateY(0px);
    }

    .stButton > button:disabled {
        background: rgba(15, 23, 42, 0.4);
        color: #475569;
        border: 1px solid rgba(255, 255, 255, 0.04);
        cursor: not-allowed;
    }

    /* Cards de Métricas na Sidebar */
    [data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 12px 16px;
        border-radius: 16px;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 800;
        color: #38bdf8;
    }

    /* Contêiner do SVG */
    .svg-container {
        display: flex;
        justify-content: center;
        align-items: center;
        background: rgba(15, 23, 42, 0.6);
        border-radius: 18px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        margin-bottom: 18px;
    }
</style>
""", unsafe_allow_html=True)


# --- FUNÇÃO DE ÁUDIO ---
def tocar_som(tipo):
    if tipo == "vitoria":
        notas = "[523.25, 659.25, 783.99, 1046.50]"
        wave = "triangle"
        step = 0.12
    else:
        notas = "[300, 250, 200, 150]"
        wave = "sawtooth"
        step = 0.18

    script = f"""
    <script>
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const notas = {notas};
        notas.forEach((freq, i) => {{
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = '{wave}';
            osc.frequency.setValueAtTime(freq, ctx.currentTime + i * {step});
            gain.gain.setValueAtTime(0.12, ctx.currentTime + i * {step});
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + i * {step} + 0.35);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(ctx.currentTime + i * {step});
            osc.stop(ctx.currentTime + i * {step} + 0.35);
        }});
    </script>
    """
    components.html(script, height=0, width=0)


# --- DESENHO VETORIAL (SVG) DA FORCA COM BRILHO NEON ---
def gerar_svg_forca(erros):
    cor_estrutura = "#64748b"
    cor_boneco = "#f43f5e" if erros >= 6 else "#38bdf8"
    brilho = f"filter: drop-shadow(0 0 8px {cor_boneco});"

    partes = [
        # 1: Cabeça
        f'<circle cx="150" cy="70" r="22" stroke="{cor_boneco}" stroke-width="4" fill="none" style="{brilho}" />',
        # 2: Tronco
        f'<line x1="150" y1="92" x2="150" y2="150" stroke="{cor_boneco}" stroke-width="4" stroke-linecap="round" style="{brilho}" />',
        # 3: Braço Esquerdo
        f'<line x1="150" y1="110" x2="120" y2="135" stroke="{cor_boneco}" stroke-width="4" stroke-linecap="round" style="{brilho}" />',
        # 4: Braço Direito
        f'<line x1="150" y1="110" x2="180" y2="135" stroke="{cor_boneco}" stroke-width="4" stroke-linecap="round" style="{brilho}" />',
        # 5: Perna Esquerda
        f'<line x1="150" y1="150" x2="125" y2="190" stroke="{cor_boneco}" stroke-width="4" stroke-linecap="round" style="{brilho}" />',
        # 6: Perna Direita + Olhos de derrota
        f'''<line x1="150" y1="150" x2="175" y2="190" stroke="{cor_boneco}" stroke-width="4" stroke-linecap="round" style="{brilho}" />
            <path d="M141 64 L147 70 M147 64 L141 70 M153 64 L159 70 M159 64 L153 70" stroke="{cor_boneco}" stroke-width="2.5" stroke-linecap="round" />'''
    ]

    corpo_desenhado = "".join(partes[:erros])

    return f"""
    <div class="svg-container">
        <svg width="220" height="230" viewBox="0 0 220 230">
            <!-- Base e Estrutura da Forca -->
            <line x1="20" y1="210" x2="110" y2="210" stroke="{cor_estrutura}" stroke-width="5" stroke-linecap="round" />
            <line x1="65" y1="210" x2="65" y2="20" stroke="{cor_estrutura}" stroke-width="5" stroke-linecap="round" />
            <line x1="65" y1="20" x2="150" y2="20" stroke="{cor_estrutura}" stroke-width="5" stroke-linecap="round" />
            <line x1="65" y1="50" x2="95" y2="20" stroke="{cor_estrutura}" stroke-width="4" stroke-linecap="round" />
            <!-- Corda -->
            <line x1="150" y1="20" x2="150" y2="48" stroke="#94a3b8" stroke-width="3" stroke-dasharray="4 2" />
            <!-- Boneco -->
            {corpo_desenhado}
        </svg>
    </div>
    """


CATEGORIAS = {
    "💻 Programação": ["PYTHON", "STREAMLIT", "ALGORITMO", "VARIAVEL", "DESENVOLVIMENTO", "COMPILADOR", "FRAMEWORK"],
    "🚀 Tecnologia": ["INTERNET", "CIBERSEGURANCA", "HARDWARE", "SOFTWARE", "INTELIGENCIA", "SERVIDOR", "NUVEM"],
    "🌍 Geral": ["BRASIL", "FUTEBOL", "UNIVERSO", "TECLADO", "DESAFIO", "ASTRONOMIA", "OCEANO"]
}

# --- INICIALIZAÇÃO DO SESSION STATE ---
for chave, valor in [("vitorias", 0), ("derrotas", 0), ("sequencia", 0), ("pontos", 0)]:
    if chave not in st.session_state:
        st.session_state[chave] = valor


def iniciar_jogo(categoria_escolhida=None):
    if categoria_escolhida and categoria_escolhida != "🎲 Aleatório":
        cat = categoria_escolhida
    else:
        cat = random.choice(list(CATEGORIAS.keys()))

    st.session_state.categoria = cat
    st.session_state.palavra_secreta = random.choice(CATEGORIAS[cat])
    st.session_state.erros = 0
    st.session_state.letras_chutadas = set()
    st.session_state.pop("partida_terminada", None)


if "palavra_secreta" not in st.session_state:
    iniciar_jogo()


def processar_letra(letra):
    if letra not in st.session_state.letras_chutadas:
        st.session_state.letras_chutadas.add(letra)
        if letra not in st.session_state.palavra_secreta:
            st.session_state.erros += 1
            st.toast(f"A letra '{letra}' não está na palavra!", icon="❌")
        else:
            st.toast(f"Boa! Acertaste a letra '{letra}'!", icon="✨")


# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("## ⚙️ Configurações")
    cat_selecionada = st.selectbox(
        "Categoria das Palavras:",
        ["🎲 Aleatório"] + list(CATEGORIAS.keys())
    )

    if st.button("🔄 Nova Palavra", use_container_width=True):
        iniciar_jogo(cat_selecionada)
        st.rerun()

    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("## 🏆 Desempenho")

    st.metric(label="Pontuação Total", value=f"{st.session_state.pontos} pts")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric(label="Vitórias", value=st.session_state.vitorias)
    with col_s2:
        st.metric(label="Derrotas", value=st.session_state.derrotas)

    st.metric(label="Sequência Invicta", value=f"{st.session_state.sequencia} 🔥")

# --- CABEÇALHO PRINCIPAL ---
st.markdown("<h1 class='main-title'>JOGO DA FORCA PRO</h1>", unsafe_allow_html=True)
st.markdown(
    f"<div style='text-align: center; margin-bottom: 28px;'><span class='category-badge'>{st.session_state.categoria}</span></div>",
    unsafe_allow_html=True
)

# --- ÁREA DO JOGO ---
col_left, col_right = st.columns([1, 1.5], gap="large")

with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; font-weight:800; color:#f1f5f9;'>⚡ Status da Forca</h3>",
                unsafe_allow_html=True)

    # Renderiza o SVG dinâmico
    st.markdown(gerar_svg_forca(st.session_state.erros), unsafe_allow_html=True)

    vidas_restantes = 6 - st.session_state.erros
    coracoes = "❤️ " * vidas_restantes + "🖤 " * st.session_state.erros
    st.markdown(f"<div style='text-align:center; font-size:1.3rem; margin-bottom:10px;'>{coracoes}</div>",
                unsafe_allow_html=True)
    st.progress(max(0.0, vidas_restantes / 6))
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; font-weight:800; color:#f1f5f9;'>🎯 Descubra a Palavra</h3>",
                unsafe_allow_html=True)

    ganhou = all(letra in st.session_state.letras_chutadas for letra in st.session_state.palavra_secreta)
    perdeu = st.session_state.erros >= 6

    # Renderiza as caixas (tiles) de cada letra
    tiles_html = '<div class="word-container">'
    for letra in st.session_state.palavra_secreta:
        if letra in st.session_state.letras_chutadas:
            tiles_html += f'<div class="letter-tile revealed">{letra}</div>'
        elif perdeu:
            tiles_html += f'<div class="letter-tile missed">{letra}</div>'
        else:
            tiles_html += '<div class="letter-tile"></div>'
    tiles_html += '</div>'
    st.markdown(tiles_html, unsafe_allow_html=True)

    # Estados de Fim de Jogo ou Teclado
    if ganhou:
        if "partida_terminada" not in st.session_state:
            st.session_state.vitorias += 1
            st.session_state.sequencia += 1
            st.session_state.pontos += 100 + (vidas_restantes * 15)
            st.session_state.partida_terminada = True
            tocar_som("vitoria")

        st.balloons()
        st.success(f"🏆 **INCRÍVEL!** Venceste com {vidas_restantes} vida(s) restante(s)!")
        if st.button("🚀 Próxima Palavra", use_container_width=True):
            iniciar_jogo(cat_selecionada)
            st.rerun()

    elif perdeu:
        if "partida_terminada" not in st.session_state:
            st.session_state.derrotas += 1
            st.session_state.sequencia = 0
            st.session_state.partida_terminada = True
            tocar_som("derrota")

        st.error("💀 **FIM DE JOGO!** As letras que faltavam foram reveladas em vermelho acima.")
        if st.button("🔄 Tentar Novamente", use_container_width=True):
            iniciar_jogo(cat_selecionada)
            st.rerun()

    else:
        # Mostra resumo das letras erradas
        letras_erradas = sorted(
            [l for l in st.session_state.letras_chutadas if l not in st.session_state.palavra_secreta])
        if letras_erradas:
            erradas_str = " • ".join(letras_erradas)
            st.markdown(
                f"<p style='text-align:center; color:#fb7185; font-size:0.95rem;'>Letras erradas: <b>{erradas_str}</b></p>",
                unsafe_allow_html=True)
        else:
            st.markdown(
                "<p style='text-align:center; color:#94a3b8; font-size:0.95rem;'>Nenhum erro até agora. Escolha uma letra abaixo:</p>",
                unsafe_allow_html=True)

        linhas_teclado = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["Z", "X", "C", "V", "B", "N", "M"]
        ]

        for linha in linhas_teclado:
            cols = st.columns(len(linha))
            for i, letra in enumerate(linha):
                ja_usada = letra in st.session_state.letras_chutadas
                # Indica visualmente no botão se a letra já usada foi acerto ou erro
                label_btn = letra
                if ja_usada:
                    label_btn = f"✓{letra}" if letra in st.session_state.palavra_secreta else f"✕{letra}"

                with cols[i]:
                    st.button(
                        label_btn,
                        key=f"btn_{letra}",
                        disabled=ja_usada,
                        on_click=processar_letra,
                        args=(letra,),
                        use_container_width=True
                    )
    st.markdown('</div>', unsafe_allow_html=True)