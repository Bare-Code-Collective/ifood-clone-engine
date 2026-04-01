# iFood Clone Engine - Data and Logistics Recommender

> Status: em evolucao para case de recomendacao com viabilidade logistica

Projeto de estudo para simular um motor de recomendacao de restaurantes que combina:
- preferencia do cliente
- qualidade do restaurante
- restricoes de entrega por localidade (distancia, ETA e frete)

## Stack
- Python 3.14.3
- FastAPI
- Pydantic
- Uvicorn

## Como executar
1. Clonar repositorio
```bash
git clone https://github.com/Bare-Code-Collective/ifood-clone-engine.git
cd ifood-clone-engine
```
2. Criar ambiente virtual
```bash
py -3.14 -m venv venv
.\venv\Scripts\activate
```
3. Instalar dependencias
```bash
pip install -r requirements.txt
```
4. Subir API
```bash
uvicorn app.main:app --reload
```

## Endpoints principais
- `GET /` health check
- `GET /restaurants` base mock de restaurantes
- `GET /recommendations/{user_id}?top_n=5&hour=20&raining=true&demand_level=high` ranking contextual com filtro logistico
- `GET /analytics/events/summary` metricas basicas
- `GET /simulation/run?runs=100&top_k=3&seed=42` simulacao de desempenho
- `GET /docs` swagger

## Logica de recomendacao (v0)
O ranking final usa score hibrido:

`score_final = 0.5 * preferencia + 0.3 * viabilidade + 0.2 * qualidade`

Viabilidade aplica regras:
- distancia maxima: 8 km
- ETA maxima: 45 min
- frete maximo: R$ 12,00
- restaurante aberto

## Estrutura tecnica
- `app/api/routes`: endpoints
- `app/services`: regras de negocio e ranking
- `app/schemas`: contratos de dados
- `app/core`: configuracoes e pesos
- `docs/`: analise de negocio, dados, modelagem e metricas

## Proximos passos
- Persistencia em banco
- Tracking de eventos
- Pipeline de features
- Modelo preditivo de proxima compra

## Simulacao e testes
Rodar simulacao offline e salvar resultado:
```bash
.\venv\Scripts\python scripts/simulate_data.py --runs 250 --top-k 3 --seed 42
```

A simulacao inclui contexto dinamico por sessao:
- chuva
- nivel de demanda (low/normal/high)
- horario de pico
- indisponibilidade operacional de restaurantes
- comparacao com baseline (mais proximo)

## Modo quase producao (v1)
- Recomendador contextual por hora/clima/demanda
- Regras de viabilidade aplicadas antes do ranking
- Simulador com cenarios operacionais e baseline para comparacao
- Testes automatizados de contrato e regressao basica

Rodar testes automatizados:
```bash
.\venv\Scripts\python -m pytest -q
```
