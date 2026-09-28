import streamlit as st
import pandas as pd
import re

# =========================================================
# CONFIGURAÇÃO
# =========================================================

st.set_page_config(
    page_title="NOVA Store",
    page_icon="🛍️",
    layout="wide"
)

# =========================================================
# ESTILO
# =========================================================

st.markdown("""
<style>
    .stApp {
        background-color: #f5f6f8;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        color: #666;
        font-size: 18px;
        margin-bottom: 25px;
    }

    .banner {
        padding: 35px;
        border-radius: 20px;
        background: #111827;
        color: white;
        text-align: center;
        margin: 20px 0 30px 0;
    }

    .banner h1 {
        margin: 0;
        font-size: 34px;
    }

    .banner p {
        margin-top: 10px;
        color: #d1d5db;
    }

    .price {
        font-size: 24px;
        font-weight: 800;
    }

    .cart-total {
        font-size: 28px;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# PRODUTOS COM PANDAS
# =========================================================

dados_produtos = {
    "nome": [
        "Fone de Ouvido Bluetooth Pro",
        "Smartwatch Fitness Pro",
        "Caixa de Som Bluetooth Premium",
        "Teclado Mecânico Gamer RGB",
        "Mouse Gamer RGB Pro",
        "Power Bank Ultra 20.000mAh",
    ],
    "categoria": [
        "Áudio",
        "Tecnologia",
        "Áudio",
        "Computadores",
        "Computadores",
        "Acessórios",
    ],
    "preco": [
        149.90,
        229.90,
        189.90,
        249.90,
        129.90,
        119.90,
    ],
    "emoji": [
        "🎧",
        "⌚",
        "🔊",
        "⌨️",
        "🖱️",
        "🔋",
    ],
}

produtos = pd.DataFrame(dados_produtos)

# =========================================================
# CARRINHO
# =========================================================

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

if "checkout" not in st.session_state:
    st.session_state.checkout = False

# =========================================================
# FUNÇÕES DE VALIDAÇÃO
# =========================================================

def limpar_numeros(valor):
    return re.sub(r"\D", "", valor)


def cpf_valido(cpf):
    cpf = limpar_numeros(cpf)

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    if digito1 != int(cpf[9]):
        return False

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    return digito2 == int(cpf[10])


def email_valido(email):
    padrao = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.fullmatch(padrao, email.strip()) is not None


def nome_valido(nome):
    partes = nome.strip().split()

    if len(partes) < 2:
        return False

    return all(
        parte.replace("-", "").replace("'", "").isalpha()
        for parte in partes
    )


def formatar_cpf(cpf):
    numeros = limpar_numeros(cpf)[:11]

    if len(numeros) <= 3:
        return numeros

    if len(numeros) <= 6:
        return f"{numeros[:3]}.{numeros[3:]}"

    if len(numeros) <= 9:
        return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:]}"

    return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"


def formatar_cep(cep):
    numeros = limpar_numeros(cep)[:8]

    if len(numeros) <= 5:
        return numeros

    return f"{numeros[:5]}-{numeros[5:]}"


# =========================================================
# CABEÇALHO
# =========================================================

st.markdown(
    '<div class="main-title">🛍️ NOVA Store</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Tecnologia, acessórios e produtos para o seu dia a dia.</div>',
    unsafe_allow_html=True
)

# =========================================================
# BANNER
# =========================================================

st.markdown("""
<div class="banner">
    <h1>🔥 OFERTAS ESPECIAIS</h1>
    <p>Produtos selecionados com preços especiais.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# PESQUISA
# =========================================================

col_busca, col_categoria, col_carrinho = st.columns([2, 2, 1])

with col_busca:
    busca = st.text_input(
        "🔎 Buscar produto",
        placeholder="Digite o nome do produto..."
    )

with col_categoria:
    categorias = ["Todos"] + sorted(
        produtos["categoria"].unique().tolist()
    )

    categoria = st.selectbox(
        "🏷️ Categoria",
        categorias
    )

with col_carrinho:
    st.write("")
    st.metric(
        "🛒 Carrinho",
        len(st.session_state.carrinho)
    )

# =========================================================
# FILTRO COM PANDAS
# =========================================================

produtos_filtrados = produtos.copy()

if busca:
    produtos_filtrados = produtos_filtrados[
        produtos_filtrados["nome"].str.contains(
            busca,
            case=False,
            na=False
        )
    ]

if categoria != "Todos":
    produtos_filtrados = produtos_filtrados[
        produtos_filtrados["categoria"] == categoria
    ]

# =========================================================
# PRODUTOS
# =========================================================

st.header("🛍️ Nossos produtos")

if produtos_filtrados.empty:
    st.warning("Nenhum produto encontrado.")

else:
    colunas = st.columns(3)

    for posicao, (_, produto) in enumerate(
        produtos_filtrados.iterrows()
    ):

        with colunas[posicao % 3]:

            with st.container(border=True):

                st.markdown(
                    f"<div style='text-align:center;font-size:70px'>{produto['emoji']}</div>",
                    unsafe_allow_html=True
                )

                st.subheader(produto["nome"])

                st.caption(produto["categoria"])

                st.markdown(
                    f'<div class="price">R$ {produto["preco"]:.2f}</div>',
                    unsafe_allow_html=True
                )

                if st.button(
                    "🛒 Adicionar ao carrinho",
                    key=f"add_{produto['nome']}",
                    use_container_width=True
                ):
                    st.session_state.carrinho.append(
                        {
                            "nome": produto["nome"],
                            "categoria": produto["categoria"],
                            "preco": float(produto["preco"]),
                            "emoji": produto["emoji"],
                        }
                    )

                    st.success("Produto adicionado!")

# =========================================================
# CARRINHO
# =========================================================

st.divider()
st.header("🛒 Seu carrinho")

if not st.session_state.carrinho:

    st.info("Seu carrinho está vazio.")

else:

    total = 0

    for i, item in enumerate(st.session_state.carrinho):

        c1, c2, c3 = st.columns([4, 2, 1])

        with c1:
            st.write(
                f"{item['emoji']} **{item['nome']}**"
            )

        with c2:
            st.write(
                f"R$ {item['preco']:.2f}"
            )

        with c3:
            if st.button(
                "❌",
                key=f"remove_{i}"
            ):
                st.session_state.carrinho.pop(i)
                st.rerun()

        total += item["preco"]

    st.divider()

    st.markdown(
        f'<div class="cart-total">Total: R$ {total:.2f}</div>',
        unsafe_allow_html=True
    )

    st.write("")

    if st.button(
        "💳 Ir para o pagamento",
        use_container_width=True
    ):
        st.session_state.checkout = True
        st.rerun()

# =========================================================
# CHECKOUT
# =========================================================

if st.session_state.checkout and st.session_state.carrinho:

    st.divider()
    st.header("💳 Finalizar pedido")

    st.write(
        "Preencha os dados corretamente para concluir a compra."
    )

    nome = st.text_input(
        "Nome completo",
        placeholder="Ex.: João da Silva"
    )

    cpf_digitado = st.text_input(
        "CPF",
        placeholder="000.000.000-00",
        max_chars=14
    )

    cpf_formatado = formatar_cpf(cpf_digitado)

    if cpf_digitado != cpf_formatado:
        st.caption(f"CPF formatado: {cpf_formatado}")

    email = st.text_input(
        "E-mail",
        placeholder="exemplo@email.com"
    )

    endereco = st.text_input(
        "Endereço de entrega",
        placeholder="Ex.: Rua das Flores, 123"
    )

    cep_digitado = st.text_input(
        "CEP",
        placeholder="00000-000",
        max_chars=9
    )

    cep_formatado = formatar_cep(cep_digitado)

    if cep_digitado != cep_formatado:
        st.caption(f"CEP formatado: {cep_formatado}")

    pagamento = st.selectbox(
        "Forma de pagamento",
        [
            "Selecione uma opção",
            "Pix",
            "Cartão de crédito",
            "Cartão de débito"
        ]
    )

    if st.button(
        "✅ Confirmar pedido",
        use_container_width=True
    ):

        erros = []

        if not nome_valido(nome):
            erros.append(
                "Digite seu nome completo, com nome e sobrenome."
            )

        if not cpf_valido(cpf_formatado):
            erros.append(
                "Digite um CPF válido."
            )

        if not email_valido(email):
            erros.append(
                "Digite um e-mail válido."
            )

        if len(endereco.strip()) < 10 or not re.search(r"\d", endereco):
            erros.append(
                "Digite um endereço completo, incluindo o número."
            )

        if len(limpar_numeros(cep_formatado)) != 8:
            erros.append(
                "Digite um CEP válido com 8 números."
            )

        if pagamento == "Selecione uma opção":
            erros.append(
                "Selecione uma forma de pagamento."
            )

        if erros:

            st.error(
                "⚠️ Corrija os dados abaixo:"
            )

            for erro in erros:
                st.warning(erro)

        else:

            st.success(
                "🎉 Pedido realizado com sucesso!"
            )

            st.info(
                f"Pagamento selecionado: {pagamento}"
            )

            st.session_state.carrinho = []
            st.session_state.checkout = False

# =========================================================
# RODAPÉ
# =========================================================

st.divider()

st.caption(
    "NOVA Store 🛍️ • © 2026"
)
