---
id: CAL-APRENDIZADOS-01
titulo: Aprendizados para não tropeçar duas vezes
data: 2026-10-31
leitor: qualquer agente ou pessoa antes de uma tarefa grande neste repositório
padrao_de_redacao: ABNT NBR ISO 24495-1 (linguagem simples) e ASD-STE100 adaptado ao PT-BR
---

# Aprendizados

Só inclusão. Um item por lição: contexto → lição. Os primeiros itens vêm do `mauricio-site` e do `knowledge-os`.

- **Afirmação de memória sobre outro repositório** (`05-metacognicao.md` §1): duas de cinco afirmações sobre o `knowledge-os` estavam erradas. → Leia o arquivo inteiro, no commit citado, antes de afirmar ou copiar.
- **Merge automático pulado** (`knowledge-os`, PR #14): o GitHub pula um job quando um job anterior da cadeia foi pulado, mesmo com o job de resumo verde. → Todo job depois de jobs condicionais usa `!cancelled()`. Há teste para isso.
- **Merge pelo `GITHUB_TOKEN` não dispara workflow** (`knowledge-os`): o release não rodava depois do merge automático. → Chame o release pela própria CI (`workflow_call`) quando ele existir.
- **`ubuntu-latest` mudou de versão** (`mauricio-site`, PR #125): o Playwright 1.58 parou de instalar navegadores no Ubuntu 26.04. → Quando uma ferramenta depende da imagem, fixe a versão do runner e anote o motivo ao lado.
- **CI só no Linux** (`knowledge-os`): o código nunca rodou no Windows. → Aqui o Windows é obrigatório desde o primeiro PR.
- **Ambiente na nuvem sem rede para alguns hosts** (`mauricio-site`): o tradutor local não baixava os modelos de tradução. → Prefira ferramenta que roda offline. O núcleo usa só biblioteca padrão.
- **A integração não cria repositório na conta do Issei** (`knowledge-os`, 403). → Peça ao Issei para criar; não tente de novo.
- **Estoque de especificação** (retrospectiva do `knowledge-os`, 22/10/2026): cerca de 18 mil palavras de Fase 0, parte para itens que talvez não existam. → Detalhe uma etapa só quando ela entrar em execução.
- **Mesma pessoa escreve o teste de referência e avalia o sistema** (`knowledge-os`, golden set C0). → Quando houver conjunto de referência, peça revisão independente (outro papel ou outra pessoa).
