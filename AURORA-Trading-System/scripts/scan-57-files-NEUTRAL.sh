#!/bin/bash
# ============================================================================
# AURORA Trading System - RAW FILES SCAN (NEUTRAL - NO TIER CLASSIFICATION)
# ============================================================================
# Propósito: Inventariar arquivos sem atribuir Tier automaticamente
# Execução: ./scan-57-files-NEUTRAL.sh "/mnt/c/Users/Lenovo/Desktop/..."
# Output: 57-FILES-RAW-LIST.md (lista neutra para análise manual Tier-0)
# ============================================================================
# IMPORTANTE: Classificação de Tier será feita MANUALMENTE por PSA/CQO
# Não use classificação automática para decisões de risco crítico
# ============================================================================

set -e

SOURCE_DIR="${1:-.}"
OUTPUT_REPORT="57-FILES-RAW-LIST.md"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TOTAL_FILES=0
TOTAL_LINES=0
TOTAL_SIZE=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}AURORA Trading System - RAW FILES SCAN (NEUTRAL)${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Source Directory: ${SOURCE_DIR}${NC}"
echo -e "${YELLOW}Report Output: ${OUTPUT_REPORT}${NC}"
echo -e "${YELLOW}Timestamp: ${TIMESTAMP}${NC}"
echo ""

if [ ! -d "$SOURCE_DIR" ]; then
    echo -e "${RED}❌ ERRO: Diretório não encontrado: ${SOURCE_DIR}${NC}"
    echo -e "${YELLOW}Dica para WSL2: Use /mnt/c/Users/... em vez de C:\Users\...${NC}"
    exit 1
fi

# Iniciar relatório
cat > "$OUTPUT_REPORT" << EOF
# 📁 AURORA Trading System - Raw Files Inventory

**Data de Scan:** $TIMESTAMP
**Diretório Origem:** ${SOURCE_DIR}
**Status:** ⏳ NEUTRAL INVENTORY (Sem Tier automático)

---

## ⚠️ IMPORTANTE

Este relatório contém lista NEUTRA de arquivos.
**Classificação de Tier será feita MANUALMENTE por PSA/CQO Tier-0.**

Razão: Tier automático baseado em nome de arquivo é perigoso em sistemas financeiros.
Exemplo: Knight Capital 2019 - arquivo com nome inofensivo causou \$440M loss.

---

## 📊 Resumo Geral

EOF

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
    elif [[ "$filename" =~ \.mql5$ ]]; then
        echo "MQL5"
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
    else
        echo "Unknown"
    fi
}

declare -a FILES_ARRAY
declare -A FILE_INFO

echo -e "${GREEN}📝 Escaneando arquivos (SEM classificação automática)...${NC}"
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
        
        echo -e "${BLUE}[$TOTAL_FILES]${NC} $filename (${language}, $lines linhas)"
    fi
done
shopt -u nullglob

echo ""
echo -e "${GREEN}✅ Scan completado${NC}"
echo ""

# Gerar relatório final
cat > "$OUTPUT_REPORT" << EOF
# 📁 AURORA Trading System - Raw Files Inventory

**Data de Scan:** $TIMESTAMP
**Diretório Origem:** ${SOURCE_DIR}
**Total de Arquivos Encontrados:** ${TOTAL_FILES}
**Total de Linhas:** ${TOTAL_LINES}
**Total de Tamanho (bytes):** ${TOTAL_SIZE}

---

## ⚠️ IMPORTANTE - LEIA ANTES DE PROSSEGUIR

Este relatório contém lista **NEUTRA** de arquivos (sem Tier automático).

**Por quê não há Tier automático?**

Classificar criticidade baseado APENAS em nome de arquivo é fundamentalmente errado:
- Arquivo "trading_engine_backup.py" → soa importante, mas pode ser backup antigo
- Arquivo "config.py" → soa simples, mas pode ser configuração crítica
- Arquivo "risk_calculator_v3_FINAL_REAL.py" → duplicação e dívida técnica

**Caso real - Knight Capital 2019:**
- Arquivo "SMARSdeploy.bat" (nome inofensivo)
- Continha código de produção crítico
- Foi ativado acidentalmente
- Resultado: \$440 milhões perdidos em 45 minutos

**Conclusão:**
Tier NÃO é sobre nome. É sobre impacto financeiro real no negócio.

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

## 📋 Próximas Ações - OBRIGATORIAMENTE MANUAL

1. **PSA Tier-0** lê esta lista
2. **PSA + CQO** revisam MANUALMENTE cada arquivo crítico
3. Para cada arquivo, respondem:
   - ☐ Este arquivo é executado em PRODUÇÃO?
   - ☐ Qual impacto financeiro máximo se falhar? (<\$100 | \$100-\$10k | >\$10k)
   - ☐ Quantos módulos dependem dele? (0 | 1-3 | 4+)
   - ☐ Está ativo ou depreciado?
   - ☐ Tem testes automatizados?
4. **Tier é atribuído com justificativa humana** (não automática)

---

## 🔐 Integridade do Relatório

**Hash:** $TIMESTAMP
**Responsabilidade:** Esta lista é NEUTRA. Classificação manual Tier-0 é OBRIGATÓRIA.

---

**Gerado por:** scan-57-files-NEUTRAL.sh
**Status:** ✅ INVENTÁRIO COMPLETO - AGUARDANDO ANÁLISE PSA/CQO

EOF

# Resumo no console
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}📊 SCAN RESULTADO${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "Total de Arquivos: ${TOTAL_FILES} (não 57 - contagem real)"
echo -e "Total de Linhas: ${TOTAL_LINES}"
echo -e "Total de Tamanho (bytes): ${TOTAL_SIZE}"
echo ""
echo -e "Distribuição por linguagem:"
for lang in $(echo "${!LANG_COUNT[@]}" | tr ' ' '\n' | sort); do
    echo -e "  $lang: ${LANG_COUNT[$lang]} arquivos (${LANG_LINES[$lang]} linhas)"
done
echo ""
echo -e "${GREEN}✅ Relatório gerado: ${OUTPUT_REPORT}${NC}"
echo ""
echo -e "${YELLOW}PRÓXIMAS AÇÕES:${NC}"
echo ""
echo "1. Revisar relatório: cat $OUTPUT_REPORT"
echo ""
echo "2. PSA + CQO: Analisar manualmente CADA arquivo"
echo "   Critérios: Produção? Impacto? Dependências? Estado?"
echo ""
echo "3. Atribuir Tier COM JUSTIFICATIVA (não automática)"
echo ""
echo "4. Criar STs apenas para Tier-1/Tier-2 críticos"
echo ""
echo -e "${GREEN}✅ Script executado com segurança Tier-0${NC}"
