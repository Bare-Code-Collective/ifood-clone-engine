🍕 iFood Clone Engine - Baré Code Collective
Este repositório contém o "motor" (backend) do projeto de engenharia reversa do iFood. O foco desta aplicação é o desenvolvimento de um sistema robusto de geolocalização e um motor de recomendação inteligente.

🛠️ Tecnologias Utilizadas
Python 3.10+

FastAPI: Framework moderno e de alta performance.

Uvicorn: Servidor ASGI para rodar a aplicação.

Pydantic: Validação de dados e esquemas.

Python-dotenv: Gerenciamento de variáveis de ambiente.

🚀 Como Rodar o Projeto Localmente
1. Clonar o repositório:

Bash
git clone https://github.com/Bare-Code-Collective/ifood-clone-engine.git
cd ifood-clone-engine
2. Configurar o Ambiente Virtual (venv):

Bash
python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
3. Instalar as dependências:

Bash
pip install -r requirements.txt
4. Configurar as Variáveis de Ambiente:
Crie um arquivo .env na raiz do projeto e adicione as configurações necessárias (veja o modelo no .env.example, se houver).

5. Iniciar o Servidor:

Bash
uvicorn app.main:app --reload
A API estará disponível em: http://127.0.0.1:8000

📍 Endpoints Principais (MVP)
GET /: Health check da API.

GET /cardapio-regional: Rota de teste para validação de dados geográficos.

GET /docs: Documentação automática gerada pelo Swagger.

🤝 Como Contribuir
Crie uma Branch para sua tarefa: git checkout -b feat/nome-da-tarefa.

Realize o Commit com mensagens claras: git commit -m "feat: adiciona calculo de frete".

Envie para o GitHub (Push): git push origin feat/nome-da-tarefa.

Abra um Pull Request para revisão do time.
