import csv
from pathlib import Path

# Sample prices for demonstration only; these are not live market prices.
STOCK_PRICES = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "MSFT": 420.00,
    "GOOGL": 160.00,
    "AMZN": 190.00,
}

OUTPUT_FILE = Path("portfolio.csv")


def show_available_stocks():
    print("\nAvailable sample stocks:")
    for symbol, price in STOCK_PRICES.items():
        print(f"  {symbol}: ${price:.2f} per share")


def collect_portfolio():
    portfolio = {}

    while True:
        symbol = input("\nEnter stock symbol (or 'done' to finish): ").strip().upper()

        if symbol == "DONE":
            break
        if symbol not in STOCK_PRICES:
            print("Symbol not found. Choose a symbol from the displayed list.")
            continue

        try:
            quantity = int(input(f"Enter quantity for {symbol}: ").strip())
            if quantity <= 0:
                print("Quantity must be a positive whole number.")
                continue
        except ValueError:
            print("Please enter a valid whole-number quantity.")
            continue

        portfolio[symbol] = portfolio.get(symbol, 0) + quantity
        print(f"Added {quantity} share(s) of {symbol}.")

    return portfolio


def calculate_total(portfolio):
    return sum(STOCK_PRICES[symbol] * quantity for symbol, quantity in portfolio.items())


def display_portfolio(portfolio):
    if not portfolio:
        print("\nYour portfolio is empty.")
        return

    print("\n=== Portfolio Summary ===")
    print(f"{'Symbol':<10}{'Price':>12}{'Quantity':>12}{'Value':>14}")
    print("-" * 48)

    for symbol, quantity in sorted(portfolio.items()):
        price = STOCK_PRICES[symbol]
        value = price * quantity
        print(f"{symbol:<10}${price:>11.2f}{quantity:>12}${value:>13.2f}")

    print("-" * 48)
    print(f"{'Total investment:':<34}${calculate_total(portfolio):.2f}")


def export_csv(portfolio):
    try:
        with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Symbol", "Sample Price", "Quantity", "Investment Value"])
            for symbol, quantity in sorted(portfolio.items()):
                writer.writerow([
                    symbol,
                    f"{STOCK_PRICES[symbol]:.2f}",
                    quantity,
                    f"{STOCK_PRICES[symbol] * quantity:.2f}",
                ])
            writer.writerow([])
            writer.writerow(["Total Investment", "", "", f"{calculate_total(portfolio):.2f}"])
        print(f"Portfolio saved to: {OUTPUT_FILE.resolve()}")
    except OSError as error:
        print(f"Could not save the CSV file: {error}")


def main():
    print("=== CodeAlpha Stock Portfolio Tracker ===")
    show_available_stocks()
    portfolio = collect_portfolio()
    display_portfolio(portfolio)

    if portfolio:
        answer = input("\nSave portfolio to CSV? (yes/no): ").strip().lower()
        if answer in {"yes", "y"}:
            export_csv(portfolio)

    print("Thank you for using the tracker!")


if __name__ == "__main__":
    main()
