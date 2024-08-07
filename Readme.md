
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


PS:

- Foi ajustado alguns tratamentos de erro da controller para que fosse possível também escrever um teste com pytest como um unittest simples que apoiasse o conhecimento técnico, não apenas em requisições http como nos testes python

- A consulta ao cartão foi substituída pelo uso da id do header na url da request para impedir que os dados sensíveis sejam usados como parâmetro, para portadores com mais de um cartão é trazida a lista dos mesmos

- Foi incluído para os cartões de crédito a criptografia dos dados de cartão no nível da controller, os dados de cartão de crédito estão sendo gravados na base de forma criptografada baseada em uma chave no arquivo env, eles são decriptografados no retorno ao usuário

- Todos os retornos de dados de cartão trazem apenas os 4 primeiros e 4 últimos dígitos dos 16 legíveis

- Foi incluído para o password tanto na criação do usuário, como na consulta ao acesso e login o password criptografado tal qual o número do cartão de crédito, a tabela também foi modificada para comportar a senha criptografada

- Como discutimos, pode ser também uma "symmetric encryption" se houver como fazer isso, no caso seria imprudente deixar o Fernet gerar a key, sob risco de produzir "side-effects"
*** É importante destacar que só isso não garante a segurança da app, além do jwt é necessário algo que não discutimos hoje, mas configuração do HTTPS respondendo na porta segura 443, por meio do SSL. ****

