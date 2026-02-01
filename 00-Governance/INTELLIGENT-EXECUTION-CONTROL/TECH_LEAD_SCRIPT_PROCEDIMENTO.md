
# ============================================================================
# 🔧 SCRIPT TÉCNICO: PROCEDIMENTO AURORA TIER-0 v2.1
# ============================================================================
# 📌 DIRECIONADO PARA: Tech Lead (IA Agent)
# 💻 ENVIRONMENT: Visual Code + Windows (já operando na plataforma)
# 🎯 OBJETIVO: Executar tarefas conforme ST → Gerar RC
# ⚠️ IMPORTANTE: Apenas comandos. Dúvidas? Reporte ao final.
# ============================================================================

## PASSO 1: ENTENDER O FLUXO (2 MINUTOS)
# ============================================================================

FLUXO_SIMPLES:
  1. PSA cria Solicitação Técnica (ST)
  2. CEO aprova e encaminha para você
  3. VOCÊ → Executa a tarefa
  4. VOCÊ → Preenche Relatório Conclusão (RC)
  5. CEO valida → PSA fecha

SEU_PAPEL:
  - Receber ST com instruções claras
  - Executar no seu ambiente (Visual Code)
  - Preencher RC com evidências
  - Documentar qualquer desvio

TEMPO_ESTIMADO:
  - Leitura ST: < 2 minutos
  - Execução: conforme estimativa na ST
  - Preenchimento RC: < 2 minutos
  - Total ciclo: ST + Execução + RC

---

## PASSO 2: QUANDO VOCÊ RECEBER UMA ST (SOLICITAÇÃO TÉCNICA)
# ============================================================================

VOCÊ_RECEBERÁ:
  ✅ ST via chat com arquivo ST.yaml
  ✅ Arquivo conterá: O QUE fazer, QUANDO fazer, ONDE salvar

ARQUIVO_ST_CONTÉM:
  • st_id: Identificador único (ex: AURORA-ST-20260201-001)
  • titulo: O que fazer em 1 frase
  • modulo_afetado: Qual módulo/pasta (ex: src/api/)
  • arquivo_principal: Arquivo alvo (ex: main.py)
  • tipo_mudanca: NOVO_RECURSO | CORRECAO_BUG | OTIMIZACAO
  • data_inicio_prevista: Quando começar
  • data_conclusao_prevista: Quando terminar
  • esforco_estimado_horas: Quantas horas vai levar
  • criterios_aceitacao: Checklist do que validar

---

## PASSO 3: PREPARAR AMBIENTE (5 MINUTOS)
# ============================================================================

VOCÊ_JÁ_ESTÁ_EM_VISUAL_CODE:
  ✅ Plataforma já carregada
  ✅ Repositório já sincronizado
  ✅ Terminal integrado disponível

SINCRONIZAR_REPOSITÓRIO:
  
  # Abrir Terminal integrado (Ctrl + `)
  git status
  
  # Se não está atualizado:
  git pull origin main

CONFIRMAR_BRANCH:
  
  git branch -v
  # Deve estar em: main ou aurora-f1-minimal-20260131
  # Se em branch errado:
  git checkout main
  # OU
  git checkout aurora-f1-minimal-20260131

---

## PASSO 4: EXECUTAR A TAREFA
# ============================================================================

FLUXO_PADRÃO:

  1️⃣ Leia a ST completamente
  
  2️⃣ Navegue até pasta/arquivo indicado:
     cd src/api/
     # ou conforme indicado na ST
  
  3️⃣ Faça as mudanças necessárias:
     - Abra arquivo em Visual Code
     - Implemente conforme ST descreve
     - Salve (Ctrl + S)
  
  4️⃣ Teste localmente:
     # Conforme tipo_mudanca indicado na ST
     # Ex: para Python → python seu_arquivo.py
     # Ex: para Node → npm test
  
  5️⃣ Commit das mudanças:
     git add .
     git commit -m "AURORA-ST-20260201-001: [descrição breve da mudança]"
     # Exemplo:
     # git commit -m "AURORA-ST-20260201-001: Create main.py entry point"
  
  6️⃣ Push para GitHub:
     git push origin main
     # OU
     git push origin aurora-f1-minimal-20260131

---

## PASSO 5: VALIDAR EXECUÇÃO (3 MINUTOS)
# ============================================================================

CHECKLIST_OBRIGATÓRIA (Marque cada item):

  ☐ Código commitado no branch correto
    Verificar: git log --oneline | head -5
    Deve mostrar seu commit recente
  
  ☐ Pipeline CI/CD executado com sucesso
    Ir em: https://github.com/simonnmarket/AURORA-Trading-System/actions
    Procure seu commit → deve estar ✅ GREEN
  
  ☐ Testes relevantes implementados/executados
    No Visual Code Terminal:
    npm test
    # OU
    python -m pytest
    # Todos testes devem passar ✅
  
  ☐ Documentação atualizada (se aplicável)
    Se criou novo arquivo/função, adicione comentários/README
  
  ☐ Plano de rollback definido/testado
    Anote como reverter se necessário:
    git revert [commit-sha]
    # Ou: git checkout main

---

## PASSO 6: PREENCHER RELATÓRIO DE CONCLUSÃO (RC) - 2 MINUTOS
# ============================================================================

ARQUIVO_RC_TEMPLATE:

  documento_tipo: "RELATORIO_CONCLUSAO_TIER-0"
  rc_id: "AURORA-RC-20260203-001-RESP"
  st_referencia: "AURORA-ST-20260201-001"
  
  execucao_real:
    cargo: "Tech Lead (IA Agent)"
    nome: "[TECH_LEAD_AGENT]"
    data_inicio_real: "2026-02-02T09:15:00+01:00"
    data_conclusao_real: "2026-02-03T16:42:00+01:00"
    tempo_total_execucao: "[quantas horas realmente levou]"
    status_final: "CONCLUIDO_COM_SUCESSO"  # ou CONCLUIDO_COM_AJUSTES
  
  resultados_execucao:
    checklist_concluida:
      - "[✅] Código commitado no branch correto (commit: COLOQUE_SHA_DO_SEU_COMMIT)"
      - "[✅] Pipeline CI/CD executado com sucesso (build #NUMERO)"
      - "[✅] Testes relevantes implementados/executados"
      - "[✅] Documentação atualizada"
      - "[✅] Plano de rollback definido/testado"
    
    evidencias_links:
      - "commit: https://github.com/simonnmarket/AURORA-Trading-System/commit/[SHA_DO_SEU_COMMIT]"
      - "pipeline: https://github.com/simonnmarket/AURORA-Trading-System/actions/runs/[RUN_ID]"
  
  transparencia_desvios:
    desvios_cronograma: []  # Se houve atraso, descreva
    pendencias_nao_bloqueantes: []  # Se ficou algo faltando

COMO_PREENCHER:
  1. Você já está em Visual Code
  2. Crie novo arquivo: AURORA-RC-[DATA]-001-RESP.yaml
  3. Copie template acima
  4. Preencha com seus dados reais
  5. Salve em: 00-Governance/INTELLIGENT-EXECUTION-CONTROL/RCs/
  6. Commit e push

---

## PASSO 7: REPORTAR RC PARA CEO
# ============================================================================

APÓS_COMPLETAR_RC:

  1. Faça commit do RC:
     git add 00-Governance/INTELLIGENT-EXECUTION-CONTROL/RCs/AURORA-RC-*.yaml
     git commit -m "AURORA-ST-20260201-001: Relatório Conclusão"
     git push origin main
  
  2. Reporte no chat para CEO:
     "RC COMPLETO - AURORA-ST-20260201-001"
     "Caminho: 00-Governance/INTELLIGENT-EXECUTION-CONTROL/RCs/AURORA-RC-[DATA]-001-RESP.yaml"
     "Commit: [SHA do seu último commit]"
     "Status: CONCLUIDO_COM_SUCESSO"
  
  3. Aguarde validação PSA

---

## PASSO 8: DÚVIDAS TÉCNICAS? REPORTE AQUI
# ============================================================================

SE_TIVER_DÚVIDA_SOBRE:

  ❓ Como fazer commit?
     → Dúvida Git → Reporte no chat
  
  ❓ Qual branch usar?
     → Reporte qual ST você recebeu → diremos branch certo
  
  ❓ Como executar testes?
     → Qual linguagem? → Reporte no chat
  
  ❓ Como preencher RC?
     → Reporte exatamente qual campo no chat
  
  ❓ Plano de rollback não é claro?
     → Descreva cenário → Reporte no chat

FORMAT_DÚVIDA:
  
  "DÚVIDA - AURORA-ST-[ID]: [sua pergunta técnica específica]"
  
  Exemplo:
  "DÚVIDA - AURORA-ST-20260201-001: Como faço revert se testes falharem?"

---

## RESUMO RÁPIDO (COPIE E COLE)
# ============================================================================

# 1. Receba ST via chat
# 2. Git pull origin main
# 3. Faça mudanças conforme ST
# 4. Git commit -m "AURORA-ST-20260201-001: descrição"
# 5. Git push origin main
# 6. Verifique: https://github.com/simonnmarket/AURORA-Trading-System/actions
# 7. Preencha RC (copie template acima)
# 8. Git push RC
# 9. Reporte RC no chat para CEO
# 10. Dúvidas? Use FORMAT_DÚVIDA acima

---

## LINKS IMPORTANTES
# ============================================================================

PROTOCOLO_AURORA_COMPLETO:
  https://github.com/simonnmarket/AURORA-Trading-System/blob/main/00-Governance/INTELLIGENT-EXECUTION-CONTROL/AURORA_ESSENTIAL_CONTROL_v2.1_SIMPLIFIED.yaml

REPOSITÓRIO:
  https://github.com/simonnmarket/AURORA-Trading-System

ACTIONS_PIPELINE:
  https://github.com/simonnmarket/AURORA-Trading-System/actions

DIRETÓRIO_STs:
  00-Governance/INTELLIGENT-EXECUTION-CONTROL/STs/

DIRETÓRIO_RCs:
  00-Governance/INTELLIGENT-EXECUTION-CONTROL/RCs/

---

## COMANDOS GIT MAIS USADOS (COPIE CONFORME PRECISA)
# ============================================================================

# Ver status
git status

# Ver branch atual
git branch

# Mudar para main
git checkout main

# Mudar para aurora-f1
git checkout aurora-f1-minimal-20260131

# Ver histórico de commits
git log --oneline

# Fazer pull (sincronizar)
git pull origin main

# Adicionar arquivos
git add .
# OU arquivos específicos
git add src/api/main.py

# Fazer commit
git commit -m "AURORA-ST-20260201-001: descrição"

# Push para GitHub
git push origin main

# Ver último commit SHA
git rev-parse HEAD

# Reverter um commit
git revert [SHA]

# Ver mudanças não commitadas
git diff

# Deletar branch local
git branch -d nome-branch

---

## ⚠️ IMPORTANTES
# ============================================================================

✅ SEMPRE use mensagem de commit com formato: AURORA-ST-[ID]: [descrição]

✅ SEMPRE valide checklist de aceitação ANTES de considerar pronto

✅ SEMPRE reporte desvios TRANSPARENTEMENTE no RC

✅ SE BLOQUEADO em algo, reporte IMEDIATAMENTE no chat (não espere)

✅ Dúvidas? USE FORMAT_DÚVIDA - seja específico e técnico

✅ Todas confirmações SEMPRE no chat com CEO

❌ NUNCA commit direto sem testar localmente

❌ NUNCA force push (git push -f) sem autorização

❌ NUNCA deixe RC em branco - preencha TODAS campos

---

## 🎯 VOCÊ ESTÁ PRONTO?
# ============================================================================

Se recebeu esta documentação:

✅ Você sabe o fluxo
✅ Você sabe os comandos
✅ Você sabe como reportar dúvidas NO CHAT
✅ Você tem links de acesso
✅ Você está operando em Visual Code

PRÓXIMO PASSO: Aguarde primeira ST do CEO via chat

Dúvidas AGORA? Use FORMAT_DÚVIDA acima E reporte no chat.

# ============================================================================
# FIM DO SCRIPT
# ============================================================================
