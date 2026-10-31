# meikyu-caliope

Backend local de apoio a pesquisas qualitativas, com servidor MCP.

Ele importa respostas de entrevistas em JSON, preserva o arquivo original e organiza trechos, códigos, temas e achados. Todo achado tem rastro até a resposta de origem. As análises são determinísticas e reproduzíveis. Um LLM pode orquestrar o trabalho por MCP, mas não lê o conteúdo das respostas. Aceitar ou rejeitar uma interpretação é sempre um ato humano, feito pela linha de comando.

Primeiro estudo: acessibilidade em serviços de streaming de vídeo no Brasil (Liga Web Para Todos).

## Estado

Especificação e ambiente de desenvolvimento prontos. O produto ainda não foi implementado (próxima etapa: E1).

- Especificação: [`docs/especificacao/`](docs/especificacao/README.md)
- Decisões de arquitetura (aceitas em 30/10/2026): [`docs/especificacao/03-adrs.md`](docs/especificacao/03-adrs.md)
- Protocolo para agentes: [`AGENTS.md`](AGENTS.md)
- CI/CD: [`docs/ci-cd.md`](docs/ci-cd.md)

## Verificar

```bash
python scripts/verificar.py
```

## Dados

Este repositório nunca recebe respostas reais. As únicas respostas aqui são fictícias, em `docs/especificacao/anexos/` e, a partir da etapa E1, em `tests/fixtures/ficticio/`. A CI e o hook do agente bloqueiam base SQLite, exportação real e JSON de resposta sem marca de fixture.
