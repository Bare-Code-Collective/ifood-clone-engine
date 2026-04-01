# Data Dictionary

## user_profile
- id: identificador do cliente
- preferred_cuisines: lista de categorias favoritas
- avg_spend_brl: ticket medio historico
- location(lat, lon): localizacao atual ou mais recente

## restaurant
- id: identificador do restaurante
- cuisine: categoria principal
- avg_ticket_brl: ticket medio
- rating: nota de qualidade (0 a 5)
- location(lat, lon): localizacao do restaurante
- is_open: disponibilidade operacional

## order_event
- user_id: cliente do pedido
- restaurant_id: restaurante escolhido
- total_brl: valor total
- hour: hora do pedido (0-23)

## recommendation_output
- score_preference: afinidade do cliente
- score_viability: adequacao logistica
- score_quality: qualidade do restaurante
- score_final: ranking final ponderado
