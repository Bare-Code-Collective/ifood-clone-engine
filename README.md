# 🍕 iFood Clone Engine - Baré Code Collective

> **Status do Projeto:** 🛠️ Em desenvolvimento (Setup Inicial)

Este repositório contém o "motor" (backend) do projeto de engenharia reversa do iFood. Nosso foco é construir uma API de alta performance com geolocalização e um sistema de recomendação inteligente.

---

### 🛠️ Tecnologias Utilizadas
* **Python 3.14.3**
* **FastAPI:** Framework moderno e rápido.
* **Uvicorn:** Servidor ASGI.
* **Pydantic:** Validação de dados.

---

### 🚀 Como Rodar o Projeto Localmente

**1. Clonar o repositório:**
```bash
git clone https://github.com/Bare-Code-Collective/ifood-clone-engine.git
cd ifood-clone-engine
```
2. Configurar o Ambiente Virtual (venv):

```bash
# No Windows, garante venv com Python 3.14.3
py -3.14 -m venv venv

# No Windows:
.\venv\Scripts\activate
```
3. Instalar as dependências:

``` Bash
pip install -r requirements.txt
```
4. Iniciar o Servidor:

```Bash
uvicorn app.main:app --reload
```
Acesse em: http://127.0.0.1:8000

📍 Endpoints Atuais
GET /: Health check (Verifica se a API está online).

GET /docs: Documentação interativa (Swagger).

🤝 Guia de Contribuição (Baré Style)
  1- Crie uma Branch para sua tarefa: git checkout -b feat/nome-da-tarefa.

  2- Realize o Commit padrão: git commit -m "tipo: descrição curta".

  3- Envie para o GitHub: git push origin feat/nome-da-tarefa.

  4- Abra um Pull Request para o time revisar.
