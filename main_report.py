import sys
from antlr4 import *
import pandas as pd 
import json 
import operator
import matplotlib.pyplot as plt 

# Mapping operator string ke fungsi Python
OP_MAP = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

# Mapping untuk mengonversi fungsi DSL ke fungsi Pandas yang benar
AGG_FUNCTION_MAP = {
    'SUM': 'sum',
    'COUNT': 'count',
    'AVERAGE': 'mean',
    'MAX': 'max',
    'MIN': 'min'
}

from parser_output.ReportDSLLexer import ReportDSLLexer
from parser_output.ReportDSLParser import ReportDSLParser
from parser_output.ReportProcessor import ReportProcessor 

# --- DATA DUMMY ---
DUMMY_DATA = [
    {"region": "West", "amount": 1200, "date": "2023-11-01", "cost": 500, "units": 10},
    {"region": "West", "amount": 2000, "date": "2023-11-10", "cost": 600, "units": 15},
    {"region": "East", "amount": 800, "date": "2023-11-05", "cost": 400, "units": 5},
    {"region": "East", "amount": 1500, "date": "2023-11-15", "cost": 700, "units": 10},
    {"region": "North", "amount": 500, "date": "2023-11-20", "cost": 300, "units": 4},
    {"region": "North", "amount": 3000, "date": "2023-11-25", "cost": 1200, "units": 20},
    {"region": "South", "amount": 400, "date": "2023-11-28", "cost": 250, "units": 2},
    {"region": "South", "amount": 2500, "date": "2023-12-01", "cost": 800, "units": 18},
    {"region": "Central", "amount": 1100, "date": "2023-12-05", "cost": 450, "units": 8},
    {"region": "Central", "amount": 2200, "date": "2023-12-10", "cost": 900, "units": 15},
    {"region": "SouthEast", "amount": 1500, "date": "2023-12-15", "cost": 500, "units": 12},
    {"region": "SouthEast", "amount": 900, "date": "2023-12-20", "cost": 300, "units": 6},
    {"region": "West", "amount": 1800, "date": "2023-12-05", "cost": 550, "units": 12},
    {"region": "East", "amount": 950, "date": "2023-12-10", "cost": 450, "units": 6},
    {"region": "North", "amount": 1100, "date": "2023-12-15", "cost": 400, "units": 8},
    {"region": "West", "amount": 3500, "date": "2023-12-20", "cost": 1000, "units": 25},
    {"region": "South", "amount": 1600, "date": "2023-12-25", "cost": 600, "units": 10},
    {"region": "East", "amount": 2800, "date": "2023-12-28", "cost": 1100, "units": 22},
    {"region": "West", "amount": 900, "date": "2024-01-05", "cost": 350, "units": 5},
    {"region": "North", "amount": 150, "date": "2024-01-10", "cost": 50, "units": 1},
    {"region": "South", "amount": 3200, "date": "2024-01-15", "cost": 1500, "units": 30},
    {"region": "East", "amount": 1000, "date": "2024-01-20", "cost": 300, "units": 7},
    {"region": "Central", "amount": 1400, "date": "2024-01-25", "cost": 500, "units": 10}, 
    {"region": "SouthEast", "amount": 2100, "date": "2024-01-30", "cost": 750, "units": 18}, 
    {"region": "West", "amount": 700, "date": "2024-01-25", "cost": 200, "units": 4},
]

def apply_filter(df, filter_config):
    """Menerapkan satu kriteria filter pada DataFrame."""
    col = filter_config['column']
    op = filter_config['operator']
    val = filter_config['value']
    val_type = filter_config['value_type']
    
    if val_type == 'number':
        try:
            val = float(val)
        except ValueError:
            print(f"🚨 WARNING: Nilai filter '{val}' bukan angka valid.")
            return df

    try:
        if op == '=':
            df = df[df[col] == val]
        elif op == '>':
            df = df[df[col] > val]
        elif op == '<':
            df = df[df[col] < val]
        elif op == '>=':
            df = df[df[col] >= val]
        elif op == '<=':
            df = df[df[col] <= val]
        elif op == '!=':
            df = df[df[col] != val]
        
        print(f"  -> Data Difilter: {col} {op} {val}. Sisa {len(df)} baris.")
        return df
        
    except KeyError:
        print(f"🚨 WARNING: Kolom filter '{col}' tidak ditemukan di data.")
        return df 
    except TypeError:
        print(f"🚨 WARNING: Kesalahan tipe data saat membandingkan kolom '{col}'.")
        return df

def process_data(config):
    """Menerapkan logika agregasi, kalkulasi, dan layout dari DSL."""
    
    df = pd.DataFrame(DUMMY_DATA)
    processed_df = df.copy() 
    total_aggregates = {}
    
    # 1. Filtering
    filter_configs = config.get('filter', [])
    for f_config in filter_configs:
        processed_df = apply_filter(processed_df, f_config)
    
    if processed_df.empty:
        print("  -> Hasil Filtering menghasilkan DataFrame kosong.")
        return pd.DataFrame(), pd.DataFrame()
        
    df_for_agg = processed_df.copy()
    df_aggregated = pd.DataFrame() 
    
    group_agg_id = None 
    group_by_col_name = None 

    # 2. Agregasi
    for agg in config['aggregates']:
        target_col = agg['column']
        agg_id = agg['id']
        
        function = AGG_FUNCTION_MAP.get(agg['function'], agg['function'].lower()) 
        group_by = agg['group_by']

        if group_by:
            aggregation_result = df_for_agg.groupby(group_by)[target_col].agg(function).reset_index()
            aggregation_result.rename(columns={target_col: agg_id}, inplace=True)
            
            group_agg_id = agg_id
            group_by_col_name = group_by

            if df_aggregated.empty:
                df_aggregated = aggregation_result.copy() 
            else:
                df_aggregated = pd.merge(df_aggregated, aggregation_result, on=group_by, how='outer')


        elif not group_by:
            total = df_for_agg[target_col].agg(function)
            total_aggregates[agg_id] = total
            print(f"  -> Total Dihitung ({agg_id}): {total}")
    
    if not df_aggregated.empty:
        processed_df = df_aggregated
    elif not total_aggregates:
        print("  -> Tidak ada Agregasi Group By yang ditemukan.")
        return pd.DataFrame(), pd.DataFrame()
        
    # 2.5. Calculated Columns
    print("\n  -> Menerapkan Calculated Columns:")
    for calc in config['calculations']:
        calc_id = calc['id']
        op1 = calc['op1']
        op = calc['operator']
        op2 = calc['op2']
        
        op_func = OP_MAP.get(op)
        if not op_func:
            print(f"     [FAIL] Operator '{op}' tidak didukung.")
            continue
            
        try:
            op2_is_col = op2 in processed_df.columns
            
            if op2_is_col:
                processed_df[calc_id] = op_func(processed_df[op1], processed_df[op2])
                print(f"     [OK] {calc_id} = {op1} {op} {op2}")
            else:
                op2_val = float(op2)
                processed_df[calc_id] = op_func(processed_df[op1], op2_val)
                print(f"     [OK] {calc_id} = {op1} {op} {op2_val}")

        except ValueError:
            print(f"     [FAIL] Operand kanan '{op2}' bukan ID kolom yang valid atau nilai numerik.")
            continue
        except KeyError as e:
            print(f"     [FAIL] Kolom {e} tidak ditemukan di hasil agregasi untuk kalkulasi.")
            continue


    # 3. Layout dan Pembersihan (Filtering kolom)
    final_columns_ids = [col['id'] for col in config['layout']['columns']]
    
    try:
        report_df = processed_df[final_columns_ids].copy()
    except KeyError as e:
        print(f"\n🚨 ERROR: Kolom output {e} tidak ditemukan di hasil pemrosesan. (Cek BR-103)")
        return pd.DataFrame(), pd.DataFrame() 

    # 4. Sorting
    sort_config = config['layout']['sort']
    if sort_config:
        report_df.sort_values(
            by=sort_config['column'], 
            ascending=(sort_config['direction'] == 'ASC'), 
            inplace=True
        )

    # 5. Mengganti nama kolom sesuai label dan formatting
    label_map = {col_spec['id']: col_spec['label'] for col_spec in config['layout']['columns']}
    format_map = {col_spec['label']: col_spec['format'] for col_spec in config['layout']['columns'] if col_spec['format']}
            
    report_df.rename(columns=label_map, inplace=True)
    
    report_df_unformatted = report_df.copy() 
    
    # 5.5. Formatting Kolom
    for col_label, fmt in format_map.items():
        if report_df[col_label].dtype in ['int64', 'float64']:
            if fmt == "CURRENCY":
                report_df[col_label] = report_df[col_label].apply(lambda x: f"Rp {x:,.0f}") 
            elif fmt == "DECIMAL_2":
                report_df[col_label] = report_df[col_label].apply(lambda x: f"{x:,.2f}")
    
    # 6. Tambahkan total aggregates
    if total_aggregates:
        target_label = label_map.get(group_agg_id) 

        default_agg_id = 'GrandTotal' 
        agg_id_to_show = default_agg_id if default_agg_id in total_aggregates else next(iter(total_aggregates), None)

        if agg_id_to_show and target_label and target_label in report_df.columns: 
            
            total_val = total_aggregates[agg_id_to_show]
            total_row = {col: '' for col in report_df.columns}
            val_to_format = float(total_val)
            formatted_val = total_val
            
            if target_label in format_map:
                fmt = format_map[target_label]
                if fmt == "CURRENCY":
                    formatted_val = f"Rp {val_to_format:,.0f}"
                elif fmt == "DECIMAL_2":
                    formatted_val = f"{val_to_format:,.2f}"
                    
            total_row[target_label] = formatted_val
                    
            report_df.loc[len(report_df)] = total_row 
            report_df.loc[len(report_df) - 1, report_df.columns[0]] = f"TOTAL ({agg_id_to_show})"
        elif total_aggregates:
             print(f"🚨 WARNING: Total agregat ({agg_id_to_show}) dihitung, tetapi kolom target '{target_label}' tidak ditemukan di Layout.")
            
    return report_df, report_df_unformatted 

def clean_data_for_chart(df, col_name):
    """Menghapus simbol format (Rp, koma) dan mengkonversi ke float."""
    try:
        df_clean = df.copy() 
        
        col_series = df_clean[col_name].astype(str)
        cleaned_series = col_series.str.replace('Rp ', '', regex=False).str.replace(',', '', regex=False)
        return cleaned_series.astype(float)
    except Exception as e:
        print(f"🚨 ERROR saat membersihkan data chart: {e}. Pastikan kolom numerik berada di posisi kedua LAYOUT.")
        return None

def display_chart(df_unformatted, config):
    """Membuat diagram dan menyimpan file PNG."""
    layout_type = config['layout']['type']
    report_id = config['header']['id']
    
    if df_unformatted.shape[1] < 2:
        print("🚨 ERROR: Diagram memerlukan setidaknya dua kolom (Kategori dan Nilai).")
        return
        
    category_col = df_unformatted.columns[0]
    value_col = df_unformatted.columns[1]

    data = clean_data_for_chart(df_unformatted, value_col)
    
    labels = df_unformatted[category_col] 

    if data is None:
        return

    plt.figure(figsize=(10, 6))

    if layout_type == 'CHART_BAR':
        plt.bar(labels, data)
        title = f"Diagram Batang: {config['header']['title']} ({value_col} per {category_col})"
        plt.title(title)
        plt.xlabel(category_col)
        plt.ylabel(value_col)
        plt.xticks(rotation=45, ha='right')
    
    elif layout_type == 'CHART_PIE':
        plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
        title = f"Diagram Lingkaran: {config['header']['title']} ({value_col} Distribution)"
        plt.title(title)
        plt.axis('equal') 
        
    plt.tight_layout()
    
    # Menyimpan diagram sebagai file PNG
    output_filename = f"{report_id}_{layout_type.lower()}.png"
    plt.savefig(output_filename) 
    print(f"\n✅ Diagram berhasil dibuat dan disimpan sebagai: {output_filename}")

def run_report_dsl(file_path):
    
    # Parsing ANTLR
    try:
        input_stream = FileStream(file_path)
    except FileNotFoundError:
        print(f"❌ ERROR: File input '{file_path}' tidak ditemukan.")
        return

    lexer = ReportDSLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ReportDSLParser(stream)
    tree = parser.report_definition()
    
    if parser.getNumberOfSyntaxErrors() > 0:
        print("\n❌ Parsing GAGAL! Periksa sintaks DSL Anda.")
        return

    #Ekstraksi Konfigurasi
    processor = ReportProcessor()
    processor.visit(tree) 
    
    config_data = processor.config
    json_file_path = f"{config_data['header']['id']}_config.json"
    
    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4)
        print(f"\n✅ Ekstraksi Konfigurasi Berhasil. Konfigurasi tersimpan di: {json_file_path}")
    except Exception as e:
        print(f"❌ Gagal menulis file JSON: {e}")
        return

    if processor.errors:
        print("\n❌ Parsing Berhasil, TAPI GAGAL DALAM SEMANTIC CHECK:")
        for error in processor.errors:
            print(f"   -> {error}")
        return
    
    print("\n✅ Semantic Check Berhasil. Menjalankan Logika Laporan ...")
    
    # Pemrosesan Data Nyata
    result = process_data(processor.config)
    
    # Safety Check: Pastikan result adalah tuple dari dua DataFrames
    if not isinstance(result, tuple) or result[0].empty:
        print("Laporan Kosong atau terjadi Error saat Pemrosesan Data.")
        return
    
    final_report, final_report_unformatted = result
    
    # --- OUTPUT ---
    
    # 1. Tampilan Tabel di Konsol
    print(f"\n--- LAPORAN AKHIR (Tabel): {processor.config['header']['title']} ---")
    print(final_report.to_markdown(index=False)) 

    # 2. Tampilan Chart (Menyimpan file PNG)
    if processor.config['layout']['type'] in ['CHART_BAR', 'CHART_PIE']:
        display_chart(final_report_unformatted, processor.config)

if __name__ == "__main__":
    run_report_dsl('test_report.rdsl')