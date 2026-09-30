import requests


def get_exchange_rate(
    base_currency: str,
    target_currency: str,
) -> float:

    url = (
        "https://api.frankfurter.app/latest"
        f"?from={base_currency.upper()}"
        f"&to={target_currency.upper()}"
    )

    response = requests.get(url, timeout=10)

    response.raise_for_status()

    data = response.json()

    rates = data.get("rates", {})

    if target_currency.upper() not in rates:
        raise ValueError(
            f"Exchange rate not available for {target_currency}."
        )

    return rates[target_currency.upper()]