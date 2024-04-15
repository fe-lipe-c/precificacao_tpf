import altair as alt
import pandas as pd


def plot_lines(df, column, title, y_title, color_column):
    df["Data do Leilão"] = pd.to_datetime(df["Data do Leilão"])
    selection = alt.selection_multi(fields=[color_column], bind="legend")
    chart_rates = (
        alt.Chart(df, title=title)
        .mark_line()
        .encode(
            alt.X(
                "Data do Leilão",
                axis=alt.Axis(
                    title=None,
                    format="%b %Y",
                ),
            ),
            alt.Y(
                column,
                title=y_title,
                scale=alt.Scale(zero=False),
            ),
            alt.Color(color_column),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        )
        .add_params(selection)
        .properties(width=250, height=350)
    )

    return chart_rates


def plot_lines_precos(df, column, title, y_title):
    selection = alt.selection_multi(fields=["Título"], bind="legend")
    chart_prices = (
        alt.Chart(df, title=title)
        .mark_line()
        .encode(
            alt.X(
                "Dias Úteis",
                axis=alt.Axis(
                    title=None,
                ),
                sort="descending",
            ),
            alt.Y(
                column,
                title=y_title,
                scale=alt.Scale(zero=False),
            ),
            alt.Color("Título"),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        )
        .add_params(selection)
        .properties(width=250, height=350)
    )

    return chart_prices


def plot_cash_flow(df):
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            alt.X("Data de Pagamento:O", title=None),
            alt.Y("Valor Presente (R$):Q", title="VP dos pagamentos (R$)"),
            color=alt.condition(
                alt.datum["Valor Presente (R$)"] > 100,
                alt.value("orange"),
                alt.value("steelblue"),
            ),
        )
    )

    return chart


def plot_diff(df, color_column):
    chart_diff = (
        alt.Chart(
            df,
            title="Série crescente da diferença entre o preço emitido e o preço calculado",
        )
        .mark_square()
        .encode(
            alt.X(
                "index",
                axis=alt.Axis(
                    title=None,
                ),
                scale=alt.Scale(zero=False),
            ),
            alt.Y(
                "Diferença",
                title="Diferença (R$)",
                scale=alt.Scale(zero=False),
            ),
            alt.Color("Data do Leilão", legend=None),
            tooltip=[
                "Data do Leilão",
                color_column,
                alt.Tooltip("Diferença", format=".2f"),
            ],
        )
        .properties(width=350, height=350)
    )

    return chart_diff
