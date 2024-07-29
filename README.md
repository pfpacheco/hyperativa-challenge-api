* O projeto segue as especificações recomendadas de acordo com as instruções disponibilizadas pela Hyperativa para o desenvolvimento do Desafio Técnico

* Para a execução do arquivo é necessário ambiente Linux preferencialmente.

* O arquio .env deve ser criado na raiz do projeto com o seguinte conteúdo

--'.env'
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=sJm}nwNZHt/?M)Y5DF'j_p4rf^S83-.U2(VaC$,d>&y{+v9*P;
JWT_SECRET_KEY=MX9)0x*A*obnNMtX6ujTG#2ZUG+0zAjBXccn?geZ}a#kMi=qHF
UPLOAD_FOLDER =/home/ppacheco/workspace/python-projects/hyperativa-challenge-api/file_ingestion
ALLOWED_EXTENSIONS={'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
SQLALCHEMY_DATABASE_URI=mysql+pymysql://a
