# Report-DSL
📌 Overview
The Report DSL is a custom language designed for creating business reports through a simple, declarative syntax. It allows users to define data sources, apply filters, perform aggregations, create calculated columns, and format output—all without writing complex code.

🚀 Features
Declarative Syntax – Write reports using a clear, English-like structure

Data Aggregation – Support for SUM, COUNT, AVERAGE, MAX, MIN with GROUP BY

Calculated Columns – Create new columns using arithmetic expressions

Flexible Filtering – Apply conditional filters on columns

Multiple Output Formats – Generate tables, bar charts, or pie charts

Semantic Validation – Built-in checks for data type consistency and reference integrity

Extensible – Designed to work with different data sources (SQL, CSV, etc.)

📖 DSL Syntax Example
```REPORT Regional_Sales_Complex TITLE "Sales Analysis Report";

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
}```

🧱 Grammar Summary
Block	Purpose
REPORT	Report header with ID and title
DATA_SOURCE	Defines data source (SQL, file, etc.)
FILTER	Applies row-level filters
AGGREGATE	Performs aggregation with optional grouping
CALCULATE	Creates calculated columns using arithmetic operations
LAYOUT	Defines output format (TABLE_VIEW, CHART_BAR, CHART_PIE) and sorting


🔧 Supported Operations
Aggregation Functions
SUM, COUNT, AVERAGE, MAX, MIN

Comparison Operators (Filtering)
=, >, <, >=, <=, !=

Arithmetic Operators (Calculations)
+, -, *, /

Layout Types
TABLE_VIEW – Tabular output

CHART_BAR – Bar chart visualization

CHART_PIE – Pie chart visualization

Formatting Options
CURRENCY – Formats numbers as currency (e.g., Rp 1,000,000)

DECIMAL_2 – Formats numbers with two decimal places

✅ Validation Rules
The DSL includes semantic checks to ensure report integrity:

Rule ID	Description
BR-102	Prevents grouping by an aggregate column
BR-103	Ensures layout columns are either aggregates, calculations, or group keys
BR-104	Validates that SQL data sources use QUERY instead of PATH
BR-106	Ensures calculated column operands are defined
BR-107	Validates numeric functions are applied to numeric columns
BR-108	Ensures group-by columns are displayed when aggregates are shown
🛠 Implementation
The DSL is built using:

ANTLR4 – For grammar definition and parsing

Python – Backend processing and data handling

Pandas – Data manipulation and aggregation

Matplotlib – Chart generation

Sample Workflow:
Write a .rdsl file with report definition

Parse using ANTLR-generated lexer/parser

Validate semantics using ReportProcessor

Process data with Pandas

Generate output (table + optional chart PNG)
