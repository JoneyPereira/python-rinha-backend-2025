# 🐳 Guia para Docker Hub - Rinha de Backend 2025 Python

## 📋 Pré-requisitos

1. **Conta no Docker Hub**: [hub.docker.com](https://hub.docker.com)
2. **Docker instalado** e funcionando
3. **Login no Docker Hub** localmente

## 🚀 Opções para Subir Imagens

### Opção 1: Script Automatizado (Recomendado)

```bash
cd python-rinha-backend-2025
python docker-hub-push.py
```

O script irá:
- ✅ Solicitar seu username do Docker Hub
- ✅ Fazer login automaticamente
- ✅ Construir e fazer tag das imagens
- ✅ Fazer push para o Docker Hub
- ✅ Criar docker-compose público

### Opção 2: Comandos Manuais

#### 1. Login no Docker Hub
```bash
docker login
# Digite seu username e password quando solicitado
```

#### 2. Construir e Fazer Tag da Imagem
```bash
# Substitua SEU_USERNAME pelo seu username do Docker Hub
docker build -t SEU_USERNAME/rinha-backend-2025-python:latest .
```

#### 3. Fazer Push da Imagem
```bash
docker push SEU_USERNAME/rinha-backend-2025-python:latest
```

#### 4. Criar docker-compose Público
```bash
# O script criará automaticamente o docker-compose.public.yml
# Ou você pode copiar o docker-compose.yml e alterar as imagens
```

## 📝 Exemplo Completo

```bash
# 1. Login no Docker Hub
docker login

# 2. Construir imagem
docker build -t meuusername/rinha-backend-2025-python:latest .

# 3. Fazer push
docker push meuusername/rinha-backend-2025-python:latest

# 4. Verificar se foi enviada
docker search meuusername/rinha-backend-2025-python
```

## 🔍 Verificando o Push

### 1. No Docker Hub Web
- Acesse [hub.docker.com](https://hub.docker.com)
- Faça login na sua conta
- Vá para "Repositories"
- Procure por `rinha-backend-2025-python`

### 2. Via Command Line
```bash
# Buscar sua imagem
docker search SEU_USERNAME/rinha-backend-2025-python

# Ver detalhes da imagem
docker inspect SEU_USERNAME/rinha-backend-2025-python:latest
```

## 📦 Usando a Imagem Publicada

### Para Outros Usuários
```bash
# Baixar a imagem
docker pull SEU_USERNAME/rinha-backend-2025-python:latest

# Usar com docker-compose.public.yml
docker-compose -f docker-compose.public.yml up -d
```

### Para Você Mesmo
```bash
# Baixar a imagem (atualizar)
docker pull SEU_USERNAME/rinha-backend-2025-python:latest

# Executar
docker-compose -f docker-compose.public.yml up -d
```

## 🏷️ Tags e Versões

### Tag Padrão
```bash
# Latest (recomendado para Rinha)
docker build -t SEU_USERNAME/rinha-backend-2025-python:latest .
docker push SEU_USERNAME/rinha-backend-2025-python:latest
```

### Tags com Versão
```bash
# Versão específica
docker build -t SEU_USERNAME/rinha-backend-2025-python:v1.0.0 .
docker push SEU_USERNAME/rinha-backend-2025-python:v1.0.0

# Múltiplas tags
docker build -t SEU_USERNAME/rinha-backend-2025-python:latest -t SEU_USERNAME/rinha-backend-2025-python:v1.0.0 .
docker push SEU_USERNAME/rinha-backend-2025-python:latest
docker push SEU_USERNAME/rinha-backend-2025-python:v1.0.0
```

## 🔧 Configuração para Rinha de Backend 2025

### info.json Atualizado
```json
{
    "name": "Seu Nome",
    "social": ["https://github.com/seu-usuario"],
    "source-code-repo": "https://github.com/seu-usuario/rinha-backend-2025",
    "langs": ["python"],
    "storages": ["postgresql", "redis"],
    "messaging": ["redis"],
    "load-balancers": ["nginx"],
    "other-technologies": ["fastapi", "sqlalchemy", "docker", "docker-compose"],
    "docker-image": "SEU_USERNAME/rinha-backend-2025-python:latest"
}
```

### README.md Atualizado
```markdown
## 🐳 Docker Hub

Esta implementação está disponível no Docker Hub:

```bash
docker pull SEU_USERNAME/rinha-backend-2025-python:latest
docker-compose -f docker-compose.public.yml up -d
```

## 📊 Métricas da Imagem

### Tamanho da Imagem
```bash
docker images SEU_USERNAME/rinha-backend-2025-python:latest
```

### Informações da Imagem
```bash
docker inspect SEU_USERNAME/rinha-backend-2025-python:latest
```

## 🚨 Troubleshooting

### Erro de Login
```bash
# Limpar credenciais
docker logout

# Fazer login novamente
docker login
```

### Erro de Push
```bash
# Verificar se está logado
docker whoami

# Verificar se a imagem existe
docker images

# Tentar push novamente
docker push SEU_USERNAME/rinha-backend-2025-python:latest
```

### Erro de Build
```bash
# Limpar cache do Docker
docker system prune -a

# Reconstruir
docker build --no-cache -t SEU_USERNAME/rinha-backend-2025-python:latest .
```

## 📋 Checklist para Submissão

- ✅ [ ] Conta no Docker Hub criada
- ✅ [ ] Login no Docker Hub realizado
- ✅ [ ] Imagem construída com sucesso
- ✅ [ ] Push realizado com sucesso
- ✅ [ ] Imagem visível no Docker Hub
- ✅ [ ] docker-compose.public.yml criado
- ✅ [ ] info.json atualizado com docker-image
- ✅ [ ] README.md atualizado com instruções

## 🎯 Próximos Passos

1. **Execute o script automatizado**:
   ```bash
   python docker-hub-push.py
   ```

2. **Verifique no Docker Hub** se a imagem foi enviada

3. **Teste a imagem publicada**:
   ```bash
   docker pull SEU_USERNAME/rinha-backend-2025-python:latest
   docker-compose -f docker-compose.public.yml up -d
   ```

4. **Atualize o info.json** com a referência da imagem

5. **Submeta para a Rinha** com a imagem pública!

---

**🎉 Sua implementação está pronta para ser compartilhada no Docker Hub!** 