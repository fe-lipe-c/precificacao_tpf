import pandas as pd
import numpy as np
from datetime import datetime
import pyield as pyd


def df_process(df_auctions):
    df_auctions = df_auctions[
        [
            "auction_date",
            "maturity_date",
            "rate",
            "quantity_accepted",
            "accepted_amount",
            "bond_type",
        ]
    ]
    df_auctions.columns = [
        "Data do Leilão",
        "Data de Vencimento",
        "Taxa (%)",
        "Quantidade Aceita",
        "Valor Aceito (R$)",
        "Tipo de Título",
    ]

    df_auctions["Preço de Emissão (R$)"] = (
        df_auctions["Valor Aceito (R$)"] / df_auctions["Quantidade Aceita"]
    )

    df_auctions["Dias Úteis"] = df_auctions.apply(
        lambda x: pyd.count_bdays(
            start=x["Data do Leilão"], end=x["Data de Vencimento"]
        ),
        axis=1,
    )

    df_auctions["Taxa (%)"] = df_auctions["Taxa (%)"].astype(float)

    df_auctions["Data do Leilão"] = pd.to_datetime(df_auctions["Data do Leilão"])
    df_auctions["Data de Liquidação"] = df_auctions["Data do Leilão"] + pd.DateOffset(
        days=1
    )
    df_auctions["Data do Leilão"] = df_auctions["Data do Leilão"].dt.strftime(
        "%Y-%m-%d"
    )

    return df_auctions


def present_value(coupons, rate, days_until_payment):
    pv = 0
    pv_list = []
    for i in range(1, coupons + 1):
        coupom = ((1000 * (1.10) ** 0.5) - 1000) / (1 + rate) ** (
            days_until_payment[i - 1] / 252
        )
        pv_list.append(coupom)
        pv += coupom
    return pv, pv_list


def precificacao_ntnf(df_ntnf):
    df_ntnf["Data de Liquidação"] = pd.to_datetime(df_ntnf["Data de Liquidação"])
    df_ntnf["Data de Liquidação"] = df_ntnf["Data de Liquidação"].dt.strftime(
        "%Y-%m-%d"
    )

    prices = []

    df_cash_flow = pd.DataFrame()
    df_cash_flow_gross = pd.DataFrame()
    for index, row in df_ntnf.iterrows():
        df_coupons = pd.DataFrame()
        auction_date = datetime.strptime(row["Data de Liquidação"], "%Y-%m-%d")
        maturity_date = datetime.strptime(row["Data de Vencimento"], "%Y-%m-%d")
        rate = row["Taxa (%)"] / 100

        days_until_maturity = pyd.count_bdays(
            start=auction_date.strftime("%Y-%m-%d"),
            end=maturity_date.strftime("%Y-%m-%d"),
        )

        # Calculate the days until each coupon payment
        days_until_payment = []
        coupon_payment_date = []

        # coupon_payment_date.append(auction_date)
        coupon_date = (
            datetime(auction_date.year, 7, 1)
            if auction_date.month < 7
            else datetime(auction_date.year + 1, 1, 1)
        )

        while coupon_date < maturity_date:
            coupon_payment_date.append(coupon_date)
            days_until_next_coupon = pyd.count_bdays(
                start=auction_date.strftime("%Y-%m-%d"),
                end=coupon_date.strftime("%Y-%m-%d"),
            )

            days_until_payment.append(days_until_next_coupon)
            # auction_date = coupon_date  # Update auction_date to the last coupon_date for the next iteration
            coupon_date = datetime(
                coupon_date.year + (coupon_date.month // 7),
                1 if coupon_date.month == 7 else 7,
                1,
            )

        days_until_payment.append(days_until_maturity)
        coupon_payment_date.append(maturity_date)

        # Calculate the present value of the bond
        pv_coupons, coupons_list = present_value(
            len(days_until_payment), rate, days_until_payment
        )

        pv_face_value = 1000 / (1 + rate) ** (days_until_maturity / 252)
        bond_price = pv_coupons + pv_face_value
        prices.append(bond_price)

        coupons_list.append(pv_face_value)
        coupon_payment_date.append(maturity_date)
        days_until_payment.append(days_until_maturity)

        coupon_payment_date = [
            date.strftime("%Y-%m-%d") for date in coupon_payment_date
        ]
        df_coupons["Data de Pagamento"] = coupon_payment_date
        df_coupons["Dias Úteis"] = days_until_payment
        gross_coupons = [(1000 * (1.10) ** 0.5) - 1000] * len(coupons_list)
        gross_coupons[-1] = 1000
        df_coupons["Valor do Cupom (R$)"] = gross_coupons
        df_coupons["Valor Presente (R$)"] = coupons_list
        maturity_date = maturity_date.strftime("%Y-%m-%d")
        df_coupons["Data de Vencimento"] = maturity_date
        auction_date = auction_date.strftime("%Y-%m-%d")
        df_coupons["Data do Leilão"] = auction_date
        df_coupons["taxa"] = rate

        df_cash_flow = pd.concat([df_cash_flow, df_coupons])

    df_ntnf["Preço Calculado (R$)"] = prices
    df_ntnf["Diferença"] = (
        df_ntnf["Preço de Emissão (R$)"] - df_ntnf["Preço Calculado (R$)"]
    )

    df_cash_flow["Valor Presente (R$)"] = df_cash_flow["Valor Presente (R$)"].round(2)
    df_cash_flow["Título"] = df_cash_flow["Data de Vencimento"].replace(
        r"^(\d{2})(\d{2})-(\d{2})-(\d{2})$", r"F\2", regex=True
    )
    df_cash_flow = df_cash_flow[
        [
            "Título",
            "Data do Leilão",
            "Data de Pagamento",
            "Dias Úteis",
            "Valor do Cupom (R$)",
            "Valor Presente (R$)",
            "taxa",
            # "Data de Vencimento",
        ]
    ]

    return df_ntnf, df_cash_flow
