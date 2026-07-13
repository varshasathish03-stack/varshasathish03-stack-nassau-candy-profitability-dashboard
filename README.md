# Project Overview
This project performs a comprehensive Exploratory Data Analysis (EDA) and profitability analysis on the Nassau Candy Distributor dataset. The objective is to transform raw transactional data into meaningful business insights and visualize product and division performance through an interactive dashboard.

The project includes:

Data cleaning and preprocessing
Feature engineering
Exploratory Data Analysis (EDA)
Profitability analysis
Risk analysis
Interactive Streamlit dashboard
Business insights and recommendations
## Project Structure
├── Nassau_Candy_Distributor.csv        # Raw dataset
├── clean_nassau_candy.py              # Data cleaning and feature engineering
├── nassau_candy_cleaned.csv           # Processed dataset
├── nassau_streamlit_app.py            # Streamlit dashboard application
├── README.md                          # Project documentation

## Dataset Information
| Column Name   | Data Type | Description             | 
| ------------- | --------- | ----------------------- | 
| Order_ID      | Integer   | Unique order identifier |
| Customer_ID   | String    | Unique customer ID      |
| Customer_Name | String    | Customer name           | 
| Product_ID    | String    | Product identifier      | 
| Product_Name  | String    | Product name            | 
| Category      | String    | Product category        | 
| Sub_Category  | String    | Product sub-category    |
| Order_Date    | Date      | Date of purchase        | 
| Ship_Date     | Date      | Shipping date           | 
| Region        | String    | Sales region            | 
| State         | String    | State name              | 
| City          | String    | City name               | 
| Quantity      | Integer   | Units sold              | 
| Unit_Price    | Decimal   | Price per unit          | 
| Discount      | Decimal   | Discount percentage     | 
| Sales         | Decimal   | Total sales amount      | 
| Profit        | Decimal   | Profit amount           | 


## Dataset Features
## Derived KPI Columns
## Order Information
  1. Order ID
  2. Order Date
  3. Ship Date
  4. Ship Mode

## Customer Information
  1. Customer ID
 
## Geographic Information
  1. Country
  2. State
  3. City
  4. Region

## Product Information
  1. Product ID
  2. Product Name
  3. Division

## Data Cleaning and Preprocessing
## 1. Date Standardization
Converts:
DD-MM-YYYY
to
YYYY-MM-DD
for:

Order Date
Ship Date

## 2. Product Name Correction
Corrects:

Wonka Bar -Scrumdiddlyumptious
to:

Wonka Bar - Scrumdiddlyumptious

## 3. Feature Engineering
## Gross Margin (%)
Gross Margin (%) = (Gross Profit / Sales) × 100
## Profit per Unit
Profit per Unit = Gross Profit / Units
## Revenue per Unit
Revenue per Unit = Sales / Units
## Cost per Unit
Cost per Unit = Cost / Units

## Exploratory Data Analysis
## Top Products by Gross Profit
1. Wonka Bar – Scrumdiddlyumptious
2. Wonka Bar – Triple Dazzle Caramel
3. Wonka Bar – Milk Chocolate
4. Wonka Bar – Nutty Crunch Surprise
5. Wonka Bar – Fudge Mallows

## Dashboard Features

## Sheet 1 – Gross Margin Analysis
## Visualization
Bar Chart
Donut Chart
Product Summary Table
## Purpose
Compare product profitability.
Identify high-margin products.

## Sheet 2 – Cost vs Sales Analysis
## Visualization
Scatter Plot
COGS Percentage Chart
Risk Table
## Purpose
Detect low-margin products.
Analyze cost efficiency.

## Sheet 3 – Division Performance
## Visualization
Grouped Bar Chart
Donut Chart
## Purpose
Compare divisions.
Measure gross profit contribution.

## Sheet 4 – Profit per Unit Heatmap
## Visualization
Heatmap
Pivot Table
## Purpose
Evaluate product profitability.
Identify risky products.











| KPI                  | Formula                               | Purpose                |
| -------------------- | ------------------------------------- | ---------------------- |
| Profit Margin        | Profit / Revenue ×100                 | Profit percentage      |
| Discount %           | Discount / Sales ×100                 | Discount analysis      |
| Revenue per Customer | Revenue / Customers                   | Customer value         |
| Monthly Growth %     | ((Current-Previous)/Previous)×100     | Growth analysis        |
| Customer Retention   | Returning Customers / Total Customers | Loyalty analysis       |

## Product-Factory Mapping
| Column       | Description          |
| ------------ | -------------------- |
| Product_ID   | Product key          |
| Product_Name | Product name         |
| Category     | Product category     |
| Sub_Category | Product sub-category |
| Brand        | Product brand        |
| Unit_Price   | Selling price        |
| Cost         | Manufacturing cost   |
| Profit       | Profit per product   |
| Supplier     | Supplier name        |
| Stock        | Available inventory  |

## KPI Formulas
| KPI                     | Formula                                                  |
| ----------------------- | -------------------------------------------------------- |
| Avg Order Value         | Revenue ÷ Orders                                         |
| Profit Margin           | (Profit ÷ Revenue) ×100                                  |
| Sales Growth            | ((Current Month - Previous Month) / Previous Month) ×100 |
| ROI                     | (Profit ÷ Investment) ×100                               |
| Customer Lifetime Value | Average Order × Purchase Frequency                       |
| Conversion Rate         | Purchases ÷ Visitors ×100                                |

## Project Structure


## Scripts Description
| File                   | Description                |
| ---------------------- | -------------------------- |
| data_cleaning.py       | Cleans raw dataset         |
| analysis.py            | Performs data analysis     |
| visualization.py       | Creates charts             |
| app.py                 | Main dashboard application |
| database.py            | Database connection        |
| requirements.txt       | Required packages          |
| README.md              | Project documentation      |

## Installation & Run
## Run
git clone https://github.com/varshasathish03-stack/nassau-candy-profitability-dashboard.git
cd nassau-candy-profitability-dashboard
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/clean_nassau_data.py
python scripts/nassau_eda_charts.py
python scripts/profitability_analysis.py
python scripts/generate_nassau_report.py
streamlit run app.py

Access: http://localhost:8501

## Run with Docker
## Requirements
| Package      | Purpose                   |
| ------------ | ------------------------- |
| pandas       | Data manipulation         |
| numpy        | Numerical operations      |
| matplotlib   | Charts                    |
| plotly       | Interactive visualization |
| seaborn      | Statistical graphs        |
| scikit-learn | Machine Learning          |
| streamlit    | Dashboard                 |
| sqlalchemy   | Database                  |
| pymysql      | MySQL connector           |
| openpyxl     | Excel support             |

## Tech Stack 
Python | pandas | numpy | matplotlib | seaborn | plotly | reportlab | 

## Author
[Varsha sathish] | Unified Mentor Internship | 2026




