grammar ReportDSL;

// ----------------------------------------------------
// PARSER RULES
// ----------------------------------------------------

// Urutan: Header -> Data Source -> Filter -> Aggregate -> Calculate -> Layout
report_definition : report_header data_source_block (filter_block)? (aggregate_def)* (calculate_def)* layout_block EOF;

// 1. HEADER
report_header : REPORT ID TITLE STRING ';';

// 2. DATA SOURCE
data_source_block : DATA_SOURCE ID COLON TYPE ID (PATH | QUERY) STRING ';';

// 3. FILTER
filter_block : FILTER '{' (filter_expression)+ '}' ;
filter_expression : ID COMPARISON_OP (STRING | NUMBER) ';';

// 4. AGGREGASI
aggregate_def : AGGREGATE ID AGG_FUNCTION '(' ID ')' (GROUP_BY ID)? ';';

// 5. CALCULATED COLUMN
calculate_def : CALCULATE ID AS calculation_expression ';';
calculation_expression : ID ARITHMETIC_OP ID
                       | ID ARITHMETIC_OP NUMBER
                       ;

// 6. LAYOUT
layout_block : LAYOUT LAYOUT_TYPE '{' (layout_param)+ '}' ;

layout_param : COLUMN ID AS STRING (FORMAT STRING)? ';'
             | SORT_BY ID DIRECTION_ID ';'
             ;

// ----------------------------------------------------
// LEXER KEYWORDS
// ----------------------------------------------------

REPORT : 'REPORT';
TITLE : 'TITLE';
DATA_SOURCE : 'DATA_SOURCE';
TYPE : 'TYPE';
AGGREGATE : 'AGGREGATE';
GROUP_BY : 'GROUP_BY';
CALCULATE : 'CALCULATE'; 
LAYOUT : 'LAYOUT';
COLUMN : 'COLUMN';
AS : 'AS';
SORT_BY : 'SORT_BY';
FILTER : 'FILTER';
FORMAT : 'FORMAT';

// Token dengan daftar pilihan
AGG_FUNCTION : 'SUM' | 'COUNT' | 'AVERAGE' | 'MAX' | 'MIN';
DIRECTION_ID : 'ASC' | 'DESC';
LAYOUT_TYPE : 'TABLE_VIEW' | 'CHART_PIE' | 'CHART_BAR';
PATH : 'PATH';
QUERY : 'QUERY';

// Operator
COMPARISON_OP : '=' | '>' | '<' | '>=' | '<=' | '!=';
ARITHMETIC_OP : '+' | '-' | '*' | '/';

// ----------------------------------------------------
// LEXER PRIMITIVES
// ----------------------------------------------------

ID : [a-zA-Z_] [a-zA-Z0-9_]*;
STRING : '"' ( '\\' . | ~["\r\n] )* '"';
NUMBER : [0-9]+;

COLON : ':';
SEMI : ';';

WS : [ \t\r\n]+ -> skip;