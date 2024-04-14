import altair as alt
import pandas as pd


def plot_lines(df, column, title, y_title):
    df["Data do Leilão"] = pd.to_datetime(df["Data do Leilão"])
    selection = alt.selection_multi(fields=["Título"], bind="legend")
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
            alt.Color("Título"),
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
