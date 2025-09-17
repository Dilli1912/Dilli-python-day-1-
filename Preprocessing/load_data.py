
import numpy as np
import pandas as pd

# ---------------------------
# Optimize DataFrame
# ---------------------------
def optimize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimize numeric dtypes:
      - Integers → int8 / int16 / int32
      - Floats   → float16 / float32
    Returns a DataFrame with reduced memory usage.
    """
    before = df.memory_usage(deep=True).sum() / 1024**2
    optimized = df.copy()

    for col in optimized.columns:
        s = optimized[col]

        # --- Integers ---
        if pd.api.types.is_integer_dtype(s):
            vals = s.astype("int64")  # safe for bound checks
            if vals.min() >= np.iinfo(np.int8).min and vals.max() <= np.iinfo(np.int8).max:
                optimized[col] = s.astype("int8")
            elif vals.min() >= np.iinfo(np.int16).min and vals.max() <= np.iinfo(np.int16).max:
                optimized[col] = s.astype("int16")
            elif vals.min() >= np.iinfo(np.int32).min and vals.max() <= np.iinfo(np.int32).max:
                optimized[col] = s.astype("int32")
            # else: leave unchanged if too large

        # --- Floats ---
        elif pd.api.types.is_float_dtype(s):
            s64 = s.astype("float64")
            if np.allclose(s64, s64.astype("float16"), rtol=1e-03, atol=1e-06, equal_nan=True):
                optimized[col] = s64.astype("float16")
            else:
                optimized[col] = s64.astype("float32")

    after = optimized.memory_usage(deep=True).sum() / 1024**2
    print(f"Memory: {before:.3f} MB → {after:.3f} MB ({(before - after) / before * 100:.2f}% reduction)")

    return optimized


# ---------------------------
# Treat Nulls
# ---------------------------
def treat_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Null handling per rules:
      - Drop columns with >30% nulls
      - Numeric → fill with median
      - Categorical/Object/Bool → fill with mode
      - Datetime → forward fill, then backward fill
    """
    cleaned = df.copy()

    # 1) Drop columns over threshold
    threshold = 0.30
    null_ratio = cleaned.isna().mean()
    to_drop = null_ratio[null_ratio > threshold].index.tolist()
    cleaned = cleaned.drop(columns=to_drop)

    if cleaned.shape[1] == 0:
        return cleaned

    # 2) Identify column types
    num_cols = [c for c in cleaned.select_dtypes(include=[np.number]).columns if cleaned[c].isna().any()]
    cat_cols = [c for c in cleaned.select_dtypes(include=["object", "category", "bool"]).columns if cleaned[c].isna().any()]
    dt_cols  = [c for c in cleaned.select_dtypes(include=["datetime64"]).columns if cleaned[c].isna().any()]

    # 3) Fill numeric with median
    if num_cols:
        medians = cleaned[num_cols].median()
        cleaned[num_cols] = cleaned[num_cols].fillna(medians)

    # 4) Fill categorical with mode
    for c in cat_cols:
        mode_val = cleaned[c].mode(dropna=True)
        if not mode_val.empty:
            cleaned[c] = cleaned[c].fillna(mode_val[0])
        else:
            cleaned[c] = cleaned[c].fillna("" if cleaned[c].dtype == "object" else 0)

    # 5) Fill datetime with ffill + bfill
    for c in dt_cols:
        cleaned[c] = cleaned[c].fillna(method="ffill").fillna(method="bfill")

    return cleaned


# ---------------------------
# Outlier Detection (Optional)
# ---------------------------
def find_outliers_iqr(df: pd.DataFrame, cols=None) -> dict:
    """
    Detect outliers in numeric columns using IQR method.
    Returns a dictionary of column -> list of outlier indices.
    """
    if cols is None:
        cols = df.select_dtypes(include=np.number).columns

    outliers = {}
    for col in cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        mask = (df[col] < lower) | (df[col] > upper)
        outliers[col] = df[mask].index.tolist()
    return outliers
df = pd.read_csv("application_train.csv")
df = optimize_dataframe(df)
df.to_csv("application_train_cleaned.csv")
print(df.head(10))
D1=df.head(10)

def visualize_dataset(df):
    import matplotlib.pyplot as plt
    df.hist(figsize=(18,14),bins=50,xlabelsize=8,ylabelsize=8)
    plt.tight_layout()
    plt.show()
print(visualize_dataset(df))

