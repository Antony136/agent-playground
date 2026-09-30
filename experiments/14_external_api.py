from app.tools.api_tools import get_exchange_rate


def main():
    rate = get_exchange_rate("USD", "EUR")

    print("USD → EUR:")
    print(rate)


if __name__ == "__main__":
    main()