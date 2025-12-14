### Report-DSL


📊 Report DSL – Transform Your Data into Insightful Reports in Minutes, Not Hours!
<div align="center">
https://img.shields.io/badge/Report_DSL-Business_Intelligence_Simplified-blue
https://img.shields.io/badge/Python-3.8+-green
https://img.shields.io/badge/License-MIT-yellow
https://img.shields.io/badge/Powered_by-ANTLR4-orange
</div>

Stop writing complex reporting code. Start declaring what you want, not how to get it.
#🚀 Features
- Declarative Syntax – Write reports using a clear, English-like structure

- Data Aggregation – Support for SUM, COUNT, AVERAGE, MAX, MIN with GROUP BY

- Calculated Columns – Create new columns using arithmetic expressions

- Flexible Filtering – Apply conditional filters on columns

- Multiple Output Formats – Generate tables, bar charts, or pie charts

- Semantic Validation – Built-in checks for data type consistency and reference integrity

- Extensible – Designed to work with different data sources (SQL, CSV, etc.)

#🎯 The Problem Every Business Faces
"Our analysts spend 70% of their time writing and debugging SQL/Python reports instead of analyzing data."

Sound familiar? You have data in databases, spreadsheets, or APIs. You need:

-Daily sales dashboards

-Monthly performance reports

-Regional comparisons

-Executive summaries

-But each report requires:

-Complex SQL queries

-Python/Pandas scripting

-Formatting headaches

-Chart customization

-Endless debugging

Time wasted: 2-5 days per report.

#💡 The Solution: Report DSL
Report DSL is a business-friendly language that lets you define reports in plain English, while generating production-ready outputs automatically.

📖 DSL Syntax Example
```
REPORT Regional_Sales_Complex TITLE "Sales Analysis Report";

DATA_SOURCE GlobalSales: TYPE SQL_DB QUERY "SELECT region, amount, cost, units, date FROM all_sales";

FILTER {
    date <= "2023-12-31";
    units >= 10;
}

AGGREGATE TotalRevenue SUM(amount) GROUP_BY region;
AGGREGATE TotalUnits SUM(units) GROUP_BY region;
AGGREGATE AvgSalePrice AS TotalRevenue / TotalUnits;

LAYOUT CHART_BAR {
    COLUMN region AS "Sales Region";
    COLUMN TotalRevenue AS "Total Revenue" FORMAT "CURRENCY";
    COLUMN AvgSalePrice AS "Average Price" FORMAT "DECIMAL_2";
    SORT_BY TotalRevenue DESC;
}
```
Output (What You Get Automatically):
Table Output:
```
Sales Territory     Revenue       # Customers   Avg Value per Customer
---------------     -------       -----------   ----------------------
North America       $1,250,000    1,250        $1,000
Europe              $890,000      920          $967
Asia Pacific        $740,000      850          $870
TOTAL               $2,880,000    
```

##🔧 Getting Started in 5 Minutes

Step 1: Install
```
pip install report-dsl
```
Step 2: Write Your First Report
```
REPORT MyFirstReport TITLE "My First DSL Report";
DATA_SOURCE Sales: TYPE CSV PATH "sales_data.csv";
AGGREGATE Total SUM(amount) GROUP_BY region;
LAYOUT TABLE_VIEW {
    COLUMN region AS "Region";
    COLUMN Total AS "Total Sales";
}
```
Step 3: Generate
```
report-dsl generate sales_report.rdsl
```

#🚀 Why Your Team Will Love Report DSL
✅ For Business Analysts
*No coding needed – Write reports like writing requirements

*Fast iteration – Change a line, regenerate in seconds

*Self-documenting – The DSL IS the documentation

*Consistent outputs – Same formatting across all reports

✅ For IT/Development Teams
*Reduced maintenance – One DSL engine, infinite reports

*Separation of concerns – Analysts define logic, developers maintain infrastructure

*Standardization – Enforce business rules at language level

*Extensible – Connect to any data source (SQL, CSV, APIs)

✅ For Management
*Faster insights – Reports go from "request" to "delivered" in minutes

*Lower costs – Reduce analyst hours by 60-80%

*Better quality – Built-in validation prevents errors

*Scalable – Add reports without adding developers

From that simple declaration, you get:

*📊 Formatted table output

*📈 Professional bar chart (saved as PNG)

*🔢 Aggregated calculations

*🎨 Properly formatted currencies

*📋 Sorted, clean data presentation

#📋 Feature Highlights for Business Users
✨ Intuitive Syntax
*Looks like English, not code

*Declarative – Say WHAT you want, not HOW to do it

*Natural flow – Filter → Aggregate → Calculate → Present

🛡️ Built-in Quality
*Automatic validation – Catch errors before running

*Consistent formatting – All reports follow company standards

*Data type checking – Prevent "apples vs oranges" mistakes

📊 Professional Outputs
*Multiple formats – Tables, bar charts, pie charts

*Automatic formatting – Currency, decimals, dates

*Sorting & filtering – Built into the language

*Export ready – PNG charts, formatted tables

🔌 Enterprise Ready
*Connect anywhere – SQL databases, CSV files, APIs

*Scalable – From 10 to 10,000 reports

*Version controllable – DSL files are plain text

*Collaborative – Teams can share and reuse report templates

#⭐ Why Developers Choose Report DSL
```
Technical Benefits:
architecture: "ANTLR4-powered DSL engine"
extensibility: "Plugin system for custom functions"
performance: "Pandas-backed data processing"
output: "Matplotlib charts, formatted tables"
validation: "Semantic checking with business rules"
integration: "REST API, CLI, Python library"
```

## 📋 DSL Feature Summary

| Feature | Syntax Example | Description |
|---------|---------------|-------------|
| **Report Header** | `REPORT SalesReport TITLE "Monthly Sales";` | Defines report ID and title |
| **Data Source** | `DATA_SOURCE Sales: TYPE SQL_DB QUERY "SELECT * FROM sales";` | Specifies data source type and query |
| **Filtering** | `date > "2024-01-01";` | Applies row-level conditions |
| **Aggregation** | `AGGREGATE TotalSales SUM(amount) GROUP_BY region;` | Performs SUM, COUNT, AVG, etc. |
| **Calculation** | `CALCULATE AvgPrice AS TotalRevenue / TotalUnits;` | Creates calculated columns |
| **Layout** | `LAYOUT TABLE_VIEW { ... }` | Defines output format (table/chart) |
| **Sorting** | `SORT_BY TotalRevenue DESC;` | Sorts output data |
| **Formatting** | `FORMAT "CURRENCY"` | Formats numbers as currency/decimal |

### 🛠 Supported Operations

| Category | Operators/Functions | Example | Output |
|----------|---------------------|---------|--------|
| **Aggregation** | SUM, COUNT, AVERAGE, MAX, MIN | `SUM(amount)` | Numeric total |
| **Comparison** | =, >, <, >=, <=, != | `units > 10` | Boolean filter |
| **Arithmetic** | +, -, *, / | `Revenue / Units` | Calculated value |
| **Layout Types** | TABLE_VIEW, CHART_BAR, CHART_PIE | `LAYOUT CHART_BAR` | Visual output |
| **Formatting** | CURRENCY, DECIMAL_2 | `FORMAT "CURRENCY"` | Rp 1,000,000 |

## 📖 Grammar Specification Summary

### 🏗️ Production Rules

| Rule | Syntax | Description | Example |
|------|--------|-------------|---------|
| **Report Definition** | `report_header data_source_block filter_block? aggregate_def* calculate_def* layout_block` | Complete report structure | - |
| **Report Header** | `REPORT ID TITLE STRING ';'` | Report ID and title | `REPORT Sales TITLE "Q1 Report";` |
| **Data Source** | `DATA_SOURCE ID COLON TYPE ID (PATH \| QUERY) STRING ';'` | Data source specification | `DATA_SOURCE db: TYPE SQL_DB QUERY "SELECT...";` |
| **Filter Block** | `FILTER '{' filter_expression+ '}'` | Filter expressions block | `FILTER { date > "2024-01-01"; }` |
| **Filter Expression** | `ID COMPARISON_OP (STRING \| NUMBER) ';'` | Single filter condition | `amount >= 1000;` |
| **Aggregate Definition** | `AGGREGATE ID AGG_FUNCTION '(' ID ')' (GROUP_BY ID)? ';'` | Aggregation function | `AGGREGATE total SUM(amount) GROUP_BY region;` |
| **Calculate Definition** | `CALCULATE ID AS calculation_expression ';'` | Calculated column | `CALCULATE profit AS revenue - cost;` |
| **Calculation Expression** | `ID ARITHMETIC_OP ID`<br>`\| ID ARITHMETIC_OP NUMBER` | Arithmetic operation | `revenue / units` |
| **Layout Block** | `LAYOUT LAYOUT_TYPE '{' layout_param+ '}'` | Output layout definition | `LAYOUT TABLE_VIEW { ... }` |
| **Layout Parameter** | `COLUMN ID AS STRING (FORMAT STRING)? ';'`<br>`\| SORT_BY ID DIRECTION_ID ';'` | Column or sort specification | `COLUMN region AS "Region";` |

### 🔤 Lexical Tokens

| Token Category | Values | Description | Example |
|----------------|--------|-------------|---------|
| **Keywords** | `REPORT, TITLE, DATA_SOURCE, TYPE, AGGREGATE, GROUP_BY, CALCULATE, LAYOUT, COLUMN, AS, SORT_BY, FILTER, FORMAT` | Reserved words | `REPORT`, `AGGREGATE` |
| **Aggregation Functions** | `SUM, COUNT, AVERAGE, MAX, MIN` | Statistical functions | `SUM(amount)` |
| **Layout Types** | `TABLE_VIEW, CHART_PIE, CHART_BAR` | Output visualization types | `LAYOUT CHART_BAR` |
| **Direction Identifiers** | `ASC, DESC` | Sort order | `SORT_BY revenue DESC` |
| **Source Types** | `PATH, QUERY` | Data source access methods | `TYPE SQL_DB QUERY` |
| **Comparison Operators** | `=, >, <, >=, <=, !=` | Filter comparison operators | `amount > 1000` |
| **Arithmetic Operators** | `+, -, *, /` | Calculation operators | `revenue - cost` |
| **Identifiers** | `[a-zA-Z_][a-zA-Z0-9_]*` | User-defined names | `region`, `Total_Sales_2024` |
| **Literals** | `STRING, NUMBER` | String and numeric values | `"West"`, `1000` |
| **Punctuation** | `:, ;, {, }` | Syntax separators | `;` (statement end) |



<div align="center">
Stop Writing Code. Start Generating Insights.
Get Started Now • View Examples • Join Community

Transform your reporting workflow today. Your analysts will thank you tomorrow.

</div>


CONTRIBUTORS: SalmanAAA, Cloviszion

