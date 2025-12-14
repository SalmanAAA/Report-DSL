from .ReportDSLVisitor import ReportDSLVisitor
from .ReportDSLParser import ReportDSLParser
import json

class ReportProcessor(ReportDSLVisitor):
    # Skema Data Dummy 
    DATA_SCHEMA = {
        'region': 'STRING',
        'amount': 'NUMERIC',
        'date': 'STRING',
        'cost': 'NUMERIC',
        'units': 'NUMERIC',
    }
    
    def __init__(self):
        self.config = {
            "header": {},
            "data_source": {},
            "filter": [], 
            "aggregates": [],
            "calculations": [], 
            "layout": {"type": None, "columns": [], "sort": {}}
        }
        self.defined_ids = set(self.DATA_SCHEMA.keys())
        self.aggregate_ids = set()
        self.group_by_columns = {}
        self.errors = []
        self.layout_columns_set = set()

    # 1. Header
    def visitReport_header(self, ctx:ReportDSLParser.Report_headerContext):
        report_id = ctx.ID().getText() 
        title = ctx.STRING().getText().strip('"') 
        self.defined_ids.add(report_id)
        self.config['header'] = {'id': report_id, 'title': title}
        return self.visitChildren(ctx)

    # 2. Data Source
    def visitData_source_block(self, ctx:ReportDSLParser.Data_source_blockContext):
        source_id = ctx.ID(0).getText()
        source_type = ctx.ID(1).getText()
        query_path = ctx.STRING().getText().strip('"') 
        path_token = ctx.QUERY() if ctx.QUERY() else ctx.PATH()
        path_type = path_token.getText()
        
        if source_type == 'SQL_DB' and path_type != 'QUERY':
            self.errors.append(f"BR-104 Gagal: SQL_DB memerlukan QUERY, bukan {path_type}.")
        
        self.defined_ids.add(source_id)
        self.config['data_source'] = {'id': source_id, 'type': source_type, 'query_path': query_path}
        return self.visitChildren(ctx)

    # 3. Filter Block
    def visitFilter_expression(self, ctx:ReportDSLParser.Filter_expressionContext):
        col = ctx.ID().getText()
        op = ctx.COMPARISON_OP().getText()
        
        value = None
        if ctx.STRING():
            value = ctx.STRING().getText().strip('"')
            value_type = 'string'
        elif ctx.NUMBER():
            value = ctx.NUMBER().getText()
            value_type = 'number'
            
        self.config['filter'].append({
            'column': col,
            'operator': op,
            'value': value,
            'value_type': value_type
        })
        return self.visitChildren(ctx)
        
    # 4. Agregasi
    def visitAggregate_def(self, ctx:ReportDSLParser.Aggregate_defContext):
        agg_id = ctx.ID(0).getText()
        target_column = ctx.ID(1).getText()
        function = ctx.AGG_FUNCTION().getText()
        group_by_id = ctx.ID(2).getText() if ctx.ID(2) else None
        
        if function in ['SUM', 'AVERAGE', 'MAX', 'MIN']:
            if self.DATA_SCHEMA.get(target_column) != 'NUMERIC':
                self.errors.append(f"BR-107 Gagal: Fungsi {function} memerlukan kolom NUMERIC, tetapi kolom '{target_column}' adalah {self.DATA_SCHEMA.get(target_column, 'UNKNOWN')}.")

        if group_by_id and group_by_id in self.aggregate_ids:
            self.errors.append(f"BR-102 Gagal: Kolom '{group_by_id}' sudah menjadi hasil agregasi.")
        
        if group_by_id:
            self.group_by_columns[agg_id] = group_by_id
            
        self.aggregate_ids.add(agg_id)
        self.defined_ids.add(agg_id)
        
        agg = {
            'id': agg_id,
            'function': function,
            'column': target_column,
            'group_by': group_by_id
        }
        self.config['aggregates'].append(agg)
        return self.visitChildren(ctx)

    # 5. Calculated Column 
    def visitCalculate_def(self, ctx:ReportDSLParser.Calculate_defContext):        
        calc_id = ctx.ID().getText() 

        calc_expr_ctx = ctx.calculation_expression()
        
        op1 = calc_expr_ctx.ID()[0].getText()
        op = calc_expr_ctx.ARITHMETIC_OP().getText()
        
        op2_id_tokens = calc_expr_ctx.ID()
        op2_number_token = calc_expr_ctx.NUMBER()

        if len(op2_id_tokens) > 1:
            op2 = op2_id_tokens[1].getText()
        elif op2_number_token:
            op2 = op2_number_token.getText()
        else:
            self.errors.append(f"BR-106 Gagal: Operand kedua untuk CALCULATE '{calc_id}' tidak ditemukan.")
            return self.visitChildren(ctx)
            
        if op1 not in self.defined_ids:
            self.errors.append(f"BR-106 Gagal: Operand kiri '{op1}' di CALCULATE belum didefinisikan.")
        if op2.isalpha() and op2 not in self.defined_ids: 
            self.errors.append(f"BR-106 Gagal: Operand kanan '{op2}' di CALCULATE belum didefinisikan.")

        self.defined_ids.add(calc_id)
        self.config['calculations'].append({
            'id': calc_id,
            'op1': op1,
            'operator': op,
            'op2': op2
        })
        return self.visitChildren(ctx) 
    # 6. Layout Block
    def visitLayout_block(self, ctx:ReportDSLParser.Layout_blockContext):
        self.config['layout']['type'] = ctx.LAYOUT_TYPE().getText()
        self.config['layout']['columns'] = [] 
        self.config['layout']['sort'] = {}
        self.layout_columns_set = set() 
        return self.visitChildren(ctx)

    # 7. Layout Parameter 
    def visitLayout_param(self, ctx:ReportDSLParser.Layout_paramContext):
        
        if ctx.AS(): 
            col_id = ctx.ID().getText()
            
            group_keys = set(self.group_by_columns.values())
            
            is_agg_or_calc = col_id in self.aggregate_ids or col_id in [c['id'] for c in self.config['calculations']]
            is_group_by_key = col_id in group_keys
            
            if not is_agg_or_calc and not is_group_by_key:
                 self.errors.append(f"BR-103 Gagal: Kolom '{col_id}' di LAYOUT harus merupakan AGGREGATE ID, CALCULATED ID, atau GROUP BY KEY.")

            format_string = None
            if ctx.FORMAT() and len(ctx.STRING()) > 1:
                format_string = ctx.STRING(1).getText().strip('"') 
            
            self.config['layout']['columns'].append({
                'id': col_id,           
                'label': ctx.STRING(0).getText().strip('"'),
                'format': format_string
            })
            self.layout_columns_set.add(col_id) 
            
        elif ctx.SORT_BY(): 
            self.config['layout']['sort'] = {
                'column': ctx.ID().getText(),       
                'direction': ctx.DIRECTION_ID().getText()
            }
            
        return self.visitChildren(ctx)
        
    # 8. Post-Processing Check (BR-108)
    def visitReport_definition(self, ctx:ReportDSLParser.Report_definitionContext):
        for agg_id, group_by_id in self.group_by_columns.items():
            if agg_id in self.layout_columns_set and group_by_id not in self.layout_columns_set:
                 self.errors.append(f"BR-108 Gagal: Hasil agregasi '{agg_id}' ditampilkan, tetapi kolom GROUP BY-nya ('{group_by_id}') tidak ditampilkan di LAYOUT.")
                 
        return self.visitChildren(ctx)