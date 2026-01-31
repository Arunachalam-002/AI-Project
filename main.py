from data_loader import load_data
from agent import KnowledgeBasedTradingAgent
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

CSV = "data/TATAMOTORS.csv"
INITIAL_CASH = 10000

if __name__ == "__main__":
    df = load_data(CSV)
    agent = KnowledgeBasedTradingAgent(short_window=10, long_window=50)

    annotated_df, decisions, facts_per_t = agent.run_inference(df)

    buys = np.full(len(annotated_df), np.nan)
    sells = np.full(len(annotated_df), np.nan)
    for i, d in enumerate(decisions):
        if d == "Buy":
            buys[i] = annotated_df["Close"].iat[i]
        elif d == "Sell":
            sells[i] = annotated_df["Close"].iat[i]

    plt.figure(figsize=(14,6))
    plt.plot(annotated_df.index, annotated_df["Close"], label="Close", alpha=0.6)
    plt.plot(annotated_df.index, annotated_df["MA_short"], "--", label="MA_short")
    plt.plot(annotated_df.index, annotated_df["MA_long"], "--", label="MA_long")
    plt.scatter(annotated_df.index, buys, marker="^", color="g", s=100, label="Buy")
    plt.scatter(annotated_df.index, sells, marker="v", color="r", s=100, label="Sell")
    plt.title("Knowledge-Based Agent Signals (from MongoDB)")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.show()

    # --- Simple Backtest ---
    cash, pos = INITIAL_CASH, 0
    for i, d in enumerate(decisions):
        price = annotated_df["Close"].iat[i]
        if d == "Buy" and cash >= price:
            pos += 1
            cash -= price
        elif d == "Sell" and pos > 0:
            cash += pos * price
            pos = 0

    final_value = cash + pos * annotated_df["Close"].iat[-1]
    print(f"\nBacktest: initial cash={INITIAL_CASH}, final portfolio value={final_value:.2f}")

    print("\nRecent 20-day facts:")
    for i, context in enumerate(facts_per_t[-20:]):
        print(f"{annotated_df.index[-20+i].date()}: "
              f"Buy={context.get('Buy', False)}, "
              f"Sell={context.get('Sell', False)}, "
              f"ExecuteBuy={context.get('ExecuteBuy', False)}, "
              f"ExecuteSell={context.get('ExecuteSell', False)}")
