import language_tool_python
import streamlit as st
import fitz  # PyMuPDF



# Configurar o layout da página
st.set_page_config(page_title="Corretor Ortográfico", page_icon="✅", layout="centered")

st.header("APP DE CORREÇÃO ORTOGRÁFICA ✅")

# Inicializar o corretor para a língua portuguesa
# tool = language_tool_python.LanguageTool('pt-BR')
tool = language_tool_python.LanguageToolPublicAPI('pt-BR')

# Inicializar as variáveis de sessão para armazenamento do texto
if "text" not in st.session_state:
    st.session_state.text = ""


# Seletor de entrada de texto ou PDF
input_option = st.radio("Escolha a forma de entrada:", ('Texto', 'PDF'))

if input_option == 'Texto':
    # Entrada de texto
    st.session_state.text = st.text_area("Digite seu texto aqui:", height=200)
elif input_option == 'PDF':
    # Upload de PDF
    uploaded_file = st.file_uploader("Carregar arquivo PDF", type=["pdf"])
    st.session_state.text = ""
    if uploaded_file is not None:
        # Ler o PDF e extrair texto
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            st.session_state.text += page.get_text()

if st.button("Corrigir Texto"):
    if st.session_state.text:
    # Corrigir o texto
        matches = tool.check(st.session_state.text)
        corrected_text = language_tool_python.utils.correct(st.session_state.text, matches)

        # Exibir o texto corrigido
        st.subheader("Texto corrigido:")
        st.success(corrected_text)

        # Verificar as correspondências encontradas e suas sugestões
        if matches:
            st.subheader("Erros encontrados e sugestões:")
            for match in matches:
                st.markdown(f"**Erro:** {match.ruleId}")
                st.markdown(f"**Mensagem:** {match.message}")
                st.markdown(f"**Contexto:** {match.context}")
                st.markdown(f"**Sugestões:** {', '.join(match.replacements)}")
                st.markdown("---")
        else:
            st.info("Nenhum erro encontrado.")
    else:
        st.warning("Por favor, insira um texto para correção ou carregue um PDF.")




# Rodapé com informações adicionais
st.sidebar.title("Sobre o aplicativo")
st.sidebar.info("""
Este aplicativo utiliza a biblioteca `language_tool_python` para realizar correções ortográficas e gramaticais em textos em português.
Desenvolvido por Rafael Galvão.
""")
# Adicionar estilo para o botão de resetar
st.sidebar.markdown(
    """
    <style>
    div.stButton > button:first-child {
        background-color: red;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        width: 100%;
        text-align: center;
    }
    div.stButton > button:first-child:hover {
        background-color: darkred;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Adicionar botão de resetar na barra lateral
if st.sidebar.button("Resetar / Reiniciar"):
    st.session_state.text = ""
    st.rerun()

