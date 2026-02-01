#!/usr/bin/env python3
import os
from datetime import datetime

def main():
    source_dir = r"C:\Users\Lenovo\Desktop\File Desktop\Arquivos Inicializacao 2026"
    output_report = "57-FILES-RAW-LIST.md"
    execution_log = "scan-execution-log.txt"
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    print("AURORA Trading System - RAW FILES SCAN")
    print("")
    
    if not os.path.isdir(source_dir):
        print("Directory not found: " + source_dir)
        return 1
    
    print("OK - Directory validated")
    print("")
    
    files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    file_count = len(files)
    print("Found: " + str(file_count) + " files")
    print("")
    
    total_lines = 0
    total_size = 0
    file_data = []
    lang_count = {}
    lang_lines = {}
    
    def detect_language(filename):
        ext = os.path.splitext(filename)[1].lower()
        mapping = {'.py': 'Python', '.mql5': 'MQL5', '.mq5': 'MQL5', '.mqh': 'MQH',
                   '.md': 'Markdown', '.sh': 'Bash', '.ps1': 'PowerShell',
                   '.json': 'JSON', '.yaml': 'YAML', '.yml': 'YAML',
                   '.env': 'ENV', '.txt': 'Text'}
        return mapping.get(ext, 'Unknown')
    
    print("Scanning files...")
    print("")
    
    for idx, filename in enumerate(sorted(files), 1):
        filepath = os.path.join(source_dir, filename)
        filesize = os.path.getsize(filepath)
        
        lines = 0
        try:
            if filename.endswith(('.py', '.sh', '.ps1', '.json', '.yaml', '.yml', '.md', '.txt', '.mq5', '.mql5')):
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = len(f.readlines())
        except:
            pass
        
        language = detect_language(filename)
        
        total_lines += lines
        total_size += filesize
        
        file_data.append({'filename': filename, 'language': language, 'lines': lines, 'size': filesize})
        
        if language not in lang_count:
            lang_count[language] = 0
            lang_lines[language] = 0
        lang_count[language] += 1
        lang_lines[language] += lines
        
        print("[" + str(idx).rjust(3) + "] " + filename + " (" + language + ", " + str(lines) + " lines)")
    
    print("")
    print("OK - Scan completed")
    print("")
    
    # Report
    report_lines = [
        "# AURORA Trading System - Raw Files Inventory",
        "",
        "Data de Scan: " + timestamp,
        "Diretorio Origem: " + source_dir,
        "Total de Arquivos: " + str(file_count),
        "Total de Linhas: " + str(total_lines),
        "Total de Tamanho (bytes): " + str(total_size),
        "",
        "---",
        "",
        "## PROTOCOLO TIER-0 - EVIDENCIA DETERMINISTICA",
        "",
        "Este relatorio contem lista NEUTRA de arquivos (SEM Tier automatico).",
        "",
        "### Por que NAO ha Tier automatico?",
        "",
        "Classificar criticidade baseado APENAS em nome de arquivo eh fundamentalmente errado.",
        "Exemplo: Knight Capital 2019 perdeu $440M por arquivo mal nomeado.",
        "",
        "---",
        "",
        "## Lista de Arquivos (Ordenada por Tamanho)",
        "",
        "| # | Arquivo | Linguagem | Linhas | Tamanho (bytes) |",
        "|---|---------|-----------|--------|-----------------|",
    ]
    
    file_data.sort(key=lambda x: x['size'], reverse=True)
    
    for idx, item in enumerate(file_data, 1):
        report_lines.append("| " + str(idx) + " | " + item['filename'] + " | " + item['language'] + " | " + str(item['lines']) + " | " + str(item['size']) + " |")
    
    report_lines.extend([
        "",
        "---",
        "",
        "## Estatisticas por Linguagem",
        "",
        "| Linguagem | Arquivos | Linhas Totais |",
        "|-----------|----------|---------------|",
    ])
    
    for lang in sorted(lang_count.keys()):
        report_lines.append("| " + lang + " | " + str(lang_count[lang]) + " | " + str(lang_lines[lang]) + " |")
    
    report_lines.extend([
        "",
        "---",
        "",
        "Gerado por: scan-57-files-NEUTRAL-REAL.py",
        "Status: OK - INVENTARIO COMPLETO",
        "Protocolo: OK - ZERO_ILLUSION_PROTOCOL",
    ])
    
    with open(output_report, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    # Log
    log_content = "AURORA Trading System - Execution Log\nTimestamp: " + timestamp + "\n"
    log_content += "Total de Arquivos: " + str(file_count) + "\nTotal de Linhas: " + str(total_lines) + "\n"
    log_content += "Total de Tamanho: " + str(total_size) + " bytes\n\n"
    log_content += "Distribuicao por linguagem:\n"
    for lang in sorted(lang_count.keys()):
        pct = (lang_count[lang] * 100) // file_count if file_count > 0 else 0
        log_content += "  " + lang + ": " + str(lang_count[lang]) + " arquivos (" + str(lang_lines[lang]) + " linhas, " + str(pct) + "%)\n"
    log_content += "\nOK - Script executado com seguranca Tier-0\n"
    
    with open(execution_log, 'w', encoding='utf-8') as f:
        f.write(log_content)
    
    # Summary
    print("=" * 60)
    print("SCAN RESULTADO - DETERMINISTICO")
    print("=" * 60)
    print("Total de Arquivos: " + str(file_count) + " (contagem REAL)")
    print("Total de Linhas: " + str(total_lines))
    print("Total de Tamanho (bytes): " + str(total_size))
    print("")
    print("Distribuicao por linguagem:")
    for lang in sorted(lang_count.keys()):
        pct = (lang_count[lang] * 100) // file_count if file_count > 0 else 0
        print("  " + lang + ": " + str(lang_count[lang]) + " arquivos (" + str(lang_lines[lang]) + " linhas, " + str(pct) + "%)")
    print("")
    print("OK - Relatorio gerado: " + output_report)
    print("OK - Log de execucao: " + execution_log)
    print("")
    print("=" * 60)
    print("OK - PROTOCOLO TIER-0: EVIDENCIA CAPTURADA")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    exit(main())
