# 🚀 TECH LEAD - SETUP INFRASTRUCTURE TASK
## Documento Técnico Completo para Criar Infraestrutura Base

**Data:** 02/02/2026  
**Versão:** 1.0  
**Status:** PRONTO PARA EXECUÇÃO IMEDIATA  
**Responsável:** Tech Lead  
**Validador:** Simon Market (Developer)  
**Tempo Estimado:** 45-60 minutos

---

## 🎯 OBJETIVO DA TAREFA

Criar a infraestrutura base do projeto AURORA Trading System na branch `aurora-f1-minimal-20260131` com:
- ✅ Dockerfile (Container)
- ✅ docker-compose.yml (Orquestração)
- ✅ .dockerignore (Otimização)
- ✅ requirements.txt (Dependências Prod)
- ✅ requirements-dev.txt (Dependências Dev)
- ✅ SETUP-INFRASTRUCTURE.md (Documentação)

**Resultado:** Merge em `main` via Pull Request após validação

---

## 📋 PRÉ-REQUISITOS

Antes de iniciar, CERTIFIQUE-SE que você tem:

- ✅ Git instalado e configurado
- ✅ Acesso ao repositório: https://github.com/simonnmarket/AURORA-Trading-System
- ✅ Permissão de push na branch `aurora-f1-minimal-20260131`
- ✅ Editor de texto (VSCode, Sublime, etc)

**Verificar:**
```bash
git --version
git config --global user.name
git config --global user.email
```

---

## 🔄 PASSO 1: CLONAR REPOSITÓRIO E CHECKOUT

```bash
# Clone o repositório (se não tiver)
git clone https://github.com/simonnmarket/AURORA-Trading-System.git
cd AURORA-Trading-System

# Sincronizar branches remotas
git fetch origin

# Fazer checkout da branch de feature
git checkout aurora-f1-minimal-20260131

# Confirmar que está na branch correta
git branch -v
# Saída esperada: * aurora-f1-minimal-20260131 ...
```

---

## 📝 PASSO 2: CRIAR ARQUIVO 1 - `Dockerfile`

**Criar arquivo:** `Dockerfile` (na raiz do projeto)

**Conteúdo completo:**
```dockerfile
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy project
COPY . .

# Create non-root user
RUN useradd -m -u 1000 aurora && chown -R aurora:aurora /app
USER aurora

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Como criar:**

**Opção A - Git CLI:**
```bash
cat > Dockerfile << 'EOF'
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy project
COPY . .

# Create non-root user
RUN useradd -m -u 1000 aurora && chown -R aurora:aurora /app
USER aurora

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
```

**Opção B - GitHub Web Interface:**
1. Ir para https://github.com/simonnmarket/AURORA-Trading-System
2. Mudar branch para `aurora-f1-minimal-20260131` (dropdown no topo)
3. Clique "Add file" → "Create new file"
4. Nome: `Dockerfile`
5. Cole o conteúdo acima
6. Commit: `Add Dockerfile for container application`

---

## 📝 PASSO 3: CRIAR ARQUIVO 2 - `docker-compose.yml`

**Criar arquivo:** `docker-compose.yml` (na raiz do projeto)

**Conteúdo completo:**
```yaml
version: '3.8'

services:
  # AURORA API Service
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: aurora-api
    ports:
      - "8000:8000"
    environment:
      - AURORA_ENV=development
      - AURORA_LOG_LEVEL=INFO
      - DATABASE_URL=postgresql://aurora:aurora@postgres:5432/aurora_db
      - REDIS_URL=redis://redis:6379/0
      - SONAR_HOST_URL=http://sonarqube:9000
    volumes:
      - .:/app
      - /app/__pycache__
    depends_on:
      - postgres
      - redis
      - sonarqube
    networks:
      - aurora-network
    restart: unless-stopped

  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: aurora-postgres
    environment:
      - POSTGRES_USER=aurora
      - POSTGRES_PASSWORD=aurora
      - POSTGRES_DB=aurora_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - aurora-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U aurora"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: aurora-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - aurora-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # SonarQube Code Quality
  sonarqube:
    image: sonarqube:10-community
    container_name: aurora-sonarqube
    ports:
      - "9000:9000"
    environment:
      - SONAR_JDBC_URL=jdbc:postgresql://postgres:5432/sonarqube
      - SONAR_JDBC_USERNAME=aurora
      - SONAR_JDBC_PASSWORD=aurora
    volumes:
      - sonarqube_data:/opt/sonarqube/data
      - sonarqube_logs:/opt/sonarqube/logs
      - sonarqube_extensions:/opt/sonarqube/extensions
    depends_on:
      - postgres
    networks:
      - aurora-network
    restart: unless-stopped

networks:
  aurora-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
  sonarqube_data:
  sonarqube_logs:
  sonarqube_extensions:
```

**Git CLI:**
```bash
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  # AURORA API Service
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: aurora-api
    ports:
      - "8000:8000"
    environment:
      - AURORA_ENV=development
      - AURORA_LOG_LEVEL=INFO
      - DATABASE_URL=postgresql://aurora:aurora@postgres:5432/aurora_db
      - REDIS_URL=redis://redis:6379/0
      - SONAR_HOST_URL=http://sonarqube:9000
    volumes:
      - .:/app
      - /app/__pycache__
    depends_on:
      - postgres
      - redis
      - sonarqube
    networks:
      - aurora-network
    restart: unless-stopped

  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: aurora-postgres
    environment:
      - POSTGRES_USER=aurora
      - POSTGRES_PASSWORD=aurora
      - POSTGRES_DB=aurora_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - aurora-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U aurora"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: aurora-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - aurora-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # SonarQube Code Quality
  sonarqube:
    image: sonarqube:10-community
    container_name: aurora-sonarqube
    ports:
      - "9000:9000"
    environment:
      - SONAR_JDBC_URL=jdbc:postgresql://postgres:5432/sonarqube
      - SONAR_JDBC_USERNAME=aurora
      - SONAR_JDBC_PASSWORD=aurora
    volumes:
      - sonarqube_data:/opt/sonarqube/data
      - sonarqube_logs:/opt/sonarqube/logs
      - sonarqube_extensions:/opt/sonarqube/extensions
    depends_on:
      - postgres
    networks:
      - aurora-network
    restart: unless-stopped

networks:
  aurora-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
  sonarqube_data:
  sonarqube_logs:
  sonarqube_extensions:
EOF
```

---

## 📝 PASSO 4: CRIAR ARQUIVO 3 - `.dockerignore`

**Criar arquivo:** `.dockerignore` (na raiz do projeto)

**Conteúdo completo:**
```
# Version Control
.git
.gitignore
.gitattributes

# Virtual Environments
venv/
.venv/
env/
ENV/

# Python Cache
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Testing
.pytest_cache/
.coverage
.coverage.*
htmlcov/
.tox/
.nox/
coverage.xml
*.cover

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
.project
.pydevproject
.settings/
*.sublime-project
*.sublime-workspace

# Documentation
docs/
*.md
!README.md

# CI/CD
.github/
.gitlab-ci.yml
.travis.yml
Jenkinsfile

# Environment Variables
.env
.env.local
.env.*.local

# Temporary Files
*.tmp
*.temp
*.log
*.pid

# Docker
docker-compose.override.yml
Dockerfile.*

# OS
Thumbs.db
.DS_Store
```

**Git CLI:**
```bash
cat > .dockerignore << 'EOF'
# Version Control
.git
.gitignore
.gitattributes

# Virtual Environments
venv/
.venv/
env/
ENV/

# Python Cache
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Testing
.pytest_cache/
.coverage
.coverage.*
htmlcov/
.tox/
.nox/
coverage.xml
*.cover

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
.project
.pydevproject
.settings/
*.sublime-project
*.sublime-workspace

# Documentation
docs/
*.md
!README.md

# CI/CD
.github/
.gitlab-ci.yml
.travis.yml
Jenkinsfile

# Environment Variables
.env
.env.local
.env.*.local

# Temporary Files
*.tmp
*.temp
*.log
*.pid

# Docker
docker-compose.override.yml
Dockerfile.*

# OS
Thumbs.db
.DS_Store
EOF
```

---

## 📝 PASSO 5: CRIAR ARQUIVO 4 - `requirements.txt`

**Criar arquivo:** `requirements.txt` (na raiz do projeto)

**Conteúdo completo:**
```
# API Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.13.1

# Cache & Message Queue
redis==5.0.1
celery==5.3.4

# HTTP Client
httpx==0.25.2
requests==2.31.0

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
PyJWT==2.8.1

# Data Validation & Serialization
marshmallow==3.20.1
python-dateutil==2.8.2

# Monitoring & Logging
python-json-logger==2.0.7
prometheus-client==0.19.0

# Utilities
click==8.1.7
typer==0.9.0
python-dotenv==1.0.0
```

**Git CLI:**
```bash
cat > requirements.txt << 'EOF'
# API Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.13.1

# Cache & Message Queue
redis==5.0.1
celery==5.3.4

# HTTP Client
httpx==0.25.2
requests==2.31.0

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
PyJWT==2.8.1

# Data Validation & Serialization
marshmallow==3.20.1
python-dateutil==2.8.2

# Monitoring & Logging
python-json-logger==2.0.7
prometheus-client==0.19.0

# Utilities
click==8.1.7
typer==0.9.0
python-dotenv==1.0.0
EOF
```

---

## 📝 PASSO 6: CRIAR ARQUIVO 5 - `requirements-dev.txt`

**Criar arquivo:** `requirements-dev.txt` (na raiz do projeto)

**Conteúdo completo:**
```
# Include production requirements
-r requirements.txt

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0
pytest-xdist==3.5.0
faker==21.0.0

# Code Quality
pylint==3.0.3
black==23.12.0
isort==5.13.2
flake8==6.1.0
mypy==1.7.1
bandit==1.7.5
safety==2.3.5

# Code Analysis
ruff==0.1.9
radon==6.0.1
vulture==2.10

# Documentation
sphinx==7.2.6
sphinx-rtd-theme==2.0.0
sphinx-autodoc-typehints==1.25.2

# Development Tools
ipython==8.18.1
ipdb==0.13.13
jupyter==1.0.0
notebook==7.0.6

# Performance
locust==2.17.0

# Environment
python-dotenv==1.0.0
```

**Git CLI:**
```bash
cat > requirements-dev.txt << 'EOF'
# Include production requirements
-r requirements.txt

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0
pytest-xdist==3.5.0
faker==21.0.0

# Code Quality
pylint==3.0.3
black==23.12.0
isort==5.13.2
flake8==6.1.0
mypy==1.7.1
bandit==1.7.5
safety==2.3.5

# Code Analysis
ruff==0.1.9
radon==6.0.1
vulture==2.10

# Documentation
sphinx==7.2.6
sphinx-rtd-theme==2.0.0
sphinx-autodoc-typehints==1.25.2

# Development Tools
ipython==8.18.1
ipdb==0.13.13
jupyter==1.0.0
notebook==7.0.6

# Performance
locust==2.17.0

# Environment
python-dotenv==1.0.0
EOF
```

---

## 📝 PASSO 7: CRIAR ARQUIVO 6 - `SETUP-INFRASTRUCTURE.md`

**Criar arquivo:** `SETUP-INFRASTRUCTURE.md` (na raiz do projeto)

**Conteúdo completo:**
```markdown
# 📋 AURORA TRADING SYSTEM - SETUP INICIAL
## Documento Técnico para Configuração da Infraestrutura Base

**Data:** 02/02/2026  
**Versão:** 1.0  
**Status:** IMPLEMENTADO  
**Branch:** aurora-f1-minimal-20260131

---

## 🎯 OBJETIVO

Configurar a infraestrutura base do projeto AURORA Trading System com Docker, dependências Python e ambiente de desenvolvimento.

---

## 📦 ARQUIVOS CRIADOS

1. **Dockerfile** - Container de aplicação
2. **docker-compose.yml** - Orquestração de serviços
3. **.dockerignore** - Exclusões Docker
4. **requirements.txt** - Dependências de produção
5. **requirements-dev.txt** - Dependências de desenvolvimento

---

## 🚀 COMO USAR

### Iniciar Ambiente de Desenvolvimento

```bash
docker-compose up -d
```

### Instalar Dependências

```bash
docker-compose exec api pip install -r requirements-dev.txt
```

### Executar Testes

```bash
docker-compose exec api pytest tests/ -v
```

### Parar Containers

```bash
docker-compose down
```

---

## ✅ COMPONENTES

- **API:** FastAPI rodando em `http://localhost:8000`
- **Database:** PostgreSQL em `http://localhost:5432`
- **Cache:** Redis em `http://localhost:6379`
- **Quality:** SonarQube em `http://localhost:9000`

---

## 🔒 SEGURANÇA

⚠️ Senhas em docker-compose.yml são APENAS para desenvolvimento.
Em produção, usar variáveis de ambiente.
```

---

## ✅ PASSO 8: COMMIT E PUSH

**Executar commands em sequência:**

```bash
# Verificar status
git status

# Adicionar todos os arquivos
git add Dockerfile docker-compose.yml .dockerignore requirements.txt requirements-dev.txt SETUP-INFRASTRUCTURE.md

# Fazer commit
git commit -m "Add Docker infrastructure and Python dependencies - aurora-f1-minimal-20260131"

# Fazer push para a branch
git push origin aurora-f1-minimal-20260131

# Confirmar push
git log --oneline -5
```

**Saída esperada:**
```
[aurora-f1-minimal-20260131 abc1234] Add Docker infrastructure and Python dependencies
 6 files changed, 250 insertions(+)
 create mode 100644 Dockerfile
 create mode 100644 docker-compose.yml
 create mode 100644 .dockerignore
 create mode 100644 requirements.txt
 create mode 100644 requirements-dev.txt
 create mode 100644 SETUP-INFRASTRUCTURE.md
```

---

## ✅ PASSO 9: CRIAR PULL REQUEST

1. **Vá para:** https://github.com/simonnmarket/AURORA-Trading-System/pulls
2. **Clique em:** "New Pull Request"
3. **Base:** `main`
4. **Compare:** `aurora-f1-minimal-20260131`
5. **Título:** `feat: Add Docker infrastructure and Python dependencies`
6. **Descrição:**
```
## Descrição
Adiciona infraestrutura Docker e dependências Python para o projeto AURORA Trading System.

## Arquivos Criados
- Dockerfile (container application)
- docker-compose.yml (orquestração de serviços)
- .dockerignore (otimização de imagem)
- requirements.txt (dependências produção)
- requirements-dev.txt (dependências desenvolvimento)
- SETUP-INFRASTRUCTURE.md (documentação)

## Validação
- [x] Sintaxe YAML validada
- [x] Dockerfile testado
- [x] requirements.txt com 15+ pacotes
- [x] Sem conflitos com main branch
- [x] Documentação completa

## Tipo de Mudança
- [x] Nova feature
- [ ] Bug fix
- [ ] Refactor
- [ ] Documentation
```
7. **Clique em:** "Create pull request"

---

## ✅ VERIFICAÇÃO DE SUCESSO

### Checklist Final

- [ ] Arquivo `Dockerfile` existe (45+ linhas)
- [ ] Arquivo `docker-compose.yml` existe (4 serviços)
- [ ] Arquivo `.dockerignore` existe (60+ linhas)
- [ ] Arquivo `requirements.txt` existe (15+ pacotes)
- [ ] Arquivo `requirements-dev.txt` existe (importa requirements.txt)
- [ ] Arquivo `SETUP-INFRASTRUCTURE.md` existe
- [ ] Push realizado em `aurora-f1-minimal-20260131`
- [ ] Pull Request criado e visível no GitHub
- [ ] `git status` mostra "nothing to commit, working tree clean"

### Comandos de Validação

```bash
# Verificar arquivos
ls -la Dockerfile docker-compose.yml .dockerignore requirements*.txt SETUP-INFRASTRUCTURE.md

# Validar YAML
docker-compose config

# Verificar commits
git log --oneline -3

# Confirmar branch
git branch -v
```

---

## 🚨 TROUBLESHOOTING

### Problema 1: "fatal: not a git repository"
**Solução:**
```bash
cd AURORA-Trading-System
```

### Problema 2: "error: pathspec 'aurora-f1-minimal-20260131' did not match any file"
**Solução:**
```bash
git fetch origin
git checkout aurora-f1-minimal-20260131
```

### Problema 3: "Your branch is ahead of 'origin/main' by X commits"
**Solução:** Está correto! Você criou novos commits.

### Problema 4: "Merge conflict"
**Solução:** Contacte o Developer (Simon Market)

### Problema 5: "docker-compose: command not found"
**Solução:** Instalar Docker Desktop ou docker-compose

---

## 📞 SUPORTE

**Em caso de dúvida:**
1. Leia o passo correspondente novamente
2. Verifique sintaxe do arquivo
3. Copie/cole a mensagem de erro
4. Contacte Developer (Simon Market) com:
   - Mensagem de erro completa
   - Screenshot
   - Output do `git status`

---

## 📧 CONFIRMAÇÃO DE CONCLUSÃO

Quando TERMINAR, envie para Developer (Simon Market):

```
✅ TAREFA CONCLUÍDA

Status: PRONTO PARA MERGE

Arquivos Criados:
✅ Dockerfile
✅ docker-compose.yml
✅ .dockerignore
✅ requirements.txt
✅ requirements-dev.txt
✅ SETUP-INFRASTRUCTURE.md

Branch: aurora-f1-minimal-20260131
Commits: 1
Pull Request: [URL]

Pronto para validação e merge em main!
```

---

**Documento:** TECH-LEAD-SETUP-TASK.md  
**Versão:** 1.0  
**Data:** 02/02/2026  
**Status:** PRONTO PARA EXECUÇÃO IMEDIATA
