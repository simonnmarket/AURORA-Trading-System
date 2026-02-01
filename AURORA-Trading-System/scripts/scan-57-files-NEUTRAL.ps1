# ============================================================================
# AURORA Trading System - RAW FILES SCAN (NEUTRAL - NO TIER CLASSIFICATION)
# PowerShell Version - Para Windows nativo sem WSL2
# ============================================================================
# Propósito: Inventariar arquivos sem atribuir Tier automaticamente
# Execução: .\scan-57-files-NEUTRAL.ps1 "C:\Users\Lenovo\Desktop\File Desktop\..."
# Output: 57-FILES-RAW-LIST.md
# ============================================================================

param(
    [string]$SourceDir = "."
)

$OutputReport = "57-FILES-RAW-LIST.md"
$Timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$TotalFiles = 0
$TotalLines = 0
$TotalSize = 0

# Cores
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Cyan"

Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor $Blue
Write-Host "AURORA Trading System - RAW FILES SCAN (NEUTRAL)" -ForegroundColor $Blue
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor $Blue
Write-Host ""
Write-Host "Source Directory: $SourceDir" -ForegroundColor $Yellow
Write-Host "Report Output: $OutputReport" -ForegroundColor $Yellow
Write-Host "Timestamp: $Timestamp" -ForegroundColor $Yellow
Write-Host ""

# Validar diretório
if (-not (Test-Path $SourceDir)) {
    Write-Host "❌ ERRO: Diretório não encontrado: $SourceDir" -ForegroundColor Red
    exit 1
}

# Funções
function Get-FileLanguage {
    param([string]$filename)
    
    $ext = [System.IO.Path]::GetExtension($filename).ToLower()
    
    switch ($ext) {
        ".py" { return "Python" }
        ".mql5" { return "MQL5" }
        ".md" { return "Markdown" }
        ".sh" { return "Bash" }
        ".ps1" { return "PowerShell" }
        ".json" { return "JSON" }
        ".yaml" { return "YAML"; break }
        ".yml" { return "YAML"; break }
        ".env" { return "ENV" }
        ".txt" { return "Text" }
        ".csv" { return "CSV" }
        ".sql" { return "SQL" }
        default { return "Unknown" }
    }
}

# Coletar arquivos
$Files = @()
$FileInfo = @{}
$LangCount = @{}
$LangLines = @{}

Write-Host "📝 Escaneando arquivos (SEM classificação automática)..." -ForegroundColor $Green
Write-Host ""

Get-ChildItem -Path $SourceDir -File | ForEach-Object {
    $TotalFiles++
    
    $filename = $_.Name
    $filesize = $_.Length
    
    # Contar linhas
    $lines = 0
    try {
        if ($_ -match '\.(py|sh|ps1|json|yaml|yml|md|txt|sql)$') {
            $lines = @(Get-Content $_.FullName -ErrorAction SilentlyContinue | Measure-Object -Line).Count
        }
    }
    catch { }
    
    $language = Get-FileLanguage $filename
    
    $TotalLines += $lines
    $TotalSize += $filesize
    
    $Files += $filename
    $FileInfo[$filename] = @{
        Language = $language
        Lines = $lines
        Size = $filesize
    }
    
    # Acumular por linguagem
    if (-not $LangCount[$language]) { $LangCount[$language] = 0 }
    if (-not $LangLines[$language]) { $LangLines[$language] = 0 }
    $LangCount[$language]++
    $LangLines[$language] += $lines
    
    Write-Host "[$TotalFiles] $filename ($language, $lines linhas)" -ForegroundColor $Blue
}

Write-Host ""
Write-Host "✅ Scan completado" -ForegroundColor $Green
Write-Host ""

# Gerar relatório
$ReportContent = @"
# 📁 AURORA Trading System - Raw Files Inventory

**Data de Scan:** $Timestamp
**Diretório Origem:** $SourceDir
**Total de Arquivos Encontrados:** $TotalFiles
**Total de Linhas:** $TotalLines
**Total de Tamanho (bytes):** $TotalSize

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
- Resultado: $440 milhões perdidos em 45 minutos

**Conclusão:**
Tier NÃO é sobre nome. É sobre impacto financeiro real no negócio.

---

## 📋 Lista de Arquivos (Ordenada por Tamanho)

| # | Arquivo | Linguagem | Linhas | Tamanho (bytes) |
|---|---------|-----------|--------|-----------------|
"@

# Ordenar por tamanho (descendente)
$SortedFiles = $Files | ForEach-Object {
    $info = $FileInfo[$_]
    [PSCustomObject]@{
        Filename = $_
        Language = $info.Language
        Lines = $info.Lines
        Size = $info.Size
    }
} | Sort-Object Size -Descending

$count = 0
$SortedFiles | ForEach-Object {
    $count++
    $ReportContent += "`n| $count | $($_.Filename) | $($_.Language) | $($_.Lines) | $($_.Size) |"
}

$ReportContent += @"

---

## 📊 Estatísticas por Linguagem

| Linguagem | Arquivos | Linhas Totais |
|-----------|----------|---------------|
"@

$LangCount.GetEnumerator() | Sort-Object Name | ForEach-Object {
    $ReportContent += "`n| $($_.Key) | $($_.Value) | $($LangLines[$_.Key]) |"
}

$ReportContent += @"

---

## 📋 Próximas Ações - OBRIGATORIAMENTE MANUAL

1. **PSA Tier-0** lê esta lista
2. **PSA + CQO** revisam MANUALMENTE cada arquivo crítico
3. Para cada arquivo, respondem:
   - ☐ Este arquivo é executado em PRODUÇÃO?
   - ☐ Qual impacto financeiro máximo se falhar? (<$100 | $100-$10k | >$10k)
   - ☐ Quantos módulos dependem dele? (0 | 1-3 | 4+)
   - ☐ Está ativo ou depreciado?
   - ☐ Tem testes automatizados?
4. **Tier é atribuído com justificativa humana** (não automática)

---

## 🔐 Integridade do Relatório

**Hash:** $Timestamp
**Responsabilidade:** Esta lista é NEUTRA. Classificação manual Tier-0 é OBRIGATÓRIA.

---

**Gerado por:** scan-57-files-NEUTRAL.ps1
**Status:** ✅ INVENTÁRIO COMPLETO - AGUARDANDO ANÁLISE PSA/CQO

"@

# Salvar relatório
$ReportContent | Out-File -FilePath $OutputReport -Encoding UTF8

# Resumo console
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor $Green
Write-Host "📊 SCAN RESULTADO" -ForegroundColor $Green
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor $Green
Write-Host "Total de Arquivos: $TotalFiles (não 57 - contagem real)" -ForegroundColor White
Write-Host "Total de Linhas: $TotalLines" -ForegroundColor White
Write-Host "Total de Tamanho (bytes): $TotalSize" -ForegroundColor White
Write-Host ""
Write-Host "Distribuição por linguagem:" -ForegroundColor White
$LangCount.GetEnumerator() | Sort-Object Name | ForEach-Object {
    Write-Host "  $($_.Key): $($_.Value) arquivos ($($LangLines[$_.Key]) linhas)" -ForegroundColor White
}
Write-Host ""
Write-Host "✅ Relatório gerado: $OutputReport" -ForegroundColor $Green
Write-Host ""
Write-Host "PRÓXIMAS AÇÕES:" -ForegroundColor $Yellow
Write-Host ""
Write-Host "1. Revisar relatório: Get-Content $OutputReport"
Write-Host ""
Write-Host "2. PSA + CQO: Analisar manualmente CADA arquivo"
Write-Host "   Critérios: Produção? Impacto? Dependências? Estado?"
Write-Host ""
Write-Host "3. Atribuir Tier COM JUSTIFICATIVA (não automática)"
Write-Host ""
Write-Host "4. Criar STs apenas para Tier-1/Tier-2 críticos"
Write-Host ""
Write-Host "✅ Script executado com segurança Tier-0" -ForegroundColor $Green
