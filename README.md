# Trabalho Prático: Desenvolvimento de Serviços Web Multitecnologia

**Discente:** Diogo Pedro (220000891)  
**Docente:** Filipe Madeira  
**Unidade Curricular:** Integração de Sistemas  

## Descrição  
Este projeto consiste no desenvolvimento de um sistema cliente-servidor utilizando múltiplas tecnologias de serviços web, nomeadamente:  

- **SOAP** (com validação XSD)  
- **REST** (com validação JSON Schema e consultas JSONPath)  
- **GraphQL** (queries e mutations)  
- **gRPC** (serviços unários e streaming)  

O objetivo é demonstrar a integração e comunicação entre diferentes tecnologias, além de permitir a exportação e importação de dados nos formatos **XML e JSON**.  

---

## Requisitos
Antes de começar, certifica-te de que tens instalados:

- **Ubuntu**
- **Python** (`python --version`)
- **Pip** (`pip --version`)

---

## Instalação
As dependências devem ser instaladas tanto no servidor como no cliente. Para isso, executa:

### 1. Clonar o Repositório  
```bash
git clone <URL_DO_REPOSITORIO>
cd <nome-do-repositorio>
```

### 2. Instalar Dependências  
```bash
pip install -r requirements.txt
```
---

## Configuração e Execução  

### Iniciar o Servidor SOAP:
```bash
python servidor/services/soap_service.py
```

### Iniciar o Servidor REST:
```bash
python servidor/services/rest_service.py
```

### Iniciar o Servidor GraphQL:
```bash
python servidor/services/graphql_service.py
```

### Iniciar o Servidor gRPC:
```bash
python servidor/services/grpc_service.py
```
---

## Exemplo de Chamadas (Postman)  

---

## Esquemas de Validação  



