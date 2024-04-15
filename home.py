import pandas as pd
import streamlit as st
import pyield as pyd
import config as cfg
from scripts.precificacao import precificacao_ntnf, df_process
from scripts.plot_functions import plot_lines, plot_lines_precos

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

    df_auctions = pd.read_csv("data/brl_auctions.csv")
    df_auctions = df_process(df_auctions)
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
    df_auctions_ntnf = df_auctions[df_auctions["Tipo de Título"] == "NTN-F"]
    # columns_dataframe[1].dataframe(df_auctions_ntnf)

    # Rename each data in 'Date de Vencimento' from 'YYYY-MM-DD' to 'FYY', where 'YY' is the last two digits of the year
    df_auctions_ntnf["Título"] = df_auctions_ntnf["Data de Vencimento"].replace(
        r"^(\d{2})(\d{2})-(\d{2})-(\d{2})$", r"F\2", regex=True
    )

    df_auctions_ntnf.reset_index(drop=True, inplace=True)

    columns_dataframe_taxa = st.columns([1, 5, 4, 1])

    columns_dataframe_taxa[1].dataframe(
        df_auctions_ntnf[
            [
                "Data do Leilão",
                "Data de Vencimento",
                "Taxa (%)",
                "Quantidade Aceita",
                "Valor Aceito (R$)",
                # "Tipo de Título",
                # "Título",
            ]
        ]
    )

    plot_taxa = plot_lines(
        df_auctions_ntnf[df_auctions_ntnf["Taxa (%)"] > 0],
        "Taxa (%)",
        "Taxa Média de Emissão",
        "Taxa (%)",
    )
    columns_dataframe_taxa[2].altair_chart(plot_taxa, use_container_width=True)

    st.markdown(
        """
        Os dados públicos dos leilões não possuem os preços de emissão, apenas a taxa média pelas quais cada título foi vendido (lembrando que o leilão de pré-fixados é do tipo preço múltiplo, onde cada comprador leva a taxa que ofertou, considerando que a taxa aceita é menor ou igual à taxa de corte estabelecida pela STN). Para encontrar o preço basta dividir o valor aceito pela quantidade aceita. Com isso, após calcularmos o preço através da equação, podemos comparar com o preço de emissão e verificar se a conta está correta.

        Uma parte do cálculo que pode falhar, e resultar em um preço errado, é a definição do número de dias úteis. É preciso apurar a quantidade de dias úteis entre o vencimento do papel e o momento da sua precificação, e para isso é necessário ter o calendário de feriados. Um fato novo neste sentido foi a aprovação no final do ano passado da Lei nº 14.759/23, que acrescentou o dia 20 de novembro como feriado nacional (dia nacional de Zumbi), diminuindo, assim, o número de dias úteis no ano. No nosso cado, isso leva a um complicador, que é a necessidade de ter dois calendários para precificar títulos que vencem após 20-11-2024. Para realizar esse cálculo, utilizaremos a biblioteca `PYield` [4], que possui um calendário de feriados brasileiros atualizado.

        A tabela abaixo apresenta o preço médio para as NTN-F emitidas, além da quantidade de dias úteis até o vencimento:
                """
    )

    columns_dataframe_preco = st.columns([1, 5, 4, 1])

    columns_dataframe_preco[1].dataframe(
        df_auctions_ntnf[
            [
                "Data do Leilão",
                "Data de Vencimento",
                "Preço de Emissão (R$)",
                "Dias Úteis",
            ]
        ]
    )

    # plot_preco = plot_lines_precos(
    #     df_auctions_ntnf[df_auctions_ntnf["Taxa (%)"] > 0],
    #     "Preço de Emissão (R$)",
    #     "Preço Médio de Emissão",
    #     "Preço (R$)",
    # )

    # plot_preco = plot_preco_dias(df_auctions_ntnf)

    plot_preco = plot_lines(
        df_auctions_ntnf[df_auctions_ntnf["Taxa (%)"] > 0],
        "Preço de Emissão (R$)",
        "Preço Médio de Emissão",
        "Preço (R$)",
    )
    columns_dataframe_preco[2].altair_chart(plot_preco, use_container_width=True)

    st.markdown(
        """
        Além disso, precisamos saber a data em que os cupons são pagos. No caso das NTN-F, os cupons são pagos nos dias 1 de janeiro e 1 de julho, com pagamento de cupom também no dia do vencimento (sempre 1 de janeiro). Vale lembrar que a liquidação da operação acontece apenas no dia útil seguinte à operaçao. Logo, a contagem de dias úteis até cada cupom e vencimento só começam no dia útil seguinte. Existe pelo menos um caso em que a liquidação de uma emissão aconteceu em dia de pagamento de cupom, que foi o leilão realizado no dia 30/06/2022, com liquidação no dia 01/07/2022. Neste caso, o primeiro pagamento de cupom dessa emissão aconteceu apenas no dia 01/01/2023.

        Abaixo apresentamos a tabela com o fluxo de caixa descontado de um título para cada emissão:
                """
    )

    df_auctions_ntnf, df_coupons = precificacao_ntnf(df_auctions_ntnf)

    df_auctions_ntnf["Diferença"] = (
        df_auctions_ntnf["Preço de Emissão (R$)"]
        - df_auctions_ntnf["Preço Calculado (R$)"]
    )

    df_auctions_ntnf["Quantidade Aceita"] = df_auctions_ntnf[
        "Quantidade Aceita"
    ].astype(int)

    df_auctions_ntnf["Taxa (%)"] = df_auctions_ntnf["Taxa (%)"].astype(float)

    # df_auctions_ntnf = df_auctions_ntnf[
    #     (df_auctions_ntnf["Quantidade Aceita"] == 150000)
    #     & (df_auctions_ntnf["Taxa (%)"] >= 13)
    # ]

    # st.dataframe(df_auctions_ntnf)

    st.dataframe(df_coupons)

    with open("texts/home_ltn.md", "r") as file:
        intro_ltn = file.read()

    st.markdown(intro_ltn)

    st.markdown(
        """
        Vamos aplicar a equação $(4)$ para as LTN emitadas pelo TN entre 2015 e abril de 2024. A tabela abaixo contém os principais dados necessários para realizar a precificação.
                """
    )

    def precificacao_ltn(taxa, dias_uteis):
        preco = 1000 / (1 + taxa / 100) ** (dias_uteis / 252)
        return preco

    df_auctions_ltn = df_auctions[df_auctions["Tipo de Título"] == "NTN-F"]

    df_auctions_ltn["Preço de Emissão (R$)"] = (
        df_auctions_ltn["Valor Aceito (R$)"] / df_auctions_ltn["Quantidade Aceita"]
    )

    df_auctions_ltn["Preço Calculado (R$)"] = df_auctions_ltn.apply(
        lambda x: precificacao_ltn(x["Taxa (%)"], x["Dias Úteis"]), axis=1
    )
    df_auctions_ltn["Diferença (R$)"] = (
        df_auctions_ltn["Preço de Emissão (R$)"]
        - df_auctions_ltn["Preço Calculado (R$)"]
    )

    st.markdown(
        """
        Na tabela abaixo apresentamos o cálculo do preço de cada papel emitido, além da diferença entre o preço de emissão e o preço calculado. Como pode ser observado, houve diferença positiva em todos os papéis, sendo a diferença máxima de R\$ 33,02 no leilão da ```LTN out/15``` em 25/06/2015 (preço calculado ficou -3% menor). Essa diferença acontecerá, pois, enquanto o montante total aceito é o valor de fato vendido, a taxa reportada é a média das taxas aceitas, o que pode fazer com que o preço de emissão seja maior que o preço calculado.
                """
    )

    st.dataframe(df_auctions_ltn)

    st.write("---")

    with open("texts/referencias.md", "r") as file:
        referencias = file.read()

    st.markdown(referencias)


def main():
    run_interface()


if __name__ == "__main__":
    main()
