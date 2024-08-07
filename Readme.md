
## Installation

execute o docker compose diretamente

```
$ docker compose -f __docker/compose.yaml up --build
```

O composer do docker sobe um banco de dados mysql responsável
pela persistências dos dados.

Ao mesmo tempo um conjunto de serviços ASGI deve subir ao mesmo tempo
através da integração Gunicorn/Uvicorn respondendo na porta 8000

Após a aplicação subir, deve ser executado

`` 
db/migration/V0001_01_init.sql
``

Esse script cria as tabelas e um usuário apto a executar o login
e gerar o token implementado pelo JWT

Há uma pasta no projeto chamada

``
src/main/test
``

Neste local se encontrar os aquivos que testam os "controllers"
e realizam as requisições 

Deve ser seguida a seguinte ordem:

1. app.user_login.http (Gera o token com a autenticação do usuario carregado no sistema)
2. create_user.http (Cria mais usuarios com acesso ao JWT)
3. create_single_credit_card_.http (Cria um único cartão de crédito associado ao owner através de uma requisição HTTP)
4. batch_create_credit_card.http (Cria cartões associado a um usuário por meio de arquivo)
5. find_credit_card_number.http (Recupera os dados do cartão e seu proprietário se ele existir)

O arquivo usado para carga é o ``flat_data.txt`` na pasta ``/file_ingestion/``

Não existem outros pré requisitos além do .env

ENVIRONMENT=development

DEBUG=Truen

SECRET_KEY=sJm}nwNZHt/?M)Y5DF'j_p4rf^S83-.U2(VaC$,d>&y{+v9*P;

JWT_SECRET_KEY=MX9)0x*A*obnNMtX6ujTG#2ZUG+0zAjBXccn?geZ}a#kMi=qHF

LANGFLOW_SECRET_KEY=VUG6KEhFGtODPZyhP0Stw2U9dnPKE5kHOM5zS_U8U_E=

UPLOAD_FOLDER =/home/ppacheco/workspace/python-projects/hyperativa-challenge-api/file_ingestion

ALLOWED_EXTENSIONS={'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

SQLALCHEMY_DATABASE_URI=mysql+pymysql://admin:qjXy9VDs8Cz4r5emEhubWF7g@database:3306/hyperativa

