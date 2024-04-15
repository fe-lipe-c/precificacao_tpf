import pandas as pd
import streamlit as st
import pyield as pyd
import config as cfg
from scripts.precificacao import precificacao_ntnf, df_process
from scripts.plot_functions import (
    plot_lines,
    plot_lines_precos,
    plot_cash_flow,
    plot_diff,
)

st.markdown(
    """<style>.block-container{max-width: 86rem !important;}</style>""",
    unsafe_allow_html=True,
)


def run_interface():
    st.title("Precificação de Títulos de Renda Fixa")
    st.write("---")

    with open("texts/home_intro.md", "r") as file:
        intro = file.read()

    st.markdown(intro)

    st.markdown(
        """
        Vamos aplicar a equação $(3)$ para as NTN-F emitadas pelo TN entre 2015 e abril de 2024. A tabela abaixo contém os principais dados necessários para realizar a precificação.
                """
    )

    # df_auctions = pd.read_csv("data/brl_auctions.csv")
    # df_auctions = df_process(df_auctions)
    # df_auctions = df_auctions[
    #     [
    #         "auction_date",
    #         "maturity_date",
    #         "rate",
    #         "quantity_accepted",
    #         "accepted_amount",
    #         "bond_type",
    #     ]
    # ]
    # df_auctions.columns = [
    #     "Data do Leilão",
    #     "Data de Vencimento",
    #     "Taxa (%)",
    #     "Quantidade Aceita",
    #     "Valor Aceito (R$)",
    #     "Tipo de Título",
    # ]
    # df_auctions_ntnf = st.session_state.df_auctions[st.session_state.df_auctions["Tipo de Título"] == "NTN-F"]
    # columns_dataframe[1].dataframe(df_auctions_ntnf)

    # Rename each data in 'Date de Vencimento' from 'YYYY-MM-DD' to 'FYY', where 'YY' is the last two digits of the year
    # st.session_state.df_auctions_ntnf["Título"] = st.session_state.df_auctions_ntnf["Data de Vencimento"].replace(
    #     r"^(\d{2})(\d{2})-(\d{2})-(\d{2})$", r"F\2", regex=True
    # )

    # df_auctions_ntnf.reset_index(drop=True, inplace=True)

    columns_dataframe_taxa = st.columns([1, 5, 4, 1])

    columns_dataframe_taxa[1].dataframe(
        st.session_state.df_auctions_ntnf[
            [
                "Data do Leilão",
                "Data de Vencimento",
                "Taxa (%)",
                "Quantidade Aceita",
                "Valor Aceito (R$)",
                # "Tipo de Título",
                # "Título",
            ]
        ],
        height=330,
    )

    plot_taxa = plot_lines(
        st.session_state.df_auctions_ntnf[
            st.session_state.df_auctions_ntnf["Taxa (%)"] > 0
        ],
        "Taxa (%)",
        "Taxa Média de Emissão",
        "Taxa (%)",
        "Título",
    )
    columns_dataframe_taxa[2].altair_chart(plot_taxa, use_container_width=True)

    st.markdown(
        """
        Os dados públicos dos leilões não possuem os preços de emissão, apenas a taxa média pelas quais cada título foi vendido (lembrando que o leilão de pré-fixados é do tipo preço múltiplo, onde cada comprador leva a taxa que ofertou, considerando que a taxa aceita é menor ou igual à taxa de corte estabelecida pela STN). Para encontrar o preço basta dividir o valor aceito pela quantidade aceita. Com isso, após calcularmos o preço através da equação (3), podemos comparar com o preço de emissão e verificar se a conta está correta.

        Uma parte do cálculo que pode falhar, e resultar em um preço errado, é a definição do número de dias úteis. É preciso apurar a quantidade de dias úteis entre o vencimento do papel e o momento da sua precificação, e para isso é necessário ter o calendário de feriados. Um fato novo neste sentido foi a aprovação no final do ano passado da Lei nº 14.759/23, que acrescentou o dia 20 de novembro como feriado nacional (dia nacional de Zumbi), diminuindo, assim, o número de dias úteis no ano. No nosso cado, isso leva a um complicador, que é a necessidade de ter dois calendários para precificar títulos que vencem após 20-11-2024. Para realizar esse cálculo, utilizaremos a biblioteca `PYield` [4], que possui um calendário de feriados brasileiros atualizado.

        A tabela abaixo apresenta o preço médio para as NTN-F emitidas, além da quantidade de dias úteis até o vencimento:
                """
    )

    columns_dataframe_preco = st.columns([1, 5, 4, 1])

    columns_dataframe_preco[1].dataframe(
        st.session_state.df_auctions_ntnf[
            [
                "Data do Leilão",
                "Data de Vencimento",
                "Preço de Emissão (R$)",
                "Dias Úteis",
            ]
        ],
        height=330,
    )

    # plot_preco = plot_lines_precos(
    #     df_auctions_ntnf[df_auctions_ntnf["Taxa (%)"] > 0],
    #     "Preço de Emissão (R$)",
    #     "Preço Médio de Emissão",
    #     "Preço (R$)",
    # )

    # plot_preco = plot_preco_dias(df_auctions_ntnf)

    plot_preco = plot_lines(
        st.session_state.df_auctions_ntnf[
            st.session_state.df_auctions_ntnf["Taxa (%)"] > 0
        ],
        "Preço de Emissão (R$)",
        "Preço Médio de Emissão",
        "Preço (R$)",
        "Título",
    )
    columns_dataframe_preco[2].altair_chart(plot_preco, use_container_width=True)

    st.markdown(
        """
        Além disso, precisamos saber a data em que os cupons são pagos. No caso das NTN-F, os cupons são pagos nos dias 1 de janeiro e 1 de julho, com pagamento de cupom também no dia do vencimento (sempre 1 de janeiro). Vale lembrar que a liquidação da operação acontece apenas no dia útil seguinte à operaçao. Logo, a contagem de dias úteis até cada cupom e vencimento só começam no dia útil seguinte. Existe pelo menos um caso em que a liquidação de uma emissão aconteceu em dia de pagamento de cupom, que foi o leilão realizado no dia 30/06/2022, com liquidação no dia 01/07/2022. Neste caso, o primeiro pagamento de cupom dessa emissão aconteceu apenas no dia 01/01/2023.

        Abaixo apresentamos a tabela com o fluxo de caixa descontado para cada emissão, onde a coluna `Valor Presente (R$)` contém o valor presente de cada fluxo de caixa, considerando a taxa média de emissão.
                """
    )

    # st.session_state.df_auctions_ntnf, df_coupons = precificacao_ntnf(
    #     st.session_state.df_auctions_ntnf
    # )

    # st.session_state.df_auctions_ntnf["Diferença"] = (
    #     st.session_state.df_auctions_ntnf["Preço de Emissão (R$)"]
    #     - st.session_state.df_auctions_ntnf["Preço Calculado (R$)"]
    # )

    # st.session_state.df_auctions_ntnf[
    #     "Quantidade Aceita"
    # ] = st.session_state.df_auctions_ntnf["Quantidade Aceita"].astype(int)

    # st.session_state.df_auctions_ntnf["Taxa (%)"] = st.session_state.df_auctions_ntnf[
    #     "Taxa (%)"
    # ].astype(float)

    # df_auctions_ntnf = df_auctions_ntnf[
    #     (df_auctions_ntnf["Quantidade Aceita"] == 150000)
    #     & (df_auctions_ntnf["Taxa (%)"] >= 13)
    # ]

    # st.dataframe(df_auctions_ntnf)

    # st.session_state.df_auctions_ntnf.to_csv("data/df_auctions_ntnf.csv", index=False)
    # df_auctions_ntnf = pd.read_csv("data/df_auctions_ntnf.csv")
    df_coupons = pd.read_csv("data/df_coupons.csv")
    # df_coupons.reset_index(drop=True, inplace=True)
    # df_coupons.to_csv("data/df_coupons.csv", index=False)
    columns_selection = st.columns([1, 1, 5, 2])
    titulo_input = columns_selection[0].selectbox(
        "Selecione o título",
        st.session_state.df_auctions_ntnf["Título"].unique(),
        index=8,
    )
    list_dates = list(
        st.session_state.df_auctions_ntnf[
            st.session_state.df_auctions_ntnf["Título"] == titulo_input
        ]["Data do Leilão"].unique()
    )
    list_dates.sort(reverse=True)

    leilao_input = columns_selection[1].selectbox(
        "Selecione a emissão",
        list_dates,
        index=2,
    )

    df_selected = df_coupons[df_coupons["Título"] == titulo_input]

    df_selected["Data do Leilão"] = pd.to_datetime(df_selected["Data do Leilão"])
    df_selected["Data do Leilão"] = df_selected["Data do Leilão"] + pd.DateOffset(
        days=-1
    )
    df_selected = df_selected[df_selected["Data do Leilão"] == leilao_input]
    df_selected["Data do Leilão"] = pd.to_datetime(
        df_selected["Data do Leilão"]
    ).dt.date

    st.markdown(
        f"Preço calculado da {titulo_input}, emitida em {leilao_input}, é de **R${int(df_selected['Valor Presente (R$)'].sum())}**."
    )

    # df_selected["Data do Leilão"] = df_selected["Data do Leilão"].astype(str)
    columns_cash_flow = st.columns([1, 4, 0.4, 3, 1])
    columns_cash_flow[1].dataframe(
        df_selected[
            ["Data do Leilão", "Título", "Data de Pagamento", "Valor Presente (R$)"]
        ],
        height=330,
    )

    chart_cash_flow = plot_cash_flow(df_selected)

    columns_cash_flow[3].altair_chart(chart_cash_flow, use_container_width=True)

    st.markdown(
        """
        Por fim, somamos cada fluxo de pagamentos e comparamos com o preço de emissão, para verificar se a conta está correta. Abaixo está a tabela com a diferença entre o valor emitido e o calculado. Como pode ser observado, a diferença não é zero, seja por motivos de arrendondamento, seja pela questão de a taxa fornecida ser a média das taxas aceitas. O gráfico ao lado mostra a série crescente da diferença entre o preço emitido e o preço calculado. A maior diferença em módulo foi de R\$ 3,96, para a emissão da F27 em 19/05/2017.
                """
    )

    columns_diferenca = st.columns([0.3, 5, 0.3, 5, 0.3])

    columns_diferenca[1].dataframe(
        st.session_state.df_auctions_ntnf[
            [
                "Data do Leilão",
                "Título",
                "Preço de Emissão (R$)",
                "Preço Calculado (R$)",
                "Diferença",
            ]
        ],
        height=330,
    )

    df_diferenca = st.session_state.df_auctions_ntnf.sort_values(by="Diferença")
    df_diferenca.reset_index(inplace=True, drop=True)
    df_diferenca.reset_index(inplace=True)
    chart_diferenca = plot_diff(df_diferenca, "Título")
    columns_diferenca[3].altair_chart(chart_diferenca, use_container_width=True)

    df_teste_ntnf = st.session_state.df_auctions_ntnf[
        st.session_state.df_auctions_ntnf["Data do Leilão"] == "2024-03-28"
    ]

    st.markdown(
        """Abaixo estão as precificações para as NTN-Fs emitidas em 28/03/2024:"""
    )

    st.dataframe(
        df_teste_ntnf[
            [
                "Data do Leilão",
                "Título",
                "Taxa (%)",
                "Preço de Emissão (R$)",
                "Preço Calculado (R$)",
            ]
        ]
    )

    # st.markdown(
    #     """
    #     Abaixo está a tabela com todos os dados utilizados.
    #             """
    # )

    # st.dataframe(st.session_state.df_auctions_ntnf, height=330)

    with open("texts/home_ltn.md", "r") as file:
        intro_ltn = file.read()

    st.markdown(intro_ltn)

    st.markdown(
        """
        Vamos aplicar a equação $(4)$ para as LTN emitadas pelo TN entre 2015 e abril de 2024. A tabela abaixo contém os principais dados necessários para realizar a precificação.
                """
    )

    columns_dataframe_taxa_ltn = st.columns([1, 5, 4, 1])

    columns_dataframe_taxa_ltn[1].dataframe(
        st.session_state.df_auctions_ltn[
            [
                "Data do Leilão",
                "Data de Vencimento",
                "Taxa (%)",
                "Quantidade Aceita",
                "Valor Aceito (R$)",
                # "Tipo de Título",
                # "Título",
            ]
        ],
        height=330,
    )

    plot_taxa_ltn = plot_lines(
        st.session_state.df_auctions_ltn[
            st.session_state.df_auctions_ltn["Taxa (%)"] > 0
        ],
        "Taxa (%)",
        "Taxa Média de Emissão",
        "Taxa (%)",
        "Data de Vencimento",
    )
    columns_dataframe_taxa_ltn[2].altair_chart(plot_taxa_ltn, use_container_width=True)

    st.markdown(
        """A tabela abaixo apresenta o preço médio para as LTN emitidas, além da quantidade de dias úteis até o vencimento:"""
    )

    columns_dataframe_preco_ltn = st.columns([1, 5, 4, 1])

    columns_dataframe_preco_ltn[1].dataframe(
        st.session_state.df_auctions_ltn[
            [
                "Data do Leilão",
                "Data de Vencimento",
                "Preço de Emissão (R$)",
                "Dias Úteis",
            ]
        ],
        height=330,
    )

    plot_preco_ltn = plot_lines(
        st.session_state.df_auctions_ltn[
            st.session_state.df_auctions_ltn["Taxa (%)"] > 0
        ],
        "Preço de Emissão (R$)",
        "Preço Médio de Emissão",
        "Preço (R$)",
        "Data de Vencimento",
    )
    columns_dataframe_preco_ltn[2].altair_chart(
        plot_preco_ltn, use_container_width=True
    )

    df_teste = st.session_state.df_auctions_ltn[
        st.session_state.df_auctions_ltn["Data do Leilão"] == "2024-03-28"
    ]

    st.markdown(
        """
        Por fim, aplicamos a equação (4) utilizando a taxa e os dias úteis até o vencimento. Abaixo está a tabela com a diferença entre o valor emitido e o calculado. Da mesmo forma como foi feito para as NTN-F, a diferença não é zero, seja por motivos de arrendondamento, seja pela questão de a taxa fornecida ser a média das taxas aceitas. O gráfico ao lado mostra a série crescente da diferença entre o preço emitido e o preço calculado. A maior diferença em módulo foi de R\$ 33,02, para a emissão da out15 em 24/06/2015.
                """
    )

    def precificacao_ltn(taxa, dias_uteis):
        preco = 1000 / (1 + taxa / 100) ** (dias_uteis / 252)
        return preco

    st.session_state.df_auctions_ltn["Preço de Emissão (R$)"] = (
        st.session_state.df_auctions_ltn["Valor Aceito (R$)"]
        / st.session_state.df_auctions_ltn["Quantidade Aceita"]
    )

    st.session_state.df_auctions_ltn[
        "Preço Calculado (R$)"
    ] = st.session_state.df_auctions_ltn.apply(
        lambda x: precificacao_ltn(x["Taxa (%)"], x["Dias Úteis"]), axis=1
    )
    st.session_state.df_auctions_ltn["Diferença"] = (
        st.session_state.df_auctions_ltn["Preço de Emissão (R$)"]
        - st.session_state.df_auctions_ltn["Preço Calculado (R$)"]
    )

    columns_diferenca_ltn = st.columns([0.3, 5, 0.3, 5, 0.3])

    columns_diferenca_ltn[1].dataframe(
        st.session_state.df_auctions_ltn[
            [
                "Data do Leilão",
                "Data de Vencimento",
                "Preço de Emissão (R$)",
                "Preço Calculado (R$)",
                "Diferença",
            ]
        ],
        height=330,
    )

    df_diferenca_ltn = st.session_state.df_auctions_ltn.sort_values(by="Diferença")
    df_diferenca_ltn.reset_index(inplace=True, drop=True)
    df_diferenca_ltn.reset_index(inplace=True)
    chart_diferenca_ltn = plot_diff(df_diferenca_ltn, "Data de Vencimento")
    columns_diferenca_ltn[3].altair_chart(chart_diferenca_ltn, use_container_width=True)

    st.markdown(
        """Abaixo estão as precificações para as LTNs emitidas em 28/03/2024:"""
    )

    st.dataframe(
        df_teste[
            [
                "Data do Leilão",
                "Data de Vencimento",
                "Taxa (%)",
                "Preço de Emissão (R$)",
                "Preço Calculado (R$)",
            ]
        ]
    )

    # st.dataframe(st.session_state.df_auctions_ltn)

    st.write("---")

    st.markdown("## Referências")

    with open("texts/referencias.md", "r") as file:
        referencias = file.read()

    st.markdown(referencias)


def init_setup():
    pass

    if "df_auctions" not in st.session_state:
        st.session_state.df_auctions = pd.read_csv("data/brl_auctions.csv")
        st.session_state.df_auctions = df_process(st.session_state.df_auctions)

    if "df_auctions_ntnf" not in st.session_state:
        st.session_state.df_auctions_ntnf = pd.read_csv("data/df_auctions_ntnf.csv")
        # st.session_state.df_auctions_ntnf = st.session_state.df_auctions[
        #     st.session_state.df_auctions["Tipo de Título"] == "NTN-F"
        # ]
        # st.session_state.df_auctions_ntnf["Título"] = st.session_state.df_auctions_ntnf[
        #     "Data de Vencimento"
        # ].replace(r"^(\d{2})(\d{2})-(\d{2})-(\d{2})$", r"F\2", regex=True)
        # st.session_state.df_auctions_ntnf.reset_index(drop=True, inplace=True)

    if "df_auctions_ltn" not in st.session_state:
        st.session_state.df_auctions_ltn = st.session_state.df_auctions[
            st.session_state.df_auctions["Tipo de Título"] == "LTN"
        ]
        st.session_state.df_auctions_ltn.reset_index(drop=True, inplace=True)


def main():
    init_setup()
    run_interface()


if __name__ == "__main__":
    main()
