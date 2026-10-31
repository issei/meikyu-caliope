## O que muda

<!-- Uma ou duas frases. Diga o problema e a mudança. -->

## Tipo

- [ ] Só documentação (entra sozinho na `main` se a CI passar — decisão D-08)
- [ ] Código, testes, CI, configuração do agente ou dados (espera o Issei)

## Rastreio

- Especificação ou ADR: <!-- ex.: 01-especificacao.md §12.1, ADR-ps-007, RF-24 -->
- Etapa do roteiro: <!-- E1, E2, E3, I2… -->

## Invariantes

- [ ] Nenhum dado real de pesquisa no PR (só fixtures com `"_fixture": true` ou hash registrado)
- [ ] Nenhuma saída do MCP ganha texto de resposta, situação, trecho ou identificação (ADR-ps-007)
- [ ] A natureza da base (fictícia ou real) continua obrigatória e imutável (ADR-ps-006)
- [ ] O núcleo `src/caliope/` não cita o estudo de streaming (ADR-ps-009)
- [ ] Nenhuma dependência de execução fora da biblioteca padrão
- [ ] Código copiado do `knowledge-os` tem cabeçalho de origem e linha em `docs/origem-do-codigo.md` (ADR-ps-008)

## Como verifiquei

<!-- Saída de `python scripts/verificar.py`, e o que não deu para verificar. -->
