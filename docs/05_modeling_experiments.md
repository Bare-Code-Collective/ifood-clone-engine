# Modeling Experiments

## Baseline 1
Ranking por categoria favorita + restaurantes mais proximos e abertos.

## Baseline 2
Categoria mais frequente do historico recente do cliente.

## Modelo inicial (hibrido)
score_final =
0.5 * score_preference +
0.3 * score_viability +
0.2 * score_quality

## Proximos experimentos
- Modelo de classificacao de proxima categoria
- Aprendizado de rank (Learning to Rank)
- Re-ranking por custo logistico em tempo real
