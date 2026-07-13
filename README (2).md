# 🍬 Nassau Candy Distributor – Data Analytics Project

## 📌 Project Overview

This project performs a comprehensive **Exploratory Data Analysis (EDA)** and **profitability analysis** on the **Nassau Candy Distributor** dataset. The objective is to transform raw transactional data into meaningful business insights and visualize product and division performance through an interactive dashboard.

The project includes:

* Data cleaning and preprocessing
* Feature engineering
* Exploratory Data Analysis (EDA)
* Profitability analysis
* Risk analysis
* Interactive Streamlit dashboard
* Business insights and recommendations

---

## 📂 Project Structure

```text
├── Nassau_Candy_Distributor.csv        # Raw dataset
├── clean_nassau_candy.py              # Data cleaning and feature engineering
├── nassau_candy_cleaned.csv           # Processed dataset
├── nassau_streamlit_app.py            # Streamlit dashboard application
├── README.md                          # Project documentation
```

---

## 🎯 Objectives

The project aims to:

* Analyze sales and profitability performance.
* Identify top-performing products.
* Evaluate division-wise contributions.
* Measure gross margins and cost efficiency.
* Detect low-margin products.
* Generate actionable business recommendations.

---

## 📊 Dataset Information

### Dataset Size

| Attribute         | Value        |
| ----------------- | ------------ |
| Number of Rows    | 10,194       |
| Number of Columns | 26           |
| Time Period       | FY 2024–2025 |

---

## Dataset Features

### Order Information

* Order ID
* Order Date
* Ship Date
* Ship Mode

### Customer Information

* Customer ID

### Geographic Information

* Country
* State
* City
* Region

### Product Information

* Product ID
* Product Name
* Division

### Financial Information

* Sales
* Cost
* Gross Profit

### Engineered Features

* Gross Margin (%)
* Profit per Unit ($)
* Revenue per Unit ($)
* Cost per Unit ($)
* Year
* Month
* Month Name
* Quarter

---

# ⚙ Data Cleaning and Preprocessing

The script **clean_nassau_candy.py** performs the following operations:

### 1. Date Standardization

Converts:

```python
DD-MM-YYYY
```

to

```python
YYYY-MM-DD
```

for:

* Order Date
* Ship Date

---

### 2. Product Name Correction

Corrects:

```python
Wonka Bar -Scrumdiddlyumptious
```

to:

```python
Wonka Bar - Scrumdiddlyumptious
```

---

### 3. Feature Engineering

#### Gross Margin (%)

```python
Gross Margin (%) = (Gross Profit / Sales) × 100
```

#### Profit per Unit

```python
Profit per Unit = Gross Profit / Units
```

#### Revenue per Unit

```python
Revenue per Unit = Sales / Units
```

#### Cost per Unit

```python
Cost per Unit = Cost / Units
```

---

### 4. Calendar Features

Extracted from Order Date:

* Year
* Month
* Month Name
* Quarter

---

# 📈 Exploratory Data Analysis

## Overall Performance

| Metric             |       Value |
| ------------------ | ----------: |
| Total Revenue      | $141,783.63 |
| Total Cost         |  $48,340.83 |
| Total Gross Profit |  $93,442.80 |
| Units Sold         |      38,654 |

---

## Division-wise Revenue and Profit

| Division  |     Revenue | Gross Profit |
| --------- | ----------: | -----------: |
| Chocolate | $131,692.90 |   $88,824.62 |
| Other     |   $9,663.25 |    $4,333.45 |
| Sugar     |     $427.48 |      $284.73 |

---

## Top Products by Gross Profit

1. Wonka Bar – Scrumdiddlyumptious
2. Wonka Bar – Triple Dazzle Caramel
3. Wonka Bar – Milk Chocolate
4. Wonka Bar – Nutty Crunch Surprise
5. Wonka Bar – Fudge Mallows

---

## Highest Margin Products

* Everlasting Gobstopper
* Hair Toffee
* Wonka Bar – Nutty Crunch Surprise
* Wonka Bar – Scrumdiddlyumptious
* Wonka Bar – Fudge Mallows

---

# 📉 Dashboard Features

The Streamlit dashboard consists of four analytical sheets.

---

## Sheet 1 – Gross Margin Analysis

### Visualization

* Bar Chart
* Donut Chart
* Product Summary Table

### Purpose

* Compare product profitability.
* Identify high-margin products.

---

## Sheet 2 – Cost vs Sales Analysis

### Visualization

* Scatter Plot
* COGS Percentage Chart
* Risk Table

### Purpose

* Detect low-margin products.
* Analyze cost efficiency.

---

## Sheet 3 – Division Performance

### Visualization

* Grouped Bar Chart
* Donut Chart

### Purpose

* Compare divisions.
* Measure gross profit contribution.

---

## Sheet 4 – Profit per Unit Heatmap

### Visualization

* Heatmap
* Pivot Table

### Purpose

* Evaluate product profitability.
* Identify risky products.

---

# 💡 Key Insights

### Chocolate Division Dominates

Approximately 94% of revenue comes from chocolate products.

---

### Wonka Products are Major Revenue Drivers

Wonka product variants contribute the highest profits.

---

### High Margin Products Exist

Products such as:

* Everlasting Gobstopper
* Hair Toffee
* Nutty Crunch Surprise

generate exceptionally high margins.

---

### Cost Efficiency Drives Profitability

Lower Cost of Goods Sold (COGS) percentages correspond to higher gross margins.

---

# 📌 Business Recommendations

### Focus on High-Profit Products

Increase:

* Inventory
* Marketing efforts
* Shelf visibility

for:

* Scrumdiddlyumptious
* Triple Dazzle Caramel
* Milk Chocolate
* Nutty Crunch Surprise

---

### Expand High-Margin Products

Products with margins above 70% should receive:

* Promotional support
* Wider distribution
* Priority stocking

---

### Optimize Costs

Monitor:

* Production costs
* Procurement costs
* Transportation expenses

to improve profitability.

---

### Review Low-Contributing Divisions

The Sugar division contributes minimally and should be reassessed.

---

# 🛠 Technologies Used

* Python
* Pandas
* NumPy
* Streamlit
* Plotly
* Tableau
* Data Visualization
* Exploratory Data Analysis (EDA)

---

# ▶ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/nassau-candy-analysis.git
```

Install dependencies:

```bash
pip install pandas numpy streamlit plotly
```

Run the data cleaning script:

```bash
python clean_nassau_candy.py
```

Launch the dashboard:

```bash
streamlit run nassau_streamlit_app.py
```

---

# Future Enhancements

* Sales Forecasting
* Customer Segmentation
* Market Basket Analysis
* Recommendation Systems
* Machine Learning Models
* Predictive Analytics

---

# Author

**Asmit Das**

Data Analytics Project – Nassau Candy Distributor

---

## License

This project is intended for educational and portfolio purposes.

