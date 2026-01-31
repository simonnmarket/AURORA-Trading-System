
# 🗂️ LESSONS LEARNED DATABASE STRUCTURE
## Especificação Técnica para Tech Lead

**Versão:** 1.0  
**Data:** 2026-01-31  
**Status:** ⚠️ AWAITING TECH LEAD REVIEW  
**Responsável:** Tech Lead (Implementação)  

---

## 1. OBJETIVO

Criar um sistema estruturado de armazenamento e recuperação de lições aprendidas em projetos Aurora, permitindo:
- Rastreabilidade de erros e soluções
- Reutilização de conhecimento
- Prevenção de repetição de problemas
- Melhoria contínua documentada

---

## 2. ESTRUTURA DE DADOS

### 2.1 Modelo de Armazenamento

**Formato:** JSON (ou PostgreSQL com export JSON)

```json
{
  "id": "LL-YYYY-MM-DD-NNN",
  "timestamp_created": "2026-02-01T14:30:00Z",
  "category": "TECHNICAL|PROCESS|SECURITY|OPERATIONAL",
  "severity": "CRITICAL|HIGH|MEDIUM|LOW",
  "component": "health_check|trading_engine|prometheus|...",
  "title": "[Concise title]",
  "situation": "[O que aconteceu - descrição do cenário]",
  "impact": "[Consequências - quantificado se possível]",
  "root_cause": "[Análise de causa raiz - 5 whys]",
  "solution": "[Solução implementada]",
  "prevention": "[Como evitar no futuro]",
  "action_items": [
    {
      "action": "[Ação específica]",
      "owner": "[Nome do responsável]",
      "due_date": "YYYY-MM-DD",
      "status": "OPEN|IN_PROGRESS|COMPLETED",
      "completion_date": "YYYY-MM-DD"
    }
  ],
  "tags": ["tag1", "tag2", "tag3"],
  "related_incidents": ["INC-001", "INC-002"],
  "author": "[Nome do criador]",
  "approver": "[PSA/CQO]",
  "approval_date": "2026-02-01T15:00:00Z",
  "references": [
    {
      "type": "JIRA|GITHUB|DOCUMENT|POST_MORTEM",
      "link": "https://..."
    }
  ],
  "metrics": {
    "time_to_detect": "PT2H30M",
    "time_to_resolve": "PT5H",
    "business_impact_usd": 50000,
    "replication_attempts": 3,
    "success_rate_prevention": "100%"
  },
  "follow_up": {
    "due_date": "2026-03-01",
    "status": "PENDING|COMPLETED",
    "notes": "[Notas de seguimento]"
  }
}
```

### 2.2 Locais de Armazenamento

```
02-Reports/
├── lessons-learned/
│   ├── 2026-01/
│   │   ├── LL-2026-01-31-001.json
│   │   ├── LL-2026-01-31-002.json
│   │   └── ...
│   ├── 2026-02/
│   │   └── ...
│   └── index.json (metaindex)
├── incidents/
│   ├── incident-post-mortem-2026-01-31.md
│   └── ...
└── archive/
    └── [lessons-learned antigos > 2 anos]
```

---

## 3. PROCESSO DE CRIAÇÃO

### 3.1 Trigger (Quando criar Lesson Learned)

**Automático:**
- Toda falha P1/P2 detectada
- Toda violação de security
- Todo rollback executado
- Todo SLA miss crítico

**Manual:**
- PSA identifica padrão em múltiplas ocorrências
- Tech Lead propõe melhoria baseada em experiência
- Conselho solicita documentação de aprendizado

### 3.2 Template de Criação

```markdown
# Lesson Learned: [TÍTULO]

**ID:** LL-YYYY-MM-DD-NNN  
**Data:** YYYY-MM-DD  
**Categoria:** [TECHNICAL/PROCESS/SECURITY/OPERATIONAL]  
**Severidade:** [CRITICAL/HIGH/MEDIUM/LOW]  
**Componente:** [health_check/trading_engine/...]  
**Autor:** [Nome]  
**Aprovador:** [PSA/CQO]  

## Situação
[Descrição detalhada do que aconteceu]

## Impacto
- Downtime: X minutos
- Usuários afetados: X
- Impacto financeiro: €X
- Dados perdidos: SIM/NÃO

## Causa Raiz (5 Whys)
1. Por quê? [Resposta]
2. Por quê? [Resposta]
3. Por quê? [Resposta]
4. Por quê? [Resposta]
5. Por quê? [Resposta final = Causa raiz]

## Solução Implementada
[Detalhes da solução]

## Prevenção
[Como evitar no futuro]

## Action Items
- [ ] [Ação 1] - Owner: [Nome] - Due: [Data]
- [ ] [Ação 2] - Owner: [Nome] - Due: [Data]

## Referências
- JIRA: [Link]
- GitHub PR: [Link]
- Post-mortem: [Link]

## Follow-up
- Due: YYYY-MM-DD
- Status: [PENDING/COMPLETED]
```

---

## 4. ESTRUTURA DE QUERY E BUSCA

### 4.1 Queries Esperadas

```python
# Tech Lead deve implementar queries para:

# Query 1: Buscar por categoria
GET /api/lessons-learned?category=SECURITY

# Query 2: Buscar por severidade
GET /api/lessons-learned?severity=CRITICAL

# Query 3: Buscar por componente
GET /api/lessons-learned?component=health_check

# Query 4: Buscar por período
GET /api/lessons-learned?from=2026-01-01&to=2026-02-01

# Query 5: Buscar por tags
GET /api/lessons-learned?tags=prometheus,monitoring

# Query 6: Búsqueda de texto livre
GET /api/lessons-learned?search=rollback

# Query 7: Listar abertos (action items pendentes)
GET /api/lessons-learned?action_status=OPEN
```

### 4.2 Agregações Esperadas

```python
# Agregação 1: Contagem por categoria (gráfico de pizza)
GET /api/lessons-learned/stats/by_category
Response: {
  "TECHNICAL": 45,
  "SECURITY": 12,
  "OPERATIONAL": 8,
  "PROCESS": 5
}

# Agregação 2: Severidade trend (gráfico de linha)
GET /api/lessons-learned/stats/severity_trend?period=monthly
Response: {
  "2026-01": {"CRITICAL": 3, "HIGH": 5, ...},
  "2026-02": {"CRITICAL": 1, "HIGH": 3, ...}
}

# Agregação 3: Top componentes com problemas
GET /api/lessons-learned/stats/top_components
Response: [
  {"component": "health_check", "count": 15},
  {"component": "trading_engine", "count": 8},
  ...
]

# Agregação 4: Action items em atraso
GET /api/lessons-learned/stats/overdue_actions
Response: {
  "overdue_count": 3,
  "items": [...]
}
```

---

## 5. INTEGRAÇÃO COM OUTROS SISTEMAS

### 5.1 Integração com Incident Management

```
incident-post-mortem.md (Fase 1)
    ↓ PSA revisa
Lesson Learned criado (Fase 2)
    ↓ Tech Lead implementa query
Lessons-Learned Database (Armazenamento)
    ↓ Dashboard recupera
KPI Dashboard (Visualização)
```

### 5.2 Integração com Prometheus

**Métrica exportada:**

```
# Lessons Learned Metrics
lessons_learned_total{category="TECHNICAL",severity="CRITICAL"} 3
lessons_learned_total{category="SECURITY",severity="HIGH"} 12
lessons_learned_action_items_open{component="health_check"} 5
lessons_learned_action_items_overdue{component="health_check"} 2
```

---

## 6. TAREFAS PARA TECH LEAD

### 6.1 Implementação de Banco de Dados

- [ ] **Escolha de storage:** PostgreSQL / MongoDB / JSON files
- [ ] **Schema de tabelas/coleções** baseado em 2.1
- [ ] **Índices** para queries rápidas (categoria, severidade, timestamp)
- [ ] **Backup automático** (diário, retenção 2 anos)
- [ ] **Encryption** de dados sensíveis (impacto financeiro, dados PII)

### 6.2 Implementação de APIs

- [ ] **REST API** com queries de 4.1
- [ ] **Agregações** de 4.2
- [ ] **Autenticação** (somente PSA/Conselho podem criar)
- [ ] **Rate limiting** para evitar abuso
- [ ] **Logging** de todas as operações

### 6.3 Integração com Prometheus

- [ ] **Exporter** que converte LL data para Prometheus metrics
- [ ] **Scheduled job** (ex: diário às 00:00 UTC) para sincronizar
- [ ] **Alertas** se action items em atraso > 2

### 6.4 Geração de Relatórios

- [ ] **Relatório semanal:** Top 5 lessons learned da semana
- [ ] **Relatório mensal:** Trend de severidades + componentes
- [ ] **Relatório trimestral:** Análise de padrões + recomendações

### 6.5 Testes e Validação

- [ ] **Teste de carga:** 10k lessons learned
- [ ] **Teste de query:** <100ms para qualquer query
- [ ] **Teste de backup:** Restauração bem-sucedida
- [ ] **Teste de integração:** Com Prometheus e dashboards

---

## 7. CRITÉRIOS DE ACEITAÇÃO

- [ ] Database funcionando e acessível
- [ ] Todas queries de 4.1 retornando dados corretos
- [ ] Agregações de 4.2 disponíveis
- [ ] Relatórios automáticos sendo gerados
- [ ] Métricas Prometheus sendo exportadas
- [ ] Documentação completa
- [ ] Testes automatizados cobrindo >90% código

---

## 8. CRONOGRAMA RECOMENDADO (Tech Lead)

```
Week 1: Database setup + schema
Week 2: APIs implementation
Week 3: Prometheus integration
Week 4: Reports automation
Week 5: Testing + documentation
Week 6: Deploy + monitoring
```

---

⚠️ **Tech Lead: Alguma crítica ou sugestão antes de proceder com implementação?**
