🐳 Desafio: Aplicação Flask + PostgreSQL com Docker
👤 Autor

Miguel Becker

🎯 Objetivo

Criar uma aplicação web Python (Flask) conectada a um banco de dados PostgreSQL, utilizando contêineres Docker.
A API permite inserir e listar mensagens armazenadas no banco via endpoints REST.

🧱 Estrutura do Projeto

Desafio-Docker/
├── app/
│ ├── app.py
│ ├── requirements.txt
│ └── Dockerfile
└── README.md

⚙️ Tecnologias utilizadas

Python 3.10

Flask

PostgreSQL 15

Docker

🚀 Passo a passo para execução

Criar uma rede Docker
docker network create minha-rede

Subir o banco de dados PostgreSQL
docker run -d --name meu-banco --network minha-rede -e POSTGRES_USER=MiguelBecker -e POSTGRES_PASSWORD=DesafioDocker123 -e POSTGRES_DB=Desafio_Docker -v pgdata:/var/lib/postgresql/data postgres:15

Construir a imagem da API Flask
docker build -t flask-db-app ./app

Executar o container da API Flask
docker run -d --name minha-api --network minha-rede -p 5000:5000 -e DB_HOST=meu-banco -e DB_NAME=Desafio_Docker -e DB_USER=MiguelBecker -e DB_PASS=DesafioDocker123 flask-db-app

✅ Testes de funcionamento

Verificar status da API
Acesse no navegador: http://localhost:5000/health

Resposta esperada: {"status": "ok"}

Inserir uma nova mensagem
curl -X POST -H "Content-Type: application/json" -d "{"texto":"Olá Docker Becker!"}" http://localhost:5000/mensagem

Resposta esperada: {"status": "mensagem salva", "id": 1}

Listar mensagens salvas
curl http://localhost:5000/mensagens

Resposta esperada: [{"id":1,"texto":"Olá Docker Becker!","criado_em":"2025-10-24T21:43:52"}]

🧩 Estrutura dos containers em execução

Verifique com:
docker ps

Exemplo:
CONTAINER ID IMAGE NAME STATUS PORTS
xxxxxxx flask-db-app minha-api Up 2 minutes 0.0.0.0:5000->5000/tcp
yyyyyyy postgres:15 meu-banco Up 5 minutes 5432/tcp

🧹 Comandos úteis

Parar e remover tudo:
docker rm -f minha-api meu-banco
docker volume rm pgdata
docker network rm minha-rede

Ver logs da API:
docker logs -f minha-api

🏁 Resultado Final

✅ API Flask funcional
✅ Banco PostgreSQL conectado via Docker
✅ Endpoints REST testados com sucesso
✅ Dados persistindo corretamente

Projeto desenvolvido por Miguel Becker — Desafio Docker / Flask / PostgreSQL 🐳

btw esse read.me foi puro gpt