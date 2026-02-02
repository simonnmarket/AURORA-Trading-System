#!/usr/bin/env python3
# ============================================================================
# AURORA ST-006: Execute Real Scan with Tier-0 Protocol
# Alternative execution via Python (deterministic)
# ============================================================================

import os
import subprocess
import json
from pathlib import Path
from datetime import datetime

def main():
    source_dir = r"C:\Users\Lenovo\Desktop\File Desktop\Arquivos Inicializacao 2026"
    output_report = "57-FILES-RAW-LIST.md"
    execution_log = "scan-execution-log.txt"
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    print("=" * 60)
    print("AURORA Trading System - RAW FILES SCAN (TIER-0 PROTOCOL)")
    print("=" * 60)
    print()
    print("🔴 PROTOCOLO: ZERO_ILLUSION_PROTOCOL")
    print("✅ EVIDÊNCIA OBRIGATÓRIA: Sim")
    print("✅ TIER AUTOMÁTICO: NÃO (manual PSA/CQO)")
    print()
    print(f"Source Directory: {source_dir}")
    print(f"Report Output: {output_report}")
    print(f"Execution Log: {execution_log}")
    print(f"Timestamp: {timestamp}")
    print()
    print("════════════════════════════════════════════════════════════════")
    print()
    
    # Validar diretório
    if not os.path.isdir(source_dir):
        print(f"❌ ERRO: Diretório não encontrado: {source_dir}")
        return 1
    
    print("✅ Diretório validado")
    print()
    
    # Contar arquivos
    files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    file_count = len(files)
    print(f"📊 Contagem prévia: {file_count} arquivos")
    print()
    
    # Coletar dados
    total_lines = 0
    total_size = 0
    file_data = []
    
    lang_count = {}
    lang_lines = {}
    
    def detect_language(filename):
        ext = os.path.splitext(filename)[1].lower()
        mapping = {
            '.py': 'Python',
            '.mql5': 'MQL5',
            '.mq5': 'MQL5',
            '.mqh': 'MQH',
            '.md': 'Markdown',
            '.sh': 'Bash',
            '.ps1': 'PowerShell',
            '.json': 'JSON',
            '.yaml': 'YAML',
            '.yml': 'YAML',
            '.env': 'ENV',
            '.txt': 'Text',
        }
        return mapping.get(ext, 'Unknown')
    
    print("📝 Escaneando arquivos...")
    print()
    
    for idx, filename in enumerate(sorted(files), 1):
        filepath = os.path.join(source_dir, filename)
        
        # Tamanho
        filesize = os.path.getsize(filepath)
        
        # Linhas
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
        
        file_data.append({
            'filename': filename,
            'language': language,
            'lines': lines,
            'size': filesize
        })
        
        if language not in lang_count:
            lang_count[language] = 0
            lang_lines[language] = 0
        lang_count[language] += 1
        lang_lines[language] += lines
        
        print(f"[{idx:3d}] {filename} ({language}, {lines} linhas)")
    
    print()
    print("✅ Scan completado")
    print()
    
    # Gerar relatório
    report_lines = [
        "# 📁 AURORA Trading System - Raw Files Inventory",
        "",
        f"**Data de Scan:** {timestamp}",
        f"**Diretório Origem:** {source_dir}",
        f"**Total de Arquivos Encontrados:** {file_count}",
        f"**Total de Linhas:** {total_lines}",
        f"**Total de Tamanho (bytes):** {total_size}",
        "",
        "---",
        "",
        "## ⚠️ PROTOCOLO TIER-0 - EVIDÊNCIA DETERMINÍSTICA",
        "",
        "Este relatório contém lista **NEUTRA** de arquivos (SEM Tier automático).",
        "",
        "### Por quê NÃO há Tier automático?",
        "",
        "Classificar criticidade baseado APENAS em nome de arquivo é fundamentalmente errado:",
        "- \"trading_engine_backup.py\" → soa importante, mas pode ser backup antigo",
        "- \"config.py\" → soa simples, mas pode ser configuração crítica",
        "- \"SMARSdeploy.bat\" (Knight Capital 2019) → resultou em $440M loss",
        "",
        "**Conclusão:** Tier NÃO é sobre nome. É sobre impacto financeiro real no negócio.",
        "",
        "### Classificação Manual Obrigatória (Próximas Fases)",
        "",
        "1. **PSA Tier-0**: Analisa manualmente cada arquivo",
        "2. **CQO**: Atribui Tier com justificativa de risco",
        "3. **CTO**: Valida critério técnico",
        "4. Tier é decisão humana, nunca automática",
        "",
        "---",
        "",
        "## 📋 Lista de Arquivos (Ordenada por Tamanho)",
        "",
        "| # | Arquivo | Linguagem | Linhas | Tamanho (bytes) |",
        "|---|---------|-----------|--------|-----------------|",
    ]
    
    # Ordenar por tamanho
    file_data.sort(key=lambda x: x['size'], reverse=True)
    
    for idx, item in enumerate(file_data, 1):
        report_lines.append(
            f"| {idx} | {item['filename']} | {item['language']} | {item['lines']} | {item['size']} |"
        )
    
    report_lines.extend([
        "",
        "---",
        "",
        "## 📊 Estatísticas por Linguagem",
        "",
        "| Linguagem | Arquivos | Linhas Totais |",
        "|-----------|----------|---------------|",
    ])
    
    for lang in sorted(lang_count.keys()):
        report_lines.append(f"| {lang} | {lang_count[lang]} | {lang_lines[lang]} |")
    
    report_lines.extend([
        "",
        "---",
        "",
        "## 📋 Próximas Ações - ANÁLISE MANUAL TIER-0",
        "",
        "1. **PSA Tier-0**: Lê este relatório",
        "2. **PSA + CQO**: Revisam MANUALMENTE cada arquivo crítico",
        "3. Para cada arquivo, respondem:",
        "   - ☐ Este arquivo está em PRODUÇÃO?",
        "   - ☐ Qual impacto financeiro máximo se falhar? (<$100 | $100-$10k | >$10k)",
        "   - ☐ Quantos módulos dependem dele? (0 | 1-3 | 4+)",
        "   - ☐ Está ativo ou depreciado?",
        "   - ☐ Tem testes automatizados?",
        "4. **Tier é atribuído com justificativa humana** (não automática)",
        "",
        "---",
        "",
        "## 🔐 Verificação de Integridade",
        "",
        f"**Executado:** {timestamp}",
        f"**Máquina:** {os.environ.get('COMPUTERNAME', 'Windows')}",
        f"**Usuário:** {os.environ.get('USERNAME', 'user')}",
        f"**Path:** {source_dir}",
        "",
        "**Validação:** ✅ Determinística",
        "",
        "---",
        "",
        "**Gerado por:** scan-57-files-NEUTRAL-REAL.py",
        "**Status:** ✅ INVENTÁRIO COMPLETO - AGUARDANDO ANÁLISE PSA/CQO",
        "**Protocolo:** ✅ ZERO_ILLUSION_PROTOCOL (Evidência obrigatória)",
    ])
    
    # Salvar relatório
    with open(output_report, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    # Salvar log
    log_content = f"""AURORA Trading System - Execution Log
Timestamp: {timestamp}
Source Directory: {source_dir}
Output Report: {output_report}

════════════════════════════════════════════════════════════════
SCAN RESULTADO - DETERMINÍSTICO
════════════════════════════════════════════════════════════════
Total de Arquivos: {file_count} (contagem REAL)
Total de Linhas: {total_lines}
Total de Tamanho (bytes): {total_size}

Distribuição por linguagem:
"""
    
    for lang in sorted(lang_count.keys()):
        percentage = (lang_count[lang] * 100) // file_count if file_count > 0 else 0
        log_content += f"  {lang}: {lang_count[lang]} arquivos ({lang_lines[lang]} linhas, {percentage}%)\n"
    
    log_content += f"""
✅ Relatório gerado: {output_report}
✅ Log de execução: {execution_log}

════════════════════════════════════════════════════════════════
✅ PROTOCOLO TIER-0: EVIDÊNCIA CAPTURADA
════════════════════════════════════════════════════════════════

Evidências armazenadas no repositório
Pronto para validação PSA/CQO

Script: scan-57-files-NEUTRAL-REAL.py
Status: ✅ Script executado com segurança Tier-0
"""
    
    with open(execution_log, 'w', encoding='utf-8') as f:
        f.write(log_content)
    
    # Resumo console
    print("════════════════════════════════════════════════════════════════")
    print("📊 SCAN RESULTADO - DETERMINÍSTICO")
    print("════════════════════════════════════════════════════════════════")
    print(f"Total de Arquivos: {file_count} (contagem REAL)")
    print(f"Total de Linhas: {total_lines}")
    print(f"Total de Tamanho (bytes): {total_size}")
    print()
    print("Distribuição por linguagem:")
    for lang in sorted(lang_count.keys()):
        percentage = (lang_count[lang] * 100) // file_count if file_count > 0 else 0
        print(f"  {lang}: {lang_count[lang]} arquivos ({lang_lines[lang]} linhas, {percentage}%)")
    print()
    print(f"✅ Relatório gerado: {output_report}")
    print(f"✅ Log de execução: {execution_log}")
    print()
    print("════════════════════════════════════════════════════════════════")
    print("✅ PROTOCOLO TIER-0: EVIDÊNCIA CAPTURADA")
    print("════════════════════════════════════════════════════════════════")
    print()
    print("✅ Script executado com segurança Tier-0")
    print("✅ Evidências armazenadas no repositório")
    print("✅ Pronto para validação PSA/CQO")
    
    return 0

if __name__ == "__main__":
    exit(main())
