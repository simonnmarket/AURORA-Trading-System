
# 📁 MAPEAMENTO DOS 57 ARQUIVOS – AURORA v8.0 FASE 2
## Especificação Técnica para Tech Lead

**Versão:** 1.0  
**Data:** 2026-01-31  
**Status:** ⚠️ AWAITING TECH LEAD REVIEW  

---

## 1. ESTRUTURA DE CATEGORIZAÇÃO

Cada arquivo será categorizado por:

- **TIER:** Criticidade (1-4)
- **GATE:** Quality gates obrigatórios
- **OWNER:** Responsável técnico
- **METRICS:** Métricas de monitoramento
- **PROMETHEUS:** Labels Prometheus

---

## 2. ARQUIVOS TIER-1 (CRÍTICA)

### 2.1 Prometheus Integration Layer

```yaml
File: prometheus.mql5
├─ Tier: 1 (CRITICAL)
├─ Owner: Tech Lead / Trading Architect
├─ Gates: [1, 2, 3, 4] (ALL required)
├─ Metrics:
│  ├─ prometheus_integration_status (gauge: 0=DOWN, 1=OK)
│  ├─ prometheus_metrics_exported_total (counter)
│  ├─ prometheus_export_latency_ms (histogram)
│  └─ prometheus_export_errors_total (counter)
├─ Prometheus Labels:
│  ├─ component="prometheus_integration"
│  ├─ language="mql5"
│  ├─ tier="critical"
│  └─ criticality="core"
├─ Tests Required:
│  ├─ Unit: Prometheus connection
│  ├─ Integration: MT5 ↔ Prometheus
│  ├─ Load: 1000 metrics/sec
│  └─ Failover: Connection loss recovery
├─ Documentation:
│  ├─ API specification
│  ├─ Configuration guide
│  ├─ Troubleshooting guide
│  └─ ADR: Decision on integration approach
└─ Rollback: Tested, <5 min RTO
```

### 2.2 Health Check System

```yaml
File: health_check.py
├─ Tier: 1 (CRITICAL)
├─ Owner: SRE / Monitoring Architect
├─ Gates: [1, 2, 3, 4] (ALL required)
├─ Metrics:
│  ├─ health_check_status (gauge: 0=FAILED, 1=OK)
│  ├─ health_check_duration_ms (histogram)
│  ├─ health_check_components_healthy (gauge)
│  └─ health_check_failures_total (counter)
├─ Prometheus Labels:
│  ├─ component="health_check"
│  ├─ language="python"
│  ├─ tier="critical"
│  └─ frequency="1m"
├─ Tests Required:
│  ├─ Unit: Each health check function
│  ├─ Integration: Full health check flow
│  ├─ Stress: Simultaneous checks
│  └─ Recovery: Timeout handling
├─ Documentation:
│  ├─ Health indicators explained
│  ├─ Configuration guide
│  ├─ Alert thresholds
│  └─ ADR: Health check strategy
└─ Rollback: Automatic fallback to basic health check
```

### 2.3 Configuration Management

```yaml
File: config.py
├─ Tier: 1 (CRITICAL)
├─ Owner: DevOps / Architecture
├─ Gates: [1, 2, 3] (Security critical)
├─ Metrics:
│  ├─ config_load_status (gauge: 0=INVALID, 1=VALID)
│  ├─ config_reload_total (counter)
│  ├─ config_validation_duration_ms (histogram)
│  └─ config_mismatch_alerts (gauge)
├─ Prometheus Labels:
│  ├─ component="config"
│  ├─ language="python"
│  ├─ tier="critical"
│  └─ env="production|staging"
├─ Tests Required:
│  ├─ Unit: Config loading
│  ├─ Integration: Env overrides
│  ├─ Security: Secrets encryption
│  └─ Validation: Invalid configs rejected
├─ Documentation:
│  ├─ Configuration schema
│  ├─ Environment variables
│  ├─ Secrets management
│  └─ ADR: Config strategy
└─ Security: Secrets encrypted, no plaintext in logs
```

---

## 3. ARQUIVOS TIER-2 (ALTA)

### 3.1 Trading Engine

```yaml
File: trading_engine.mql5
├─ Tier: 2 (HIGH)
├─ Owner: Quantitative Engineer
├─ Gates: [1, 2] (Technical + Operational)
├─ Metrics:
│  ├─ trading_orders_total (counter)
│  ├─ trading_orders_success_rate (gauge)
│  ├─ trading_order_latency_ms (histogram)
│  └─ trading_errors_total (counter)
├─ Prometheus Labels:
│  ├─ component="trading_engine"
│  ├─ language="mql5"
│  ├─ tier="high"
│  └─ strategy="[strategy_name]"
├─ Tests Required:
│  ├─ Unit: Order logic
│  ├─ Backtest: Historical data
│  ├─ Paper trading: Simulated orders
│  └─ Load: Max orders/sec
├─ Documentation:
│  ├─ Strategy documentation
│  ├─ Order types supported
│  ├─ Risk limits
│  └─ ADR: Algorithm decisions
└─ Monitoring: Real-time order tracking
```

### 3.2 Risk Management

```yaml
File: risk_management.py
├─ Tier: 2 (HIGH)
├─ Owner: Risk Officer / CQO
├─ Gates: [1, 2] (Technical + Operational)
├─ Metrics:
│  ├─ risk_limit_breaches_total (counter)
│  ├─ risk_score (gauge: 0-100)
│  ├─ capital_at_risk_usd (gauge)
│  └─ var_95 (gauge)
├─ Prometheus Labels:
│  ├─ component="risk_management"
│  ├─ language="python"
│  ├─ tier="high"
│  └─ metric="[VAR|Sharpe|Volatility]"
├─ Tests Required:
│  ├─ Unit: Risk calculations
│  ├─ Stress: Extreme scenarios
│  ├─ Compliance: Regulatory limits
│  └─ Accuracy: vs. external validators
├─ Documentation:
│  ├─ Risk metrics definitions
│  ├─ Limit thresholds
│  ├─ Alert triggers
│  └─ ADR: Risk model
└─ Compliance: Auditable, immutable logs
```

### 3.3 Data Pipeline

```yaml
File: data_pipeline.py
├─ Tier: 2 (HIGH)
├─ Owner: Data Engineer
├─ Gates: [1, 2] (Technical + Operational)
├─ Metrics:
│  ├─ pipeline_throughput_records_sec (gauge)
│  ├─ pipeline_latency_ms (histogram)
│  ├─ pipeline_errors_total (counter)
│  └─ pipeline_data_quality_score (gauge: 0-100)
├─ Prometheus Labels:
│  ├─ component="data_pipeline"
│  ├─ language="python"
│  ├─ tier="high"
│  └─ stage="[ingestion|transform|load]"
├─ Tests Required:
│  ├─ Unit: Transform logic
│  ├─ Integration: Full pipeline
│  ├─ Performance: Throughput benchmark
│  └─ Data Quality: Validation rules
├─ Documentation:
│  ├─ Data schema
│  ├─ Transform rules
│  ├─ Quality checks
│  └─ ADR: Pipeline architecture
└─ Monitoring: End-to-end latency tracking
```

---

## 4. ARQUIVOS TIER-3 (MÉDIA)

### 4.1 Documentation Files

```yaml
Files: *.md (all markdown files)
├─ Count: ~25 files
├─ Tier: 3 (MEDIUM)
├─ Owner: Technical Writer / PSA
├─ Gates: [1] (Completeness only)
├─ Metrics: (none - documentation)
├─ Categories:
│  ├─ README.md (root documentation)
│  ├─ ARCHITECTURE.md (system design)
│  ├─ API.md (API documentation)
│  ├─ DEPLOYMENT.md (deployment guide)
│  ├─ RUNBOOK_*.md (operational guides)
│  ├─ TROUBLESHOOTING.md (debugging)
│  └─ [others]
├─ Tests Required:
│  ├─ Markdown syntax validation
│  ├─ Links validation (no broken links)
│  ├─ Code examples compilation
│  └─ Freshness check (updated last 6 months)
├─ Documentation:
│  ├─ Style guide (GFM)
│  ├─ Update process
│  ├─ Review cadence
│  └─ Ownership per file
└─ Automation: Markdown linter + link checker
```

### 4.2 Automation Scripts

```yaml
Files: *.sh, *.ps1 (shell and powershell scripts)
├─ Count: ~15 files
├─ Tier: 3 (MEDIUM)
├─ Owner: DevOps / SRE
├─ Gates: [1] (Code quality only)
├─ Metrics:
│  ├─ script_execution_time_sec (histogram)
│  ├─ script_errors_total (counter)
│  └─ script_success_rate (gauge)
├─ Examples:
│  ├─ validate_prometheus.ps1 (monitoring)
│  ├─ generate-audit-trail.sh (logging)
│  ├─ rollback_tier0.py (recovery)
│  ├─ backup_database.sh (backup)
│  ├─ deploy.sh (deployment)
│  └─ [others]
├─ Tests Required:
│  ├─ Syntax check (shellcheck, PSLint)
│  ├─ Dry-run validation
│  ├─ Error handling
│  └─ Idempotency
├─ Documentation:
│  ├─ Usage instructions
│  ├─ Parameter documentation
│  ├─ Error codes
│  └─ ADR: Scripting strategy
└─ Automation: Scheduled execution with monitoring
```

### 4.3 Test Files

```yaml
Files: test_*.py (pytest test files)
├─ Count: ~12 files
├─ Tier: 3 (MEDIUM)
├─ Owner: QA Engineer
├─ Gates: [1] (Code quality only)
├─ Metrics:
│  ├─ test_pass_rate (gauge: %)
│  ├─ test_execution_time_sec (histogram)
│  ├─ code_coverage_percent (gauge: %)
│  └─ test_skipped_total (counter)
├─ Categories:
│  ├─ test_health_check.py
│  ├─ test_prometheus_integration.py
│  ├─ test_risk_management.py
│  ├─ test_data_pipeline.py
│  └─ [others]
├─ Coverage Requirements:
│  ├─ Tier-1 files: ≥95%
│  ├─ Tier-2 files: ≥90%
│  ├─ Tier-3 files: ≥70%
│  └─ Overall: ≥80%
├─ Tests Required:
│  ├─ Unit tests
│  ├─ Integration tests
│  ├─ Performance tests
│  └─ Edge case tests
├─ Documentation:
│  ├─ Test strategy
│  ├─ Test data setup
│  ├─ Assertions explained
│  └─ ADR: Testing approach
└─ Automation: CI/CD integration, run on every commit
```

---

## 5. ARQUIVOS TIER-4 (BAIXA)

### 5.1 Configuration Files

```yaml
Files: .env, *.yaml, *.json (configuration files)
├─ Count: ~5 files
├─ Tier: 4 (LOW)
├─ Owner: DevOps
├─ Gates: [] (No mandatory gates)
├─ Metrics: (none)
├─ Examples:
│  ├─ .env.example (template)
│  ├─ prometheus.yaml (Prometheus config)
│  ├─ grafana-dashboard.json (Dashboard export)
│  ├─ docker-compose.yaml (Local dev)
│  └─ [others]
├─ Validation:
│  ├─ JSON/YAML syntax
│  ├─ Schema validation
│  ├─ No secrets in examples
│  └─ Comments for clarity
├─ Documentation:
│  ├─ Configuration options
│  ├─ Defaults explained
│  ├─ Secrets management
│  └─ ADR: Configuration approach
└─ Automation: Syntax validation on commit
```

---

## 6. INTEGRAÇÃO PROMETHEUS

Cada arquivo mapeia para métricas Prometheus:

```yaml
prometheus.mql5:
  ├─ aurora_prometheus_integration_status
  ├─ aurora_prometheus_metrics_exported_total
  └─ aurora_prometheus_export_latency_ms

health_check.py:
  ├─ aurora_health_check_status
  ├─ aurora_health_check_duration_ms
  └─ aurora_health_check_components_healthy

config.py:
  ├─ aurora_config_load_status
  ├─ aurora_config_reload_total
  └─ aurora_config_validation_duration_ms

[... etc for all files]
```

---

## 7. MATRIZ DE GATES POR TIER

```
TIER-1 (CRÍTICA):
  └─ Gates: [1, 2, 3, 4] (ALL mandatory)
     Scores: 90/85/80/75 (or BLOCKED)

TIER-2 (ALTA):
  └─ Gates: [1, 2] (Technical + Operational)
     Scores: 90/85 (or CONDITIONAL)

TIER-3 (MÉDIA):
  └─ Gates: [1] (Technical only)
     Scores: 85+ (or REMEDIATION)

TIER-4 (BAIXA):
  └─ Gates: [] (Optional)
     Scores: 70+ (advisory)
```

---

## 8. LISTA COMPLETA DOS 57 ARQUIVOS

(Tech Lead deve revisar e validar cada um)

### Tier-1 (4 files)
1. prometheus.mql5
2. health_check.py
3. config.py
4. monitoring_core.py

### Tier-2 (8 files)
5. trading_engine.mql5
6. risk_management.py
7. data_pipeline.py
8. authentication.py
9. api_gateway.py
10. notification_service.py
11. audit_logger.py
12. performance_optimizer.py

### Tier-3 (30 files)
13-22. test_*.py (10 test files)
23-43. Various *.md (21 documentation files)
44-52. Various *.sh, *.ps1 (9 automation scripts)

### Tier-4 (15 files)
53-57. Configuration files (.env, *.yaml, *.json, etc.)

**Total: 57 files**

---

## 9. TAREFAS PARA TECH LEAD

- [ ] **Validar lista de 57 arquivos** (adicionar/remover conforme necessário)
- [ ] **Atribuir owner** para cada arquivo
- [ ] **Definir métricas Prometheus** específicas
- [ ] **Implementar labels** nos arquivos
- [ ] **Configurar CI/CD** para validar gates por tier
- [ ] **Criar dashboards** para visualizar compliance por tier
- [ ] **Testes:** Validar todos os 57 arquivos passam nos gates requeridos

---

## 10. CRITÉRIOS DE ACEITAÇÃO

- [ ] Lista de 57 arquivos validada
- [ ] Owners designados
- [ ] Métricas Prometheus definidas
- [ ] CI/CD validando gates automaticamente
- [ ] Dashboard de compliance funcionando
- [ ] Documentação completa

---

⚠️ **Tech Lead: Alguma crítica ou sugestão antes de proceder?**
