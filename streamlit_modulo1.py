
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Módulo 1 - Parâmetros Iniciais", layout="wide")

st.title("📊 Módulo 1: Parâmetros Iniciais")

# Upload da planilha
st.subheader("1. Carregar Planilha de Parâmetros")
arquivo = st.file_uploader("Selecione o arquivo Excel", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)
    st.success("Arquivo carregado com sucesso!")

    st.dataframe(df)

    st.subheader("2. Adicionar Novo Registro")

    with st.form("form_novo_registro"):
        unidade = st.text_input("Unidade de Negócio")
        responsavel = st.text_input("Responsável")
        ano = st.number_input("Ano", value=2025, step=1)
        mes = st.selectbox("Mês", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                                   "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
        enviado = st.form_submit_button("Adicionar")

        if enviado:
            novo_id = df["ID"].max() + 1 if not df.empty else 1
            novo_registro = {
                "ID": novo_id,
                "Unidade de Negócio": unidade,
                "Responsável": responsavel,
                "Ano": ano,
                "Mês": mes
            }
            df = df.append(novo_registro, ignore_index=True)
            st.success("Registro adicionado com sucesso!")

            st.subheader("3. Dados Atualizados")
            st.dataframe(df)

            # Exportar novo Excel
            def converter_para_excel(df):
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False, sheet_name="Parametros")
                return buffer.getvalue()

            excel_bytes = converter_para_excel(df)
            st.download_button(
                label="📥 Baixar planilha atualizada",
                data=excel_bytes,
                file_name="parametros_atualizados.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
