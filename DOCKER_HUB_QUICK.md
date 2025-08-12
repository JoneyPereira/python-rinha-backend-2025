# 🐳 Docker Hub - Guia Rápido

## 🚀 Opções para Subir Imagens

### Opção 1: Script Python Automatizado
```bash
cd python-rinha-backend-2025
python docker-hub-push.py
```
- ✅ Mais fácil e interativo
- ✅ Solicita username automaticamente
- ✅ Cria docker-compose público
- ✅ Tratamento de erros

### Opção 2: Script Bash Manual
```bash
cd python-rinha-backend-2025
chmod +x docker-hub-manual.sh
./docker-hub-manual.sh SEU_USERNAME
```
- ✅ Comandos diretos
- ✅ Controle total
- ✅ Funciona em Linux/Mac

### Opção 3: Comandos Manuais
```bash
# 1. Login
docker login

# 2. Construir
docker build -t SEU_USERNAME/rinha-backend-2025-python:latest .

# 3. Push
docker push SEU_USERNAME/rinha-backend-2025-python:latest
```

## 📋 Pré-requisitos

1. **Conta no Docker Hub**: [hub.docker.com](https://hub.docker.com)
2. **Docker instalado** e funcionando
3. **Username do Docker Hub** (criar se não tiver)

## 🎯 Passos Rápidos

### 1. Criar Conta no Docker Hub
- Acesse [hub.docker.com](https://hub.docker.com)
- Clique em "Sign Up"
- Crie sua conta gratuita

### 2. Executar Script
```bash
cd python-rinha-backend-2025
python docker-hub-push.py
```

### 3. Seguir Instruções
- Digite seu username quando solicitado
- Digite suas credenciais do Docker Hub
- Aguarde o processo completar

### 4. Verificar
- Acesse [hub.docker.com](https://hub.docker.com)
- Faça login na sua conta
- Procure por `rinha-backend-2025-python`

## 📦 Usando a Imagem

### Para Outros Usuários
```bash
docker pull SEU_USERNAME/rinha-backend-2025-python:latest
docker-compose -f docker-compose.public.yml up -d
```

### Para Você Mesmo
```bash
# Atualizar imagem
docker pull SEU_USERNAME/rinha-backend-2025-python:latest

# Executar
docker-compose -f docker-compose.public.yml up -d
```

## 🔧 Troubleshooting

### Erro de Login
```bash
docker logout
docker login
```

### Erro de Push
```bash
# Verificar se está logado
docker whoami

# Verificar imagem
docker images

# Tentar novamente
docker push SEU_USERNAME/rinha-backend-2025-python:latest
```

### Erro de Build
```bash
# Limpar cache
docker system prune -a

# Reconstruir
docker build --no-cache -t SEU_USERNAME/rinha-backend-2025-python:latest .
```

## 📝 Arquivos Criados

Após o push, você terá:
- ✅ Imagem no Docker Hub: `SEU_USERNAME/rinha-backend-2025-python:latest`
- ✅ `docker-compose.public.yml` - Para uso público
- ✅ Logs do processo

## 🎉 Próximos Passos

1. **Teste a imagem publicada**:
   ```bash
   docker pull SEU_USERNAME/rinha-backend-2025-python:latest
   docker-compose -f docker-compose.public.yml up -d
   ```

2. **Atualize o info.json**:
   ```json
   {
     "docker-image": "SEU_USERNAME/rinha-backend-2025-python:latest"
   }
   ```

3. **Submeta para a Rinha** com a imagem pública!

---

**🎉 Sua implementação está pronta para o Docker Hub!** 