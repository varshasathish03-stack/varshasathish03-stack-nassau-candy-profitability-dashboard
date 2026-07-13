# ============================================================
# Nassau Candy Distributor — Streamlit Dashboard
# Mirrors Tableau Workbook: visualization.twb
#
# Sheet 1: Gross Margin (%) by Product Name (bar) — colored by Product Name
#           Labels: SUM(Gross Profit) as %, Division
# Sheet 2: Margin Risk flag (rows) × SUM(Gross Profit), SUM(Sales), SUM(Cost)
#           Scatter — colored by Product Name
# Sheet 3: Division / Product Name (cols) × SUM(Gross Profit) (rows)
#           Bar — labeled with SUM(Revenue per Unit ($))
# Sheet 4: Product Name (rows) × Division / Margin Risk flag (cols)
#           Text table — values = SUM(Profit per Unit ($)), colored by Risk flag
#
# Run:  streamlit run nassau_streamlit_app.py
# Req:  pip install streamlit plotly pandas numpy
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="Nassau Candy — Profitability Dashboard",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Exact Tableau color map for Product Name ───────────────
PRODUCT_COLORS = {
    "SweeTARTS":                           "#499894",
    "Everlasting Gobstopper":              "#4e79a7",
    "Kazookles":                           "#59a14f",
    "Wonka Bar - Scrumdiddlyumptious":     "#79706e",
    "Wonka Bar - Fudge Mallows":           "#86bcb6",
    "Laffy Taffy":                         "#8cd17d",
    "Fizzy Lifting Drinks":                "#a0cbe8",
    "Lickable Wallpaper":                  "#b6992d",
    "Wonka Bar - Triple Dazzle Caramel":   "#bab0ac",
    "Wonka Gum":                           "#d37295",
    "Wonka Bar - Milk Chocolate":          "#e15759",
    "Nerds":                               "#f1ce63",
    "Fun Dip":                             "#f28e2b",
    "Wonka Bar - Nutty Crunch Surprise":   "#ff9d9a",
    "Hair Toffee":                         "#ffbe7d",
}
RISK_COLORS  = {"Safe": "#59a14f", "Risk": "#e15759"}
DIV_COLORS   = {"Chocolate": "#c47a3a", "Other": "#5b9cf6", "Sugar": "#e07c9a"}

DARK  = "#0f0f0f"
CARD  = "#1a1a1a"
BORDER= "#2a2a2a"
TEXT  = "#e8e0d0"
MUTED = "#888070"

# ── Theme CSS ───────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{background:#0d0d0d}
[data-testid="stSidebar"]{background:#141414;border-right:1px solid #222}
[data-testid="stSidebar"] *{color:#e0d8cc!important}
.block-container{padding:1.5rem 2rem}
h1,h2,h3{font-family:'Georgia',serif!important}
div[data-testid="stPlotlyChart"]{background:transparent!important}
.stSelectbox label,.stSlider label,.stDateInput label,
.stMultiSelect label,.stTextInput label{color:#a09890!important;font-size:13px!important}
div[data-baseweb="tab-list"]{background:#1a1a1a;border-radius:8px;padding:4px}
div[data-baseweb="tab"]{color:#a09890!important}
div[aria-selected="true"]{background:#2a2a2a!important;border-radius:6px}
.kpi-box{background:#1a1a1a;border:0.5px solid #2a2a2a;border-radius:12px;
         padding:1rem 1.4rem;margin-bottom:0.5rem}
.kpi-lbl{font-size:11px;color:#7a7268;letter-spacing:.1em;
         text-transform:uppercase;font-family:monospace;margin-bottom:6px}
.kpi-val{font-size:26px;font-family:Georgia,serif;color:#f0ece3;line-height:1;margin-bottom:4px}
.kpi-sub{font-size:12px;color:#9a9288}
</style>""", unsafe_allow_html=True)

def plot_cfg(fig, h=400):
    fig.update_layout(
        plot_bgcolor=CARD, paper_bgcolor=CARD,
        font=dict(color=TEXT, family="Outfit,sans-serif", size=12),
        height=h, margin=dict(l=10,r=10,t=40,b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=BORDER,
                    font=dict(size=10,color=TEXT)),
        xaxis=dict(gridcolor=BORDER, zeroline=False, tickfont=dict(color=MUTED)),
        yaxis=dict(gridcolor=BORDER, zeroline=False, tickfont=dict(color=MUTED)),
    )
    return fig

# ── Load & prepare data ────────────────────────────────────
@st.cache_data
def load():
    df = pd.read_csv("nassau_candy_cleaned.csv", parse_dates=["Order Date","Ship Date"])
    df["Margin Risk flag"] = df["Gross Margin (%)"].apply(
        lambda x: "Risk" if x < 50 else "Safe")
    df["Profitability Category"] = df["Gross Margin (%)"].apply(
        lambda x: "High Profit" if x > 60 else ("Medium Profit" if x > 40 else "Low Profit"))
    return df

df_full = load()

# ── Sidebar Filters ────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍬 Nassau Candy")
    st.markdown("**Profitability Dashboard**")
    st.markdown("---")

    st.markdown("### 🏭 Division")
    all_divs = sorted(df_full["Division"].unique())
    sel_divs = st.multiselect("Division", all_divs, default=all_divs)
    if not sel_divs: sel_divs = all_divs
    
    st.markdown("### 📅 Date Range")
    d0 = df_full["Order Date"].min().date()
    d1 = df_full["Order Date"].max().date()
    rng = st.date_input("Order date", value=(d0,d1), min_value=d0, max_value=d1)
    ds = pd.Timestamp(rng[0]) if len(rng)>=1 else pd.Timestamp(d0)
    de = pd.Timestamp(rng[1]) if len(rng)==2 else pd.Timestamp(d1)
    
    
    st.markdown("### 📊 Margin Risk Threshold")
    threshold = st.slider("Risk below (%)", 0, 100, 50, 1,
                          help="Matches Tableau calc: < threshold → Risk")

    st.markdown("### 🔍 Product Search")
    search = st.text_input("Product name contains", "")

    st.markdown("---")
    st.caption(f"Records: {len(df_full):,} | Products: {df_full['Product Name'].nunique()}")

# ── Apply filters ──────────────────────────────────────────
df = df_full.copy()
df = df[(df["Order Date"] >= ds) & (df["Order Date"] <= de)]
df = df[df["Division"].isin(sel_divs)]
if search:
    df = df[df["Product Name"].str.contains(search, case=False, na=False)]
df["Margin Risk flag"] = df["Gross Margin (%)"].apply(
    lambda x: "Risk" if x < threshold else "Safe")

if df.empty:
    st.warning("No data for current filters.")
    st.stop()

# ── Product-level aggregation (matches Tableau SUM aggregation) ──
pm = (df.groupby(["Division","Product Name"]).agg(
        GP   =("Gross Profit","sum"),
        Sales=("Sales","sum"),
        Cost =("Cost","sum"),
        Units=("Units","sum"),
        RevPerUnit=("Revenue per Unit ($)","sum"),
        ProfPerUnit=("Profit per Unit ($)","sum"),
     ).reset_index())
pm["Avg_Margin"] = (pm["GP"] / pm["Sales"] * 100).round(2)
pm["Margin Risk flag"] = pm["Avg_Margin"].apply(
    lambda x: "Risk" if x < threshold else "Safe")
pm["GP_pct"] = (pm["GP"] / pm["GP"].sum() * 100).round(1)
pm = pm.sort_values("GP", ascending=False).reset_index(drop=True)

# KPIs
tot_rev = df["Sales"].sum()
tot_gp  = df["Gross Profit"].sum()
tot_units = df["Units"].sum()
avg_m = tot_gp/tot_rev*100 if tot_rev else 0
risk_n = (pm["Margin Risk flag"]=="Risk").sum()

# ── Header ─────────────────────────────────────────────────
st.markdown("""<div style="padding:.5rem 0 1rem">
  <p style="font-family:monospace;font-size:11px;color:#e8c97a;letter-spacing:.12em;
     text-transform:uppercase;margin-bottom:4px">Exploratory Data Analysis</p>
  <h1 style="font-family:Georgia,serif;font-size:2.2rem;color:#f0ece3;margin:0;line-height:1.1">
    Nassau Candy — <em style="color:#e8c97a">Profitability</em> Dashboard</h1>
  <p style="color:#7a7268;font-size:13px;margin-top:4px">
    Mirrors Tableau Workbook · 4 sheets · FY 2024–2025</p>
</div>""", unsafe_allow_html=True)

c1,c2,c3,c4,c5 = st.columns(5)
for col, lbl, val, sub in [
    (c1,"Total Revenue",     f"${tot_rev:,.0f}",  f"{len(df):,} transactions"),
    (c2,"Gross Profit",      f"${tot_gp:,.0f}",   f"{avg_m:.1f}% avg margin"),
    (c3,"Units Sold",        f"{tot_units:,}",     f"{pm['Product Name'].nunique()} products"),
    (c4,"At-Risk Products",  str(risk_n),          f"Below {threshold}% margin"),
    (c5,"Top GP Product",    pm.iloc[0]["Product Name"].replace("Wonka Bar - ","") if len(pm) else "—",
                             f"${pm.iloc[0]['GP']:,.0f} · {pm.iloc[0]['GP_pct']:.1f}% share" if len(pm) else ""),
]:
    col.markdown(f"""<div class="kpi-box">
      <div class="kpi-lbl">{lbl}</div>
      <div class="kpi-val">{val}</div>
      <div class="kpi-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ────────────────────────────────────────────────────
t1,t2,t3,t4 = st.tabs([
    "📊 Sheet 1 — Gross Margin % by Product",
    "🔵 Sheet 2 — Cost/Sales Scatter + Risk",
    "📦 Sheet 3 — GP by Division / Product",
    "📋 Sheet 4 — Profit per Unit Table",
])

# ════════════════════════════════════════════════════════════
# SHEET 1 — Bar: Product Name (x) × SUM(Gross Margin %) (y)
#           Color = Product Name, Labels = SUM(GP) as % + Division
# ════════════════════════════════════════════════════════════
with t1:
    st.markdown("**Gross Margin (%) by Product Name** — bar height = avg gross margin %, "
                "labeled with gross profit $ and division. Color matches Tableau palette.")

    s1 = pm.sort_values("Avg_Margin", ascending=False).copy()

    fig1 = go.Figure()
    for _, row in s1.iterrows():
        col = PRODUCT_COLORS.get(row["Product Name"], "#aaa")
        label = f"{row['GP']:,.0f}<br>{row['Division']}"
        fig1.add_trace(go.Bar(
            x=[row["Product Name"]],
            y=[row["Avg_Margin"]],
            name=row["Product Name"],
            marker_color=col,
            marker_line_width=0,
            text=[label],
            textposition="outside",
            textfont=dict(size=9, color=TEXT),
            hovertemplate=(
                f"<b>{row['Product Name']}</b><br>"
                f"Division: {row['Division']}<br>"
                f"Gross Margin: {row['Avg_Margin']:.1f}%<br>"
                f"Gross Profit: ${row['GP']:,.0f}<br>"
                f"GP share: {row['GP_pct']:.1f}%"
                "<extra></extra>"
            ),
        ))
    fig1.add_hline(y=threshold, line_dash="dash", line_color="#e8c97a",
                   annotation_text=f"Risk threshold {threshold}%",
                   annotation_font_color="#e8c97a", line_width=1.5)
    fig1.update_layout(
        showlegend=False,
        yaxis_title="Gross Margin (%)",
        xaxis_tickangle=-30,
        bargap=0.3,
    )
    st.plotly_chart(plot_cfg(fig1, 460), use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Gross Profit donut by Product**")
        fig1b = go.Figure(go.Pie(
            labels=s1["Product Name"],
            values=s1["GP"],
            hole=0.55,
            marker=dict(
                colors=[PRODUCT_COLORS.get(p,"#aaa") for p in s1["Product Name"]],
                line=dict(color="#0d0d0d", width=2),
            ),
            textinfo="percent",
            textfont=dict(size=9),
            hovertemplate="<b>%{label}</b><br>GP: $%{value:,.0f}<br>%{percent}<extra></extra>",
        ))
        fig1b.update_layout(showlegend=False)
        st.plotly_chart(plot_cfg(fig1b, 320), use_container_width=True)
    with col_b:
        st.markdown("**Product detail table**")
        tbl = s1[["Product Name","Division","Sales","GP","Avg_Margin","GP_pct","Margin Risk flag"]].copy()
        tbl.columns = ["Product","Division","Revenue","GP ($)","Margin %","GP Share %","Risk"]
        tbl["Revenue"] = tbl["Revenue"].apply(lambda x: f"${x:,.0f}")
        tbl["GP ($)"]  = tbl["GP ($)"].apply(lambda x: f"${x:,.0f}")
        tbl["Margin %"]= tbl["Margin %"].apply(lambda x: f"{x:.1f}%")
        tbl["GP Share %"] = tbl["GP Share %"].apply(lambda x: f"{x:.1f}%")
        st.dataframe(tbl.reset_index(drop=True), use_container_width=True, height=310)

# ════════════════════════════════════════════════════════════
# SHEET 2 — Scatter: rows = Margin Risk flag × cols = Sales + Cost
#           Color = Product Name (Tableau palette)
# ════════════════════════════════════════════════════════════
with t2:
    st.markdown("**Cost vs Sales scatter with Margin Risk flag rows** — "
                "replicates Tableau Sheet 2: each dot = one product, "
                "rows split by Risk/Safe, two x-axes (Sales, Cost), "
                "color = Product Name.")

    s2 = pm.copy()
    s2["short"] = s2["Product Name"].str.replace("Wonka Bar - ","").str.replace("Wonka ","")

    col_a, col_b = st.columns(2)
    for col_ax, xfield, xtitle, container in [
        (col_a, "Sales", "SUM(Sales)", col_a),
        (col_b, "Cost",  "SUM(Cost)",  col_b),
    ]:
        with container:
            fig2 = px.scatter(
                s2, x=xfield, y="Margin Risk flag",
                color="Product Name",
                color_discrete_map=PRODUCT_COLORS,
                size="GP", size_max=40,
                text="short",
                hover_data={"GP":".0f","Avg_Margin":".1f","Sales":".0f","Cost":".0f"},
                title=f"GP vs {xtitle} — by Margin Risk",
            )
            fig2.update_traces(textposition="top center", textfont_size=8)
            fig2.update_layout(showlegend=False, xaxis_title=xtitle,
                               yaxis_title="Margin Risk flag")
            st.plotly_chart(plot_cfg(fig2, 340), use_container_width=True)

    st.markdown("**COGS % of Revenue — risk flagging**")
    s2["COGS_pct"] = (s2["Cost"]/s2["Sales"]*100).round(1)
    s2s = s2.sort_values("COGS_pct", ascending=False)
    fig2b = go.Figure()
    for _, row in s2s.iterrows():
        fig2b.add_trace(go.Bar(
            x=[row["short"]], y=[row["COGS_pct"]],
            name=row["Product Name"],
            marker_color=RISK_COLORS[row["Margin Risk flag"]],
            marker_line_width=0,
            text=[f"{row['COGS_pct']:.1f}%"],
            textposition="outside",
            textfont=dict(size=9, color=TEXT),
            hovertemplate=(f"<b>{row['Product Name']}</b><br>"
                           f"COGS %: {row['COGS_pct']:.1f}%<br>"
                           f"Risk: {row['Margin Risk flag']}<extra></extra>"),
        ))
    fig2b.add_hline(y=100-threshold, line_dash="dot", line_color="#e8c97a",
                    annotation_text=f"COGS limit = {100-threshold}%",
                    annotation_font_color="#e8c97a", line_width=1.2)
    fig2b.update_layout(showlegend=False, xaxis_tickangle=-30,
                        yaxis_title="COGS as % of Revenue")
    st.plotly_chart(plot_cfg(fig2b, 360), use_container_width=True)

    st.markdown("**At-risk product detail**")
    risk_df = s2[s2["Margin Risk flag"]=="Risk"][
        ["Product Name","Division","Sales","Cost","GP","Avg_Margin","COGS_pct"]].copy()
    if risk_df.empty:
        st.success(f"✓ No products below {threshold}% margin threshold.")
    else:
        st.warning(f"⚠ {len(risk_df)} product(s) below {threshold}%")
        risk_df.columns = ["Product","Division","Revenue","COGS","GP","Margin %","COGS %"]
        for c in ["Revenue","COGS","GP"]:
            risk_df[c] = risk_df[c].apply(lambda x: f"${x:,.0f}")
        risk_df["Margin %"] = risk_df["Margin %"].apply(lambda x: f"{x:.1f}%")
        risk_df["COGS %"]   = risk_df["COGS %"].apply(lambda x: f"{x:.1f}%")
        st.dataframe(risk_df.reset_index(drop=True), use_container_width=True)

# ════════════════════════════════════════════════════════════
# SHEET 3 — Bar: (Division / Product Name) cols × SUM(GP) rows
#           Color = Product Name, label = SUM(Revenue per Unit ($))
# ════════════════════════════════════════════════════════════
with t3:
    st.markdown("**Gross Profit by Division › Product Name** — "
                "grouped by Division, then Product (matches Tableau Sheet 3 layout). "
                "Bar label = SUM(Revenue per Unit $).")

    s3 = pm.sort_values(["Division","GP"], ascending=[True,False]).copy()

    fig3 = go.Figure()
    for div in s3["Division"].unique():
        sub = s3[s3["Division"]==div]
        for _, row in sub.iterrows():
            col = PRODUCT_COLORS.get(row["Product Name"],"#aaa")
            fig3.add_trace(go.Bar(
                x=[f"{row['Division']}<br>{row['Product Name'].replace('Wonka Bar - ','').replace('Wonka ','')}"],
                y=[row["GP"]],
                name=row["Product Name"],
                marker_color=col,
                marker_line_width=0,
                text=[f"{row['RevPerUnit']:,.0f}"],
                textposition="outside",
                textfont=dict(size=8, color=TEXT),
                hovertemplate=(
                    f"<b>{row['Product Name']}</b><br>"
                    f"Division: {row['Division']}<br>"
                    f"Gross Profit: ${row['GP']:,.0f}<br>"
                    f"Rev/Unit (sum): ${row['RevPerUnit']:,.0f}"
                    "<extra></extra>"
                ),
            ))
    fig3.update_layout(showlegend=False, bargap=0.25,
                       yaxis_title="SUM(Gross Profit)",
                       xaxis_tickangle=-25)
    st.plotly_chart(plot_cfg(fig3, 480), use_container_width=True)

    st.markdown("**Division summary**")
    dm = (df.groupby("Division").agg(
        Revenue=("Sales","sum"), GP=("Gross Profit","sum"),
        Units=("Units","sum"), Txns=("Row ID","count")
    ).reset_index())
    dm["Margin %"] = (dm["GP"]/dm["Revenue"]*100).round(1)
    dm["GP Share"] = (dm["GP"]/dm["GP"].sum()*100).round(1)

    col_a,col_b = st.columns(2)
    with col_a:
        fig3b = go.Figure()
        for _, row in dm.iterrows():
            fig3b.add_trace(go.Bar(
                x=[row["Division"]], y=[row["Revenue"]],
                name=row["Division"],
                marker_color=DIV_COLORS.get(row["Division"],"#aaa"),
                marker_line_width=0,
                opacity=0.5,
            ))
            fig3b.add_trace(go.Bar(
                x=[row["Division"]], y=[row["GP"]],
                showlegend=False,
                marker_color=DIV_COLORS.get(row["Division"],"#aaa"),
                marker_line_width=0,
            ))
        fig3b.add_annotation(x=0.5, y=1.06, xref="paper", yref="paper",
                             text="dim = Revenue  |  solid = GP", showarrow=False,
                             font=dict(size=10, color=MUTED))
        fig3b.update_layout(barmode="group", showlegend=False,
                            yaxis_title="Amount ($)")
        st.plotly_chart(plot_cfg(fig3b, 300), use_container_width=True)
    with col_b:
        fig3c = go.Figure(go.Pie(
            labels=dm["Division"], values=dm["GP"], hole=0.5,
            marker=dict(
                colors=[DIV_COLORS.get(d,"#aaa") for d in dm["Division"]],
                line=dict(color="#0d0d0d",width=2)),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>GP: $%{value:,.0f}<br>%{percent}<extra></extra>",
        ))
        fig3c.update_layout(showlegend=False)
        st.plotly_chart(plot_cfg(fig3c, 300), use_container_width=True)

# ════════════════════════════════════════════════════════════
# SHEET 4 — Text table: Product Name (rows) × Division/Risk (cols)
#           Values = SUM(Profit per Unit ($)), color = Risk flag
# ════════════════════════════════════════════════════════════
with t4:
    st.markdown("**Profit per Unit table by Division & Margin Risk flag** — "
                "replicates Tableau Sheet 4: rows = Product Name, "
                "columns = Division × Risk flag, value = SUM(Profit per Unit $), "
                "green = Safe, red = Risk.")

    s4 = pm[["Division","Product Name","ProfPerUnit","Margin Risk flag"]].copy()

    pivot = s4.pivot_table(
        index="Product Name",
        columns=["Division","Margin Risk flag"],
        values="ProfPerUnit",
        aggfunc="sum",
    ).fillna(0)

    # Reorder columns to match Tableau (Division alpha, then Risk/Safe)
    pivot = pivot.sort_index(axis=1)
    # Sort rows by total desc
    pivot["_total"] = pivot.sum(axis=1)
    pivot = pivot.sort_values("_total", ascending=True).drop(columns="_total")

    # Build heatmap
    z, text_vals, x_labels = [], [], []
    for col in pivot.columns:
        x_labels.append(f"{col[0]}<br>{col[1]}")
    for prod in pivot.index:
        row_z, row_t = [], []
        for col in pivot.columns:
            v = pivot.loc[prod, col]
            is_risk = col[1] == "Risk"
            row_z.append(1 if is_risk else 0)
            row_t.append(f"{v:.2f}" if v > 0 else "")
        z.append(row_z)
        text_vals.append(row_t)

    fig4 = go.Figure(go.Heatmap(
        z=z, x=x_labels, y=list(pivot.index),
        text=text_vals,
        texttemplate="%{text}",
        textfont=dict(size=11, color="white"),
        colorscale=[[0,"#59a14f"],[1,"#e15759"]],
        showscale=False,
        hovertemplate="<b>%{y}</b><br>%{x}<br>Profit/Unit: $%{text}<extra></extra>",
    ))
    fig4.update_layout(
        xaxis=dict(side="top", tickangle=-20, tickfont=dict(size=10,color=MUTED)),
        yaxis=dict(tickfont=dict(size=10,color=TEXT)),
        margin=dict(l=220,r=10,t=60,b=10),
    )
    st.plotly_chart(plot_cfg(fig4, 520), use_container_width=True)

    # Also show raw pivot as dataframe
    st.markdown("**Raw pivot table values**")
    show = pivot.copy()
    show.columns = [f"{a}/{b}" for a,b in show.columns]
    show = show.map(lambda v: f"${v:.2f}" if v > 0 else "—")
    st.dataframe(show, use_container_width=True, height=400)

# ── Footer ──────────────────────────────────────────────────
st.markdown("---")
st.markdown("""<div style="display:flex;justify-content:space-between;
  padding:.4rem 0;font-size:12px;color:#4a4640">
  <span>Nassau Candy Distributors · FY 2024–2025 · Tableau Mirror Dashboard</span>
  <span style="font-family:Georgia,serif;color:#e8c97a">Nassau Candy</span>
</div>""", unsafe_allow_html=True)
