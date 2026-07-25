"""
=============================================================================
Projeto: Sistema Web de Gestão Escolar
Descrição: Aplicação web interativa desenvolvida em Streamlit para controle
           de alunos, professores, turmas e acompanhamento financeiro (faturamento
           e inadimplência) com banco de dados SQLite.
Utilizações/Sistemas: Python, Streamlit, Pandas, SQLite, Plotly.
=============================================================================
"""

import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

# 1. Configuração da página
st.set_page_config(
    page_title="Gestor Escolar",
    layout="wide"
)

DB_NAME = "sistema_escolar.db"


def inicializar_banco():
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_do_aluno TEXT NOT NULL,
            codigo_do_aluno TEXT,
            data_de_nascimento TEXT,
            valor_da_mensalidade REAL,
            data_pagamento TEXT,
            curso TEXT,
            data_de_iniciacao TEXT,
            previsao_termino TEXT,
            status TEXT,
            status_pagamento TEXT DEFAULT 'Pendente'
        )
    """
    )

    # Tratamento para bases existentes que precisem da coluna de status de pagamento
    try:
        cursor.execute("ALTER TABLE alunos ADD COLUMN status_pagamento TEXT DEFAULT 'Pendente'")
        conexao.commit()
    except:
        pass

    # Tabela de Professores
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS professores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_professor TEXT NOT NULL,
            data_de_nascimento TEXT,
            disciplina TEXT,
            data_de_iniciacao TEXT,
            regime TEXT,
            status TEXT
        )
    """
    )

    conexao.commit()
    conexao.close()


inicializar_banco()

def contar_total_alunos():
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM alunos")
    total = cursor.fetchone()[0]
    conexao.close()
    return total

def contar_alunos_ativos():
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM alunos WHERE status = 'Ativo'")
    total = cursor.fetchone()[0]
    conexao.close()
    return total

def calcular_faturamento_total():
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    cursor.execute("SELECT SUM(valor_da_mensalidade) FROM alunos WHERE status = 'Ativo'")
    resultado = cursor.fetchone()[0]
    conexao.close()
    return resultado if resultado is not None else 0.0

def gerar_proximo_codigo():
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    cursor.execute("SELECT codigo_do_aluno FROM alunos WHERE codigo_do_aluno LIKE '31010%'")
    codigos = cursor.fetchall()
    conexao.close()

    if not codigos:
        return "3101011"

    maior_num = 3101010
    for (cod,) in codigos:
        try:
            num = int(cod)
            if num > maior_num:
                maior_num = num
        except ValueError:
            continue

    return str(maior_num + 1)


# 3. Barra Lateral e Navegação
st.markdown(
    """
    <style>
        /* Fundo geral da aplicação em branco e cor padrão de texto */
        .stApp {
            background-color: #ffffff !important;
            color: #1F2937 !important;
        }

        /* Todos os textos, títulos e parágrafos em #1F2937 */
        h1, h2, h3, h4, h5, h6, p, span, label, div {
            color: #1F2937;
        }

        /* Força os títulos das páginas especificamente */
        .stApp h1 {
            color: #1F2937 !important;
        }

        /* Barra lateral em cinza mais claro */
        [data-testid="stSidebar"] {
            background-color: #f3f4f6 !important;
        }

        /* Textos dentro da barra lateral em #1F2937 */
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] span {
            color: #1F2937 !important;
        }

        [data-testid="stSidebar"] div.row-widget.stRadio > div {
            gap: 0px;
        }

        /* Botões da navegação lateral e botões gerais em amarelo mostarda com texto #1F2937 */
        [data-testid="stSidebar"] div.row-widget.stRadio label,
        div.stButton > button:first-child {
            background-color: #eab308 !important;
            color: #1F2937 !important;
            padding: 12px 16px;
            border-radius: 6px;
            margin-bottom: 6px;
            font-weight: 600;
            display: flex;
            align-items: center;
            width: 100%;
            cursor: pointer;
            border: none !important;
        }

        [data-testid="stSidebar"] input[type="radio"],
        [data-testid="stSidebar"] div[data-baseweb="radio"] {
            display: none !important;
        }

        [data-testid="stSidebar"] div.row-widget.stRadio label:hover,
        div.stButton > button:first-child:hover {
            background-color: #ca8a04 !important;
            color: #1F2937 !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# 4. Barra Lateral com Navegação por Botões
with st.sidebar:
    st.markdown("<h2 style='color: #1f2937; font-size: 20px; padding-left: 10px;'>Gestão Escolar</h2>",
                unsafe_allow_html=True)
    st.markdown("---")

    if "pagina_selecionada" not in st.session_state:
        st.session_state.pagina_selecionada = "Visão Geral"

    opcoes = [
        "Visão Geral",
        "Alunos Ativos",
        "Professores",
        "Faturamento",
        "Configurar Sistema"
    ]

    for op in opcoes:
        if st.button(op, key=f"btn_{op}", use_container_width=True):
            st.session_state.pagina_selecionada = op
            st.rerun()

    st.markdown("---")
    st.markdown("<p style='color: #9ca3af; font-size: 14px; padding-left: 10px;'>Faturamento Total (Ativos)</p>",
                unsafe_allow_html=True)
    faturamento_total_sidebar = calcular_faturamento_total()
    st.markdown(
        f"<p style='color: #ffffff; font-size: 18px; font-weight: bold; padding-left: 10px;'>R$ {faturamento_total_sidebar:,.2f}</p>",
        unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='color: #9ca3af; font-size: 14px; padding-left: 10px;'>Ver Sistema Online</p>",
                unsafe_allow_html=True)

pagina_selecionada = st.session_state.pagina_selecionada

# 5. Página principal e Visão Geral com gráficos
if pagina_selecionada == "Visão Geral":
    st.title("Visão Geral")
    st.markdown("Bem-vinda ao painel principal de controle escolar.")

    total_alunos = contar_total_alunos()
    faturamento_total = calcular_faturamento_total()
    total_alunos_ativos = contar_alunos_ativos()

    # Consulta para cruzamento de dados de status financeiro
    conexao = sqlite3.connect(DB_NAME)
    df_visao = pd.read_sql("SELECT status, status_pagamento, valor_da_mensalidade FROM alunos", conexao)
    conexao.close()

    df_visao['status_pagamento'] = df_visao['status_pagamento'].fillna('Pendente')
    df_ativos_visao = df_visao[df_visao['status'] == 'Ativo']

    faturamento_atual = df_ativos_visao[df_ativos_visao['status_pagamento'] == 'Pago/Em dia']['valor_da_mensalidade'].sum()

    # Faturamento atual e contagem de inadimplência/pagamentos
    pagamentos_em_dia = len(df_ativos_visao[df_ativos_visao['status_pagamento'] == 'Pago/Em dia'])
    pendentes_qtd = len(df_ativos_visao[df_ativos_visao['status_pagamento'] == 'Pendente'])
    inadimplentes = len(df_ativos_visao[df_ativos_visao['status_pagamento'] == 'Inadimplente'])

    # Exibição de Indicadores (KPI Cards)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric(label="Total de Alunos", value=total_alunos)
    with col2:
        st.metric(label="Faturamento Previsto", value=f"R$ {faturamento_total:,.2f}")
    with col3:
        st.metric(label="Faturamento Atual", value=f"R$ {faturamento_atual:,.2f}")
    with col4:
        st.metric(label="Alunos Ativos", value=total_alunos_ativos)
    with col5:
        st.metric(label="Pagamentos em dia", value=pagamentos_em_dia)
    with col6:
        st.metric(label="Inadimplentes", value=inadimplentes)

    st.markdown("---")

    # Gráficos Analíticos com Plotly
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.subheader("Distribuição de Alunos")
        dados_grafico_alunos = pd.DataFrame({
            "Categoria": ["Alunos Ativos", "Alunos Inativos"],
            "Quantidade": [total_alunos_ativos, total_alunos - total_alunos_ativos],
        })
        fig1 = px.pie(
            dados_grafico_alunos,
            names="Categoria",
            values="Quantidade",
            hole=0.4,
            color_discrete_sequence=["#2563eb", "#93c5fd"]
        )
        fig1.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=350)
        st.plotly_chart(fig1, use_container_width=True)

    with col_graf2:
        st.subheader("Status de Pagamento (Ativos)")
        dados_grafico_pagamento = pd.DataFrame({
            "Status": ["Pago/Em dia", "Pendente", "Inadimplente"],
            "Quantidade": [pagamentos_em_dia, pendentes_qtd, inadimplentes],
        })
        fig2 = px.pie(
            dados_grafico_pagamento,
            names="Status",
            values="Quantidade",
            hole=0.4,
            color_discrete_sequence=["#eab308", "#16a34a", "#dc2626"]
        )
        fig2.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=350)
        st.plotly_chart(fig2, use_container_width=True)

elif pagina_selecionada == "Alunos Ativos":
    st.title("Alunos Ativos")
    st.markdown("Gerencie o cadastro, visualize, filtre e edite as informações dos estudantes.")

    aba_visualizar, aba_cadastrar, aba_editar = st.tabs(["📋 Visualizar Alunos", "➕ Cadastrar Aluno", "✏️ Editar Aluno"])

    with aba_visualizar:
        st.subheader("Lista de Alunos Registrados")

        # Filtros e Pesquisa na Tabela
        col_filtro1, col_filtro2 = st.columns([2, 1])
        with col_filtro1:
            pesquisa_nome = st.text_input("🔍 Pesquisar aluno por nome", placeholder="Digite o nome...")
        with col_filtro2:
            filtro_status = st.selectbox("Filtrar por Status", ["Todos", "Ativo", "Pendente", "Inativo"])

        conexao = sqlite3.connect(DB_NAME)

        # Montando a query com base nos filtros
        query = "SELECT codigo_do_aluno, nome_do_aluno, data_de_nascimento, valor_da_mensalidade, data_pagamento, curso, data_de_iniciacao, previsao_termino, status FROM alunos WHERE 1=1"
        parametros = []

        if pesquisa_nome:
            query += " AND nome_do_aluno LIKE ?"
            parametros.append(f"%{pesquisa_nome}%")

        if filtro_status != "Todos":
            query += " AND status = ?"
            parametros.append(filtro_status)

        query += " ORDER BY nome_do_aluno ASC"

        df = pd.read_sql(query, conexao, params=parametros)
        conexao.close()

        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"Exibindo {len(df)} registro(s) encontrado(s).")
        else:
            st.info("Nenhum aluno encontrado com os filtros selecionados.")

    with aba_cadastrar:
        st.subheader("Adicionar Novo Aluno")
        proximo_codigo = gerar_proximo_codigo()

        with st.form("form_add_aluno"):
            st.markdown(f"**Código gerado automaticamente:** `{proximo_codigo}`")

            nome_do_aluno = st.text_input("Nome do Aluno")
            data_de_nascimento = st.text_input("Data de Nascimento (Ex: DD/MM/AAAA)")
            valor_da_mensalidade = st.number_input("Valor da Mensalidade (R$)", value=0.0)
            data_pagamento = st.text_input("Data de Pagamento (Ex: Dia do vencimento)")
            curso = st.text_input("Curso")
            data_de_iniciacao = st.text_input("Data de Iniciação (Ex: DD/MM/AAAA)")
            previsao_termino = st.text_input("Previsão de Término (Ex: DD/MM/AAAA)")
            status = st.selectbox("Status", ["Ativo", "Pendente", "Inativo"])

            salvar = st.form_submit_button("Salvar no Banco de Dados")

            if salvar:
                if nome_do_aluno:
                    conexao = sqlite3.connect(DB_NAME)
                    cursor = conexao.cursor()
                    cursor.execute(
                        """
                        INSERT INTO alunos (
                            nome_do_aluno, codigo_do_aluno, data_de_nascimento, 
                            valor_da_mensalidade, data_pagamento, curso, 
                            data_de_iniciacao, previsao_termino, status
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            nome_do_aluno, proximo_codigo, data_de_nascimento,
                            valor_da_mensalidade, data_pagamento, curso,
                            data_de_iniciacao, previsao_termino, status
                        )
                    )
                    conexao.commit()
                    conexao.close()
                    st.success(f"Aluno cadastrado com sucesso! Código: {proximo_codigo}")
                    st.rerun()
                else:
                    st.warning("O campo Nome do Aluno é obrigatório.")

    with aba_editar:
        st.subheader("Editar Dados do Aluno")
        conexao = sqlite3.connect(DB_NAME)
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome_do_aluno, codigo_do_aluno FROM alunos ORDER BY nome_do_aluno ASC")
        alunos_cadastrados = cursor.fetchall()
        conexao.close()

        if alunos_cadastrados:
            opcoes_alunos = {f"{nome} (Código: {cod})": id_aluno for id_aluno, nome, cod in alunos_cadastrados}
            aluno_selecionado = st.selectbox("Selecione o Aluno para Editar", list(opcoes_alunos.keys()))
            id_selecionado = opcoes_alunos[aluno_selecionado]

            conexao = sqlite3.connect(DB_NAME)
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT nome_do_aluno, codigo_do_aluno, data_de_nascimento, valor_da_mensalidade, data_pagamento, curso, data_de_iniciacao, previsao_termino, status FROM alunos WHERE id = ?",
                (id_selecionado,))
            dados_atuais = cursor.fetchone()
            conexao.close()

            if dados_atuais:
                with st.form("form_edit_aluno"):
                    e_nome = st.text_input("Nome do Aluno", value=dados_atuais[0])
                    e_codigo = st.text_input("Código do Aluno", value=dados_atuais[1] if dados_atuais[1] else "")
                    e_nascimento = st.text_input("Data de Nascimento", value=dados_atuais[2] if dados_atuais[2] else "")
                    e_mensalidade = st.number_input("Valor da Mensalidade (R$)",
                                                    value=float(dados_atuais[3]) if dados_atuais[3] else 0.0)
                    e_pagamento = st.text_input("Data de Pagamento", value=dados_atuais[4] if dados_atuais[4] else "")
                    e_curso = st.text_input("Curso", value=dados_atuais[5] if dados_atuais[5] else "")
                    e_iniciacao = st.text_input("Data de Iniciação", value=dados_atuais[6] if dados_atuais[6] else "")
                    e_termino = st.text_input("Previsão de Término", value=dados_atuais[7] if dados_atuais[7] else "")

                    status_opcoes = ["Ativo", "Pendente", "Inativo"]
                    status_atual = dados_atuais[8] if dados_atuais[8] in status_opcoes else "Ativo"
                    e_status = st.selectbox("Status", status_opcoes, index=status_opcoes.index(status_atual))

                    atualizar = st.form_submit_button("Salvar Alterações")

                    if atualizar:
                        conexao = sqlite3.connect(DB_NAME)
                        cursor = conexao.cursor()
                        cursor.execute(
                            """
                            UPDATE alunos SET 
                                nome_do_aluno = ?, codigo_do_aluno = ?, data_de_nascimento = ?, 
                                valor_da_mensalidade = ?, data_pagamento = ?, curso = ?, 
                                data_de_iniciacao = ?, previsao_termino = ?, status = ?
                            WHERE id = ?
                            """,
                            (
                                e_nome, e_codigo, e_nascimento, e_mensalidade,
                                e_pagamento, e_curso, e_iniciacao, e_termino, e_status, id_selecionado
                            )
                        )
                        conexao.commit()
                        conexao.close()
                        st.success("Dados atualizados com sucesso!")
                        st.rerun()
        else:
            st.info("Nenhum aluno cadastrado para editar.")

elif pagina_selecionada == "Professores":
    st.title("Base de Professores")
    st.markdown("Gerenciamento de professores, contatos e turmas vinculadas.")

    aba_vis_prof, aba_cad_prof, aba_edt_prof = st.tabs(
        ["📋 Visualizar Professores", "➕ Cadastrar Professor", "✏️ Editar Professor"])

    with aba_vis_prof:
        st.subheader("Lista de Professores Registrados")
        conexao = sqlite3.connect(DB_NAME)
        df_prof = pd.read_sql(
            "SELECT nome_professor, data_de_nascimento, disciplina, data_de_iniciacao, regime, status FROM professores ORDER BY nome_professor ASC",
            conexao
        )
        conexao.close()

        if not df_prof.empty:
            st.dataframe(df_prof, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum professor cadastrado ainda. Utilize a aba ao lado para adicionar.")

    with aba_cad_prof:
        st.subheader("Adicionar Novo Professor")
        with st.form("form_add_professor"):
            nome_do_professor = st.text_input("Nome do Professor")
            data_de_nascimento = st.text_input("Data de Nascimento (Ex: DD/MM/AAAA)")
            disciplina = st.text_input("Disciplina")
            data_de_iniciacao = st.text_input("Data de Iniciação (Ex: DD/MM/AAAA)")
            regime = st.selectbox("Regime", ["CLT", "Freelancer", "Temporário"])
            status = st.selectbox("Status", ["Ativo", "Desativado", "Afastado(a)", "Férias"])

            salvar_prof = st.form_submit_button("Salvar no Banco de Dados")

            if salvar_prof:
                if nome_do_professor:
                    conexao = sqlite3.connect(DB_NAME)
                    cursor = conexao.cursor()
                    cursor.execute(
                        """
                        INSERT INTO professores (
                            nome_professor, data_de_nascimento, 
                            disciplina, data_de_iniciacao, regime, status
                        ) VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            nome_do_professor, data_de_nascimento,
                            disciplina, data_de_iniciacao, regime, status
                        )
                    )
                    conexao.commit()
                    conexao.close()
                    st.success("Professor cadastrado com sucesso!")
                    st.rerun()
                else:
                    st.warning("O campo Nome do Professor é obrigatório.")

    with aba_edt_prof:
        st.subheader("Editar Dados do Professor")
        conexao = sqlite3.connect(DB_NAME)
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome_professor FROM professores ORDER BY nome_professor ASC")
        professores_cadastrados = cursor.fetchall()
        conexao.close()

        if professores_cadastrados:
            opcoes_profs = {nome: id_prof for id_prof, nome in professores_cadastrados}
            prof_selecionado = st.selectbox("Selecione o Professor para Editar", list(opcoes_profs.keys()))
            id_prof_selecionado = opcoes_profs[prof_selecionado]

            conexao = sqlite3.connect(DB_NAME)
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT nome_professor, data_de_nascimento, disciplina, data_de_iniciacao, regime, status FROM professores WHERE id = ?",
                (id_prof_selecionado,))
            dados_prof_atuais = cursor.fetchone()
            conexao.close()

            if dados_prof_atuais:
                with st.form("form_edit_professor"):
                    ep_nome = st.text_input("Nome do Professor", value=dados_prof_atuais[0])
                    ep_nascimento = st.text_input("Data de Nascimento",
                                                  value=dados_prof_atuais[1] if dados_prof_atuais[1] else "")
                    ep_disciplina = st.text_input("Disciplina",
                                                  value=dados_prof_atuais[2] if dados_prof_atuais[2] else "")
                    ep_iniciacao = st.text_input("Data de Iniciação",
                                                 value=dados_prof_atuais[3] if dados_prof_atuais[3] else "")

                    regimes_opcoes = ["CLT", "Freelancer", "Temporário"]
                    regime_atual = dados_prof_atuais[4] if dados_prof_atuais[4] in regimes_opcoes else "CLT"
                    ep_regime = st.selectbox("Regime", regimes_opcoes, index=regimes_opcoes.index(regime_atual))

                    status_p_opcoes = ["Ativo", "Desativado", "Afastado(a)", "Férias"]
                    status_p_atual = dados_prof_atuais[5] if dados_prof_atuais[5] in status_p_opcoes else "Ativo"
                    ep_status = st.selectbox("Status", status_p_opcoes, index=status_p_opcoes.index(status_p_atual))

                    atualizar_prof = st.form_submit_button("Salvar Alterações")

                    if atualizar_prof:
                        conexao = sqlite3.connect(DB_NAME)
                        cursor = conexao.cursor()
                        cursor.execute(
                            """
                            UPDATE professores SET 
                                nome_professor = ?, data_de_nascimento = ?, 
                                disciplina = ?, data_de_iniciacao = ?, regime = ?, status = ?
                            WHERE id = ?
                            """,
                            (
                                ep_nome, ep_nascimento, ep_disciplina,
                                ep_iniciacao, ep_regime, ep_status, id_prof_selecionado
                            )
                        )
                        conexao.commit()
                        conexao.close()
                        st.success("Professor cadastrado com sucesso!")
                        st.rerun()
        else:
            st.info("Nenhum professor cadastrado para editar.")

elif pagina_selecionada == "Faturamento":
    st.title("Gestão de Faturamento")
    st.markdown("Acompanhe os recebimentos, mensalidades pendentes e saúde financeira do sistema escolar.")

    st.markdown("---")

    conexao = sqlite3.connect(DB_NAME)
    df_faturamento = pd.read_sql(
        "SELECT id, nome_do_aluno, valor_da_mensalidade, data_pagamento, status, status_pagamento FROM alunos ORDER BY nome_do_aluno ASC",
        conexao)
    conexao.close()

    df_faturamento['status_pagamento'] = df_faturamento['status_pagamento'].fillna('Pendente')

    # Filtra apenas os alunos com status de matrícula 'Ativo'
    df_ativos = df_faturamento[df_faturamento['status'] == 'Ativo'].copy()

    # Contagens
    total_em_dia = len(df_ativos[df_ativos['status_pagamento'] == 'Pago/Em dia'])
    total_pendentes = len(df_ativos[df_ativos['status_pagamento'] == 'Pendente'])
    total_inadimplentes = len(df_ativos[df_ativos['status_pagamento'] == 'Inadimplente'])

    # Cálculos financeiros baseados nos alunos ativos
    faturamento_previsto = df_ativos['valor_da_mensalidade'].sum()
    faturamento_atual = df_ativos[df_ativos['status_pagamento'] == 'Pago/Em dia']['valor_da_mensalidade'].sum()
    valor_inadimplencia = df_ativos[df_ativos['status_pagamento'] == 'Inadimplente']['valor_da_mensalidade'].sum()

    # Exibindo as métricas em colunas
    col_m1, col_m2, col_m3, col_m4, col_m5, col_m6 = st.columns(6)
    with col_m1:
        st.metric(label="Faturamento Previsto", value=f"R$ {faturamento_previsto:,.2f}")
    with col_m2:
        st.metric(label="Faturamento Atual", value=f"R$ {faturamento_atual:,.2f}")
    with col_m3:
        st.metric(label="Valor Inadimplência", value=f"R$ {valor_inadimplencia:,.2f}")
    with col_m4:
        st.metric(label="Pago / Em dia", value=total_em_dia)
    with col_m5:
        st.metric(label="Pendentes", value=total_pendentes)
    with col_m6:
        st.metric(label="Inadimplentes", value=total_inadimplentes)

    st.markdown("---")

    st.subheader("📋 Atualizar Status de Pagamento (Alunos Ativos)")

    if not df_ativos.empty:
        for index, linha in df_ativos.iterrows():
            with st.container(border=True):
                col_info1, col_info2, col_info3, col_acao = st.columns([2, 1, 1, 2])

                with col_info1:
                    st.markdown(f"**{linha['nome_do_aluno']}**")
                    st.caption(f"Vencimento: Dia {linha['data_pagamento']}")
                with col_info2:
                    val = linha['valor_da_mensalidade'] if pd.notnull(linha['valor_da_mensalidade']) else 0.0
                    st.markdown(f"R$ {val:.2f}")
                with col_info3:
                    st.markdown(f"*{linha['status_pagamento']}*")
                with col_acao:
                    opcoes_status = ["Pago/Em dia", "Pendente", "Inadimplente"]
                    status_atual_idx = opcoes_status.index(linha['status_pagamento']) if linha[
                                                                                             'status_pagamento'] in opcoes_status else 1

                    novo_status = st.selectbox(
                        "Alterar",
                        opcoes_status,
                        index=status_atual_idx,
                        key=f"status_pag_{linha['id']}",
                        label_visibility="collapsed"
                    )

                    if st.button("Salvar", key=f"btn_{linha['id']}"):
                        conexao = sqlite3.connect(DB_NAME)
                        cursor = conexao.cursor()
                        cursor.execute("UPDATE alunos SET status_pagamento = ? WHERE id = ?",
                                       (novo_status, linha['id']))
                        conexao.commit()
                        conexao.close()
                        st.success("Atualizado com sucesso!")
                        st.rerun()
    else:
        st.info("Nenhum aluno ativo encontrado para faturamento.")

elif pagina_selecionada == "Configurar Sistema":
    st.title("⚙️ Configurações do Sistema")
    st.markdown("Personalize a aparência geral e os detalhes visuais do seu painel escolar.")

    st.markdown("---")

    # Seção de Estilização e Personalização Global
    st.subheader("🎨 Estilização e Aparência do Painel")
    st.markdown("Ajuste o estilo visual para adaptar o sistema ao seu gosto.")

    raio_borda = st.slider("Arredondamento dos Componentes (px)", min_value=0, max_value=20, value=8)
    fonte_estilo = st.selectbox(
        "Estilo de Tipografia",
        ["Moderna (Sans-Serif)", "Clássica (Serif)", "Técnica (Monospace)"]
    )

    # Aplicando a estilização dinâmica via CSS injetado
    st.markdown(
        f"""
        <style>
            /* Ajuste dinâmico do arredondamento baseado nas escolhas */
            .stMetric, div[data-testid="stHorizontalBlock"] > div {{
                border-radius: {raio_borda}px !important;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Botão para salvar simulação de preferências visuais
    if st.button("Salvar Preferências Visuais"):
        st.success("Configurações de estilo aplicadas com sucesso ao painel!")