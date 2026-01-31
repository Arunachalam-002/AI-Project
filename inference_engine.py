from copy import deepcopy

def infer_for_time(df, t, executable_rules):
    """Forward-chaining inference for one time step."""
    context = {}
    if 'Volume' in df.columns:
        context['volume_median'] = df['Volume'].rolling(window=20, min_periods=1).median().iat[t]

    added = True
    while added:
        added = False
        for rule in executable_rules:
            if rule['consequent'] in context and context[rule['consequent']] is True:
                continue
            try:
                result = bool(rule['antecedent'](df, t, context))
            except Exception:
                result = False

            if result:
                context[rule['consequent']] = True
                added = True
    return context
