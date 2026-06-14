def query_data(cached_dfs: dict, dataset: str, state: str = None,
               commodity: str = None, aggregation: str = None,
               column: str = None, date_from: str = None,
               date_to: str = None) -> dict:
    
    df = cached_dfs.get(dataset)
    if df is None:
        return {"error": f"Dataset '{dataset}' not found in cache"}

    # Filters ----------------------------------------------------
    # state filter 
    # state filter — same column for both datasets now
    # state filter — same column for both datasets now
    if state:
        df = df.dropna(subset=["provider_admin1_name"])
        df = df[df["provider_admin1_name"].str.lower() == state.lower()]
        if df.empty:
            return {"error": f"No data found for state '{state}' in {dataset}"}

    # commodity filter (food_price only)
    if commodity and dataset == "food_price":
        df = df[df["commodity_name"].str.lower() == commodity.lower()]
        if df.empty:
            return {"error": f"No data found for '{commodity}' in {dataset}"}

    # date range filter — same column for both datasets now
    if date_from or date_to:
        df["reference_period_end"] = pd.to_datetime(df["reference_period_end"])
        if date_from:
            df = df[df["reference_period_end"] >= pd.to_datetime(date_from)]
        if date_to:
            df = df[df["reference_period_end"] <= pd.to_datetime(date_to)]
        if df.empty:
            return {"error": "No data found for the given date range"}
        
    # clean NaN values before returning
    df = df.fillna(value="")
    
    # aggregation
    if aggregation == "latest":
        df = df.sort_values("reference_period_end", ascending=False)
        result = df.head(10).to_dict(orient="records")
        return {"result": result, "aggregation": "latest"}

    elif aggregation == "average":
        if column is None:
            return {"error": "column parameter required for average aggregation"}
        if column not in df.columns:
            return {"error": f"Column '{column}' not found in {dataset}"}
        result = float(df[column].mean())
        return {"result": {f"average_{column}": round(result, 4)}, "aggregation": "average"}

    elif aggregation == "trend":
        if column is None:
            return {"error": "column parameter required for trend aggregation"}
        if column not in df.columns:
            return {"error": f"Column '{column}' not found in {dataset}"}
        df_sorted = df.sort_values("reference_period_end", ascending=True)
        earliest = float(df_sorted[column].iloc[0])
        latest = float(df_sorted[column].iloc[-1])
        pct_change = float(((latest - earliest) / earliest) * 100)
        return {"result": {"earliest": round(earliest, 4), "latest": round(latest, 4), "pct_change": round(pct_change, 2)}, "aggregation": "trend"}

    return {"result": df.head(10).to_dict(orient="records")}
    