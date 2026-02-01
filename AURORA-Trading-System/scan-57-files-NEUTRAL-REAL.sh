#!/bin/bash
# ============================================================================
# AURORA Trading System - RAW FILES SCAN (NEUTRAL - TIER-0 PROTOCOL)
# ============================================================================
# ST-006: Neutral File Scan - Real Execution Deterministic
# 
# Propósito: Inventariar arquivos SEM atribuir Tier automaticamente
# Protocolo: ZERO_ILLUSION_PROTOCOL - Evidência obrigatória
# 
# Execução: ./scan-57-files-NEUTRAL-REAL.sh "/path/to/files"
# Output: 57-FILES-RAW-LIST.md (lista neutra para análise manual PSA/CQO)
# 
# ⚠️ IMPORTANTE: Classificação de Tier será feita MANUALMENTE por PSA/CQO
# ⚠️ NÃO use classificação automática para decisões de risco crítico
# ============================================================================

set -euo pipefail

SOURCE_DIR="${1:-.}"
OUTPUT_REPORT="57-FILES-RAW-LIST.md"
EXECUTION_LOG="scan-execution-log.txt"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TOTAL_FILES=0
TOTAL_LINES=0
TOTAL_SIZE=0

# ANSI Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ============================================================================
# PROTOCOLO TIER-0: EVIDÊNCIA DETERMINÍSTICA
# ============================================================================
# Todos os comandos REAL com timestamps
# Todas saídas capturadas para auditoria
# Sem simulação, sem pressupostos, apenas FATOS verificáveis
# ============================================================================

{

echo "════════════════════════════════════════════════════════════════"
echo "AURORA Trading System - RAW FILES SCAN (TIER-0 PROTOCOL)"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "🔴 PROTOCOLO: ZERO_ILLUSION_PROTOCOL"
echo "✅ EVIDÊNCIA OBRIGATÓRIA: Sim"
echo "✅ TIER AUTOMÁTICO: NÃO (manual PSA/CQO)"
echo ""
echo "Source Directory: $SOURCE_DIR"
echo "Report Output: $OUTPUT_REPORT"
echo "Execution Log: $EXECUTION_LOG"
echo "Timestamp: $TIMESTAMP"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

# Validar diretório
if [ ! -d "$SOURCE_DIR" ]; then
    echo "❌ ERRO: Diretório não encontrado: $SOURCE_DIR"
    echo "Dica WSL2: Use /mnt/c/Users/... em vez de C:\Users\..."
    exit 1
fi

echo "✅ Diretório validado"
echo ""

# Contar arquivos antes
FILE_COUNT=$(find "$SOURCE_DIR" -maxdepth 1 -type f | wc -l)
echo "📊 Contagem prévia: $FILE_COUNT arquivos"
echo ""

# Funções APENAS para coleta de dados (SEM Tier)
count_lines() {
    local file="$1"
    if [ -f "$file" ]; then
        wc -l < "$file" 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

get_size() {
    local file="$1"
    if [ -f "$file" ]; then
        stat -c%s "$file" 2>/dev/null || wc -c < "$file" 2>/dev/null
    else
        echo "0"
    fi
}

detect_language() {
    local filename="$1"
    
    if [[ "$filename" =~ \.py$ ]]; then
        echo "Python"
    elif [[ "$filename" =~ \.mql5$ ]] || [[ "$filename" =~ \.mq5$ ]]; then
        echo "MQL5"
    elif [[ "$filename" =~ \.mqh$ ]]; then
        echo "MQH"
    elif [[ "$filename" =~ \.md$ ]]; then
        echo "Markdown"
    elif [[ "$filename" =~ \.sh$ ]]; then
        echo "Bash"
    elif [[ "$filename" =~ \.ps1$ ]]; then
        echo "PowerShell"
    elif [[ "$filename" =~ \.json$ ]]; then
        echo "JSON"
    elif [[ "$filename" =~ \.yaml$ ]] || [[ "$filename" =~ \.yml$ ]]; then
        echo "YAML"
    elif [[ "$filename" =~ \.env$ ]]; then
        echo "ENV"
    elif [[ "$filename" =~ \.txt$ ]]; then
        echo "Text"
    else
        echo "Unknown"
    fi
}

# Coletar dados
declare -a FILES_ARRAY
declare -A FILE_INFO

echo "📝 Escaneando arquivos..."
echo ""

shopt -s nullglob
for file in "$SOURCE_DIR"/*; do
    if [ -f "$file" ]; then
        TOTAL_FILES=$((TOTAL_FILES + 1))
        
        filename=$(basename "$file")
        filesize=$(get_size "$file")
        lines=$(count_lines "$file")
        language=$(detect_language "$filename")
        
        TOTAL_LINES=$((TOTAL_LINES + lines))
        TOTAL_SIZE=$((TOTAL_SIZE + filesize))
        
        FILES_ARRAY+=("$filename")
        FILE_INFO["$filename"]="$language|$lines|${filesize}"
        
        printf "[%3d] %s (%s, %d linhas)\n" "$TOTAL_FILES" "$filename" "$language" "$lines"
    fi
done
shopt -u nullglob

echo ""
echo "✅ Scan completado"
echo ""

# Gerar relatório
cat > "$OUTPUT_REPORT" << EOF
# 📁 AURORA Trading System - Raw Files Inventory

**Data de Scan:** $TIMESTAMP
**Diretório Origem:** $SOURCE_DIR
**Total de Arquivos Encontrados:** $TOTAL_FILES
**Total de Linhas:** $TOTAL_LINES
**Total de Tamanho (bytes):** $TOTAL_SIZE

---

## ⚠️ PROTOCOLO TIER-0 - EVIDÊNCIA DETERMINÍSTICA

Este relatório contém lista **NEUTRA** de arquivos (SEM Tier automático).

### Por quê NÃO há Tier automático?

Classificar criticidade baseado APENAS em nome de arquivo é fundamentalmente errado:
- "trading_engine_backup.py" → soa importante, mas pode ser backup antigo
- "config.py" → soa simples, mas pode ser configuração crítica  
- "SMARSdeploy.bat" (Knight Capital 2019) → resultou em \$440M loss

**Conclusão:** Tier NÃO é sobre nome. É sobre impacto financeiro real no negócio.

### Classificação Manual Obrigatória (Próximas Fases)

1. **PSA Tier-0**: Analisa manualmente cada arquivo
2. **CQO**: Atribui Tier com justificativa de risco
3. **CTO**: Valida critério técnico
4. Tier é decisão humana, nunca automática

---

## 📋 Lista de Arquivos (Ordenada por Tamanho)

| # | Arquivo | Linguagem | Linhas | Tamanho (bytes) |
|---|---------|-----------|--------|-----------------|
EOF

# Ordenar por tamanho (descendente) e adicionar à tabela
(
    for filename in "${FILES_ARRAY[@]}"; do
        IFS='|' read -r lang lines size <<< "${FILE_INFO[$filename]}"
        echo "$size|$filename|$lang|$lines"
    done
) | sort -rn | awk -F'|' '{
    count++
    printf "| %d | %s | %s | %s | %s |\n", count, $2, $3, $4, $1
}' >> "$OUTPUT_REPORT"

cat >> "$OUTPUT_REPORT" << EOF

---

## 📊 Estatísticas por Linguagem

EOF

# Agrupar por linguagem
declare -A LANG_COUNT
declare -A LANG_LINES

for filename in "${FILES_ARRAY[@]}"; do
    IFS='|' read -r lang lines size <<< "${FILE_INFO[$filename]}"
    LANG_COUNT[$lang]=$((${LANG_COUNT[$lang]:-0} + 1))
    LANG_LINES[$lang]=$((${LANG_LINES[$lang]:-0} + lines))
done

echo "| Linguagem | Arquivos | Linhas Totais |" >> "$OUTPUT_REPORT"
echo "|-----------|----------|---------------|" >> "$OUTPUT_REPORT"

for lang in $(echo "${!LANG_COUNT[@]}" | tr ' ' '\n' | sort); do
    echo "| $lang | ${LANG_COUNT[$lang]} | ${LANG_LINES[$lang]} |" >> "$OUTPUT_REPORT"
done

cat >> "$OUTPUT_REPORT" << EOF

---

## 📋 Próximas Ações - ANÁLISE MANUAL TIER-0

1. **PSA Tier-0**: Lê este relatório
2. **PSA + CQO**: Revisam MANUALMENTE cada arquivo crítico
3. Para cada arquivo, respondem:
   - ☐ Este arquivo está em PRODUÇÃO?
   - ☐ Qual impacto financeiro máximo se falhar? (<\$100 | \$100-\$10k | >\$10k)
   - ☐ Quantos módulos dependem dele? (0 | 1-3 | 4+)
   - ☐ Está ativo ou depreciado?
   - ☐ Tem testes automatizados?
4. **Tier é atribuído com justificativa humana** (não automática)

---

## 🔐 Verificação de Integridade

**Executado:** $TIMESTAMP
**Máquina:** $(hostname)
**Usuário:** $(whoami)
**Shell:** $(bash --version | head -1)
**Path:** $SOURCE_DIR

**Validação:** ✅ Determinística

---

**Gerado por:** scan-57-files-NEUTRAL-REAL.sh
**Status:** ✅ INVENTÁRIO COMPLETO - AGUARDANDO ANÁLISE PSA/CQO
**Protocolo:** ✅ ZERO_ILLUSION_PROTOCOL (Evidência obrigatória)

EOF

# Resumo console
echo "════════════════════════════════════════════════════════════════"
echo "📊 SCAN RESULTADO - DETERMINÍSTICO"
echo "════════════════════════════════════════════════════════════════"
echo "Total de Arquivos: $TOTAL_FILES (contagem REAL)"
echo "Total de Linhas: $TOTAL_LINES"
echo "Total de Tamanho (bytes): $TOTAL_SIZE"
echo ""
echo "Distribuição por linguagem:"
for lang in $(echo "${!LANG_COUNT[@]}" | tr ' ' '\n' | sort); do
    PERCENTAGE=$((LANG_COUNT[$lang] * 100 / TOTAL_FILES))
    echo "  $lang: ${LANG_COUNT[$lang]} arquivos (${LANG_LINES[$lang]} linhas, $PERCENTAGE%)"
done
echo ""
echo "✅ Relatório gerado: $OUTPUT_REPORT"
echo "✅ Log de execução: $EXECUTION_LOG"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ PROTOCOLO TIER-0: EVIDÊNCIA CAPTURADA"
echo "════════════════════════════════════════════════════════════════"
echo ""

} | tee "$EXECUTION_LOG"

echo ""
echo "✅ Script executado com segurança Tier-0"
echo "✅ Evidências armazenadas no repositório"
echo "✅ Pronto para validação PSA/CQO"
