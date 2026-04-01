# API Design

## Endpoints atuais
- GET `/` health check
- GET `/restaurants` lista de restaurantes mock
- GET `/recommendations/{user_id}?top_n=5` ranking viavel e personalizado
- GET `/analytics/events/summary` metricas basicas de pedidos

## Contrato principal
`/recommendations/{user_id}` retorna:
- usuario
- categoria prevista para proxima compra
- lista top-N com scores e justificativas

## Evolucao prevista
- POST `/events` para tracking real
- POST `/orders` para fluxo transacional
- GET `/recommendations/{user_id}/explain` para explicabilidade detalhada
