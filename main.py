import pandas as pd
pd.set_option('display.float_format', '{:.2f}'.format)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

def load_portfolio():
    """Load portfolio from CSV."""
    try:
        df = pd.read_csv("portfolio.csv")
        # Ensure required columns
        required_cols = ['symbol', 'quantity', 'buy_price', 'current_price']
        for col in required_cols:
            if col not in df.columns:
                df[col] = 0  # Fallback
        return df
    except FileNotFoundError:
        print("❌ portfolio.csv not found. Creating new...")
        return pd.DataFrame(columns=['symbol', 'quantity', 'buy_price', 'current_price'])
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        exit(1)

def save_portfolio(df):
    """Save portfolio to CSV."""
    df.to_csv("portfolio.csv", index=False)
    print("💾 Portfolio saved!")

def print_report(df):
    """Print formatted portfolio report."""
    if df.empty:
        print("📭 Portfolio is empty.")
        return

    # Calculate metrics
    df["investment"] = df["quantity"] * df["buy_price"]
    df["current_value"] = df["quantity"] * df["current_price"]
    df["profit_loss"] = df["current_value"] - df["investment"]
    df['profit_pct'] = (df['profit_loss'] / df["investment"] * 100).round(2).fillna(0)

    # Totals
    total_investment = df["investment"].sum()
    total_current_value = df["current_value"].sum()
    total_profit_loss = df["profit_loss"].sum()
    total_profit_pct = (total_profit_loss / total_investment * 100).round(2) if total_investment > 0 else 0

    print("📊 STOCK PORTFOLIO REPORT")
    df_sorted = df.sort_values('symbol')
    print(df_sorted[['symbol', 'quantity', 'buy_price', 'current_price', 'investment', 'current_value', 'profit_loss', 'profit_pct']].to_string(index=False))

    print("\n📈 PORTFOLIO SUMMARY")
    print(f"Total Investment     : ${total_investment:.2f}")
    print(f"Total Current Value  : ${total_current_value:.2f}")
    print(f"Total Profit/Loss    : ${total_profit_loss:.2f} ({total_profit_pct:+.2f}%)")
    if total_profit_loss > 0:
        print("🎉 PROFITABLE PORTFOLIO!")
    else:
        print("📉 Review your positions.")

def add_stock(df):
    """Add new stock interactively."""
    symbol = input("Enter stock symbol: ").strip().upper()
    try:
        quantity = int(input("Enter quantity: "))
        buy_price = float(input("Enter buy price: "))
        current_price = float(input("Enter current price: "))
    except ValueError:
        print("❌ Invalid input. Try again.")
        return df

    new_row = pd.DataFrame({
        'symbol': [symbol],
        'quantity': [quantity],
        'buy_price': [buy_price],
        'current_price': [current_price]
    })
    df = pd.concat([df, new_row], ignore_index=True)
    print(f"✅ Added {quantity} shares of {symbol}")
    return df

# Main interactive loop
while True:
    print("\n=== STOCK PORTFOLIO MANAGER ===")
    print("1. View Report")
    print("2. Add Stock")
    print("3. Quit")
    choice = input("Choose (1-3): ").strip()

    if choice == '1':
        df = load_portfolio()
        print_report(df)
    elif choice == '2':
        df = load_portfolio()
        df = add_stock(df)
        save_portfolio(df)
    elif choice == '3':
        print("👋 Goodbye!")
        break
    else:
        print("❌ Invalid choice. Try again.")
