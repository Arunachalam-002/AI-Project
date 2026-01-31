from knowledge_db import load_rules_from_db, load_percepts_from_db
from inference_engine import infer_for_time
from utils import moving_average, RSI
import numpy as np

# Define core reasoning functions (local executable logic)
def bullish_cross(df, t, ctx):
    if t == 0:
        return False
    return (df["MA_short"].iat[t] > df["MA_long"].iat[t]) and (df["MA_short"].iat[t-1] <= df["MA_long"].iat[t-1])

def bearish_cross(df, t, ctx):
    if t == 0:
        return False
    return (df["MA_short"].iat[t] < df["MA_long"].iat[t]) and (df["MA_short"].iat[t-1] >= df["MA_long"].iat[t-1])

def buy_from_bull(df, t, ctx):
    return bullish_cross(df, t, ctx) and (df["RSI"].iat[t] < 65)

def sell_from_bear(df, t, ctx):
    return bearish_cross(df, t, ctx) and (df["RSI"].iat[t] > 35)

def exec_buy(df, t, ctx):
    return ctx.get("Buy", False)

def exec_sell(df, t, ctx):
    return ctx.get("Sell", False)


class KnowledgeBasedTradingAgent:
    def __init__(self, short_window=10, long_window=50):
        self.short_window = short_window
        self.long_window = long_window

        # Load knowledge dynamically
        self.logical_rules = load_rules_from_db()
        self.percepts = load_percepts_from_db()

        # Link human-readable rules to executable logic
        self.executable_rules = [
            {"name": "BullishCross", "antecedent": bullish_cross, "consequent": "BullishCross"},
            {"name": "BearishCross", "antecedent": bearish_cross, "consequent": "BearishCross"},
            {"name": "BuyFromBull", "antecedent": buy_from_bull, "consequent": "Buy"},
            {"name": "SellFromBear", "antecedent": sell_from_bear, "consequent": "Sell"},
            {"name": "ExecuteBuy", "antecedent": exec_buy, "consequent": "ExecuteBuy"},
            {"name": "ExecuteSell", "antecedent": exec_sell, "consequent": "ExecuteSell"},
        ]

    def annotate_indicators(self, df):
        df = df.copy()
        df["MA_short"] = moving_average(df["Close"], self.short_window)
        df["MA_long"] = moving_average(df["Close"], self.long_window)
        df["RSI"] = RSI(df["Close"], period=14)
        return df

    def run_inference(self, df):
        df = self.annotate_indicators(df)
        n = len(df)
        decisions = [None] * n
        facts_per_t = [None] * n

        for t in range(n):
            context = infer_for_time(df.reset_index(drop=True), t, self.executable_rules)
            facts_per_t[t] = context
            if context.get("ExecuteBuy", False):
                decisions[t] = "Buy"
            elif context.get("ExecuteSell", False):
                decisions[t] = "Sell"
            else:
                decisions[t] = None
        return df, decisions, facts_per_t
