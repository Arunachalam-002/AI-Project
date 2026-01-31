"""
Knowledge base storing:
 - human-readable logical rules (strings)
 - executable rule objects (callable) used by the inference engine
"""

# ----------------------------------------------
# 1. Logical rules (for documentation / reference)
# ----------------------------------------------
logical_rules = [
    "FOR ALL t: IF BullishCross(t) AND RSI(t) < 65 THEN Buy(t)",
    "FOR ALL t: IF BearishCross(t) AND RSI(t) > 35 THEN Sell(t)",
    "FOR ALL t: IF Buy(t) THEN ExecuteBuy(t)",
    "FOR ALL t: IF Sell(t) THEN ExecuteSell(t)",
]

# ----------------------------------------------
# 2. Helper functions
# ----------------------------------------------
def bullish_cross(df, t, ctx):
    """Short MA crosses above Long MA"""
    if t == 0:
        return False
    return (
        df["MA_short"].iat[t] > df["MA_long"].iat[t]
        and df["MA_short"].iat[t - 1] <= df["MA_long"].iat[t - 1]
    )

def bearish_cross(df, t, ctx):
    """Short MA crosses below Long MA"""
    if t == 0:
        return False
    return (
        df["MA_short"].iat[t] < df["MA_long"].iat[t]
        and df["MA_short"].iat[t - 1] >= df["MA_long"].iat[t - 1]
    )

# ----------------------------------------------
# 3. Buy / Sell rule antecedents
# ----------------------------------------------
def buy_from_bull(df, t, ctx):
    # Buy when bullish crossover and RSI not overbought
    return bullish_cross(df, t, ctx) and (df["RSI"].iat[t] < 65)

def sell_from_bear(df, t, ctx):
    # Sell when bearish crossover and RSI not oversold
    return bearish_cross(df, t, ctx) and (df["RSI"].iat[t] > 35)

# ----------------------------------------------
# 4. Execution rules
# ----------------------------------------------
# (No "holding" logic restriction so we can see both buy/sell clearly)
def exec_buy(df, t, ctx):
    return ctx.get("Buy", False)

def exec_sell(df, t, ctx):
    return ctx.get("Sell", False)

# ----------------------------------------------
# 5. Rule list for inference engine
# ----------------------------------------------
executable_rules = [
    {"name": "BullishCross", "antecedent": bullish_cross, "consequent": "BullishCross"},
    {"name": "BearishCross", "antecedent": bearish_cross, "consequent": "BearishCross"},
    {"name": "BuyFromBull", "antecedent": buy_from_bull, "consequent": "Buy"},
    {"name": "SellFromBear", "antecedent": sell_from_bear, "consequent": "Sell"},
    {"name": "ExecuteBuy", "antecedent": exec_buy, "consequent": "ExecuteBuy"},
    {"name": "ExecuteSell", "antecedent": exec_sell, "consequent": "ExecuteSell"},
]
