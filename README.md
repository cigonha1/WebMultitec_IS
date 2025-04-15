# Trabalho Prático: Desenvolvimento de Serviços Web Multitecnologia

**Discente:** Diogo Pedro (220000891)  
**Docente:** Filipe Madeira  
**Unidade Curricular:** Integração de Sistemas  

---

## Descrição  
Este projeto consiste no desenvolvimento de um sistema cliente-servidor utilizando múltiplas tecnologias de serviços web. O objetivo principal é demonstrar a integração e comunicação entre diferentes tecnologias, além de permitir a exportação e importação de dados nos formatos **XML e JSON**.  

### Tecnologias Utilizadas:
- **REST** – Flask + JSON Schema + JSONPath  
- **SOAP** – Spyne + Validação com XSD  
- **GraphQL** – Strawberry + FastAPI  
- **gRPC** – Python gRPC (Protobuf)  
- **Conversão entre JSON e XML**  
- **Validações rigorosas** com schemas  

---

## Requisitos  

Antes de começar, certifique-se de que o seu ambiente atende aos seguintes requisitos:  
- **Sistema Operacional:** Ubuntu  
- **Python:** Certifique-se de que o Python está instalado. Verifique a versão com:
  ```bash
  python --version
  ```
- **Pip:** Certifique-se de que o Pip está instalado. Verifique a versão com:
  ```bash
  pip --version
  ```
- **MobaXterm:** Para acesso SSH ao servidor. O IP do servidor é: `192.168.246.33`.  

⚠️ **Nota:** Docker **não foi utilizado** neste projeto. Todo o código foi desenvolvido no **VSCode** e o servidor foi configurado manualmente via SSH.

---

## Instalação  

### 1. Clonar o Repositório  
Para obter o código fonte, execute os seguintes comandos:  
```bash
git clone <URL_DO_REPOSITORIO>
cd <nome-do-repositorio>
```

### 2. Instalar Dependências  
Instale as dependências do projeto tanto no cliente como no servidor.  
```bash
pip install -r requirements.txt
```

---

## Configuração e Execução  

### Iniciar o Servidor SOAP:
```bash
python3 var/www/Dmgp/soap/soap_service.py
```

### Iniciar o Servidor REST:
```bash
python3 var/www/Dmgp/rest/rest_service.py
```

### Iniciar o Servidor GraphQL:
```bash
python3 var/www/Dmgp/graphql/graphql_service.py
```

### Iniciar o Servidor gRPC:
```bash
python3 var/www/Dmgp/grpc/grpc_service.py
```

---

## Exemplo de Chamadas (Postman)  

### SOAP  
#### Exemplo de Request (XML)
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://servicos.exemplo/">
   <soapenv:Header/>
   <soapenv:Body>
      <ser:getLivro>
         <id>2</id>
      </ser:getLivro>
   </soapenv:Body>
</soapenv:Envelope>
```

#### Exemplo de Response  
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soapenv:Body>
      <getLivroResponse>
         <livro>
            <id>2</id>
            <titulo>1984</titulo>
            <descricao>Um clássico de George Orwell sobre um futuro distópico.</descricao>
            <estado>pendente</estado>
         </livro>
      </getLivroResponse>
   </soapenv:Body>
</soapenv:Envelope>
```

---

#### Exemplo de Request: GET /livros/2
```http
GET http://192.168.246.33:55556/livros/2 HTTP/1.1
Host: 192.168.246.33
```

#### Exemplo de Response  
```json
[
  {
    "id": 2,
    "titulo": "1984",
    "descricao": "Um clássico de George Orwell sobre um futuro distópico.",
    "estado": "pendente"
  }
]
```

---

### GraphQL  
#### Exemplo de Request Body  
```json
{
  "query": "query { livro(id: 2) { titulo descricao estado } }"
}
```

#### Exemplo de Response  
```json
{
  "data": {
    "livro": {
      "titulo": "1984",
      "descricao": "Um clássico de George Orwell sobre um futuro distópico.",
      "estado": "pendente"
    }
  }
}
```

---

### gRPC  
#### Exemplo de Request 
```python
import grpc
from livros_pb2 import LivroRequest
from livros_pb2_grpc import LivrosStub

# Configuração do canal gRPC
channel = grpc.insecure_channel('192.168.246.33:55558')
client = LivrosStub(channel)

# Enviar a requisição
response = client.GetLivro(LivroRequest(id=2))

# Exibir a resposta
print(response)
```

#### Exemplo de Response  
```json
{
  "id": 2,
  "titulo": "1984",
  "descricao": "Um clássico de George Orwell sobre um futuro distópico.",
  "estado": "pendente"
}
```
```

---

## Prints dos Passos de Configuração  

Abaixo estão os prints capturados durante o processo de configuração do servidor:  

### 1. Remover o repositório do CD-ROM  
![Remover o repositório do CD-ROM](WebMultitec_IS/prints_configServer/Passo1.png)  

### 2. Atualizar os repositórios e instalar o Apache  
![Atualizar os repositórios e instalar o Apache](path/para/print2.png)  

### 3. Verificar se o serviço Apache está ativo  
![Verificar se o serviço Apache está ativo](path/para/print3.png)  

### 4. Garantir que o serviço Apache inicia automaticamente  
![Garantir que o serviço Apache inicia automaticamente](path/para/print4.png)  

### 5. Testar o servidor Apache  
![Testar o servidor Apache](path/para/print5.png)  

### 6. Apagar a página padrão do Apache  
![Apagar a página padrão do Apache](path/para/print6.png)  

### 7. Criar um ficheiro `index.html` de teste  
![Criar um ficheiro index.html de teste](path/para/print7.png)  

### 8. Configurar um Virtual Host  
![Configurar um Virtual Host](path/para/print8.png)  

### 9. Associar o domínio personalizado ao IP  
![Associar o domínio personalizado ao IP](path/para/print9.png)  

### 10. Testar o domínio personalizado  
![Testar o domínio personalizado](path/para/print10.png)  

---

## Estrutura do Projeto  

Abaixo está a estrutura do projeto, conforme exibido na imagem:

```
Trabalho Individual
│
├── AmbVirtualIS
│   ├── Lib
│   ├── Scripts
│   └── WebMultitec_IS
│       ├── cliente
│       │   ├── requests
│       │   │   ├── graphql_client.py
│       │   │   ├── grpc_client.py
│       │   │   ├── rest_client.py
│       │   │   └── soap_client.py
│       │   └── documentacao
│       │       └── requirements.txt
│       ├── Prints da configuração do Server
│       └── servidor
│           ├── data
│           │   └── livros.json
│           └── services
│               ├── graphql_service.py
│               ├── grpc_service.py
│               ├── rest_service.py
│               ├── soap_service.py
│               ├── livros_pb2_grpc.py
│               ├── livros_pb2.py
│               └── livros.proto

```