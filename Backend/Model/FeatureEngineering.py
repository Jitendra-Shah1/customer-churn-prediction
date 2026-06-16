def engineering_features(df):
    df["has_3_plus_products"] = (df["NumOfProducts"] >= 3).astype(int)
    df["is_high_risk_age"] = ((df["Age"] >= 40) & (df["Age"] <= 60)).astype(int)
    df["has_zero_balance"] = (df["Balance"] == 0).astype(int)
    df["is_germany"] = (df["Geography"] == "Germany").astype(int)
    return df

