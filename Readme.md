
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

Não existem outros pré requisitos
