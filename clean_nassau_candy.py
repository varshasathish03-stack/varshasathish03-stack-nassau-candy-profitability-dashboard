"""
Nassau Candy Distributor — Raw to Cleaned CSV
=============================================
Transforms Nassau_Candy_Distributor.csv into the cleaned format.

Transformations applied:
  1. Parse dates (DD-MM-YYYY → YYYY-MM-DD) for Order Date & Ship Date
  2. Fix product name typo: 'Wonka Bar -Scrumdiddlyumptious'
                         → 'Wonka Bar - Scrumdiddlyumptious'
  3. Add derived financial columns:
       - Gross Margin (%)        = round(Gross Profit / Sales * 100, 2)
       - Profit per Unit ($)     = round(Gross Profit / Units, 2)
       - Revenue per Unit ($)    = round(Sales / Units, 2)
       - Cost per Unit ($)       = round(Cost / Units, 2)
  4. Add calendar columns derived from Order Date:
       - Year        (int)
       - Month       (int, 1-12)
       - Month Name  (Jan, Feb, …, Dec)
       - Quarter     (e.g. 2024Q1)
"""

import pandas as pd


# ── 1. Load raw file ──────────────────────────────────────────────────────────
df = pd.read_csv("Nassau_Candy_Distributor.csv")


# ── 2. Parse & reformat dates (DD-MM-YYYY → YYYY-MM-DD) ──────────────────────
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y").dt.strftime("%Y-%m-%d")
df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  format="%d-%m-%Y").dt.strftime("%Y-%m-%d")


# ── 3. Fix Product Name typo ──────────────────────────────────────────────────
# Raw has 'Wonka Bar -Scrumdiddlyumptious' (missing space after dash)
df["Product Name"] = df["Product Name"].str.replace(
    r"Wonka Bar -Scrumdiddlyumptious",
    "Wonka Bar - Scrumdiddlyumptious",
    regex=False,
)


# ── 4. Derived financial columns ──────────────────────────────────────────────
df["Gross Margin (%)"]      = (df["Gross Profit"] / df["Sales"] * 100).round(2)
df["Profit per Unit ($)"]   = (df["Gross Profit"] / df["Units"]).round(2)
df["Revenue per Unit ($)"]  = (df["Sales"]        / df["Units"]).round(2)
df["Cost per Unit ($)"]     = (df["Cost"]         / df["Units"]).round(2)


# ── 5. Calendar columns from Order Date ───────────────────────────────────────
order_dt = pd.to_datetime(df["Order Date"], format="%Y-%m-%d")

df["Year"]       = order_dt.dt.year
df["Month"]      = order_dt.dt.month
df["Month Name"] = order_dt.dt.strftime("%b")           # Jan, Feb, …, Dec

# Quarter: e.g. 2024Q1 — built from year + pandas quarter number
df["Quarter"] = order_dt.dt.year.astype(str) + "Q" + order_dt.dt.quarter.astype(str)


# ── 6. Save cleaned file ──────────────────────────────────────────────────────
output_path = "nassau_candy_cleaned.csv"
df.to_csv(output_path, index=False)

print(f"Done! Cleaned file saved to: {output_path}")
print(f"Rows: {len(df):,}  |  Columns: {len(df.columns)}")
print("\nColumn list:")
for col in df.columns:
    print(f"  {col}")
