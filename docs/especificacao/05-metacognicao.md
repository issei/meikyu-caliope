# Metacognição: repositório, abstração e reaproveitamento

| Campo | Valor |
| :-- | :-- |
| Pedido | Issei, 30/10/2026: "faça uma bateria de meta-cognição sobre a proposta dessa solução considerando esses pontos e atualize a especificação" |
| Pontos | (1) repositório próprio; (2) abstração para outras pesquisas; (3) reaproveitamento do `knowledge-os` |
| Fonte conferida | `issei/knowledge-os`, `main` em `feefe4d` (30/10/2026): `src/kos/mcp/__init__.py`, `store/schema.py`, `store/dump.py`, `errors.py`, `audit/__init__.py`, `cite/__init__.py`, `search/__init__.py`, `.github/workflows/`, `docs/fase-1/retrospectiva-2026-10-22.md` |
| Resultado | Mudanças na especificação listadas na §9 |

Siglas e prefixos de identificadores seguem o cabeçalho de `01-especificacao.md`. `BL-` e `TC-` são itens de backlog e casos de teste do `knowledge-os`.

Método: para cada ponto, escrevo o pressuposto, o melhor argumento contrário, um pré-mortem ("daqui a seis meses deu errado; por quê?") e a confiança na recomendação. Antes disso, confiro as minhas próprias afirmações das respostas anteriores.

---

## 1. Conferência das minhas afirmações

| # | O que eu afirmei | O que o código mostra | Situação |
| :-- | :-- | :-- | :-- |
| C-1 | "A conferência de citação do `knowledge-os` relê o texto e compara byte a byte." | `cite.verify` compara `sha256(normalize(recorte))` com o hash guardado. A comparação byte a byte é uma ação **pendente** na retrospectiva (§7). | **Errado.** Corrigi a mensagem no thread. |
| C-2 | ADR-ps-005: "padrão do `knowledge-os`: toda ferramenta com `outputSchema`". | O servidor devolve `structuredContent`, mas não declara `outputSchema`. | **Errado.** `outputSchema` é um acréscimo deste projeto. ADR corrigida. |
| C-3 | "A busca FTS5 do `knowledge-os` devolve trechos." | `search._query` usa `snippet(fragment_fts, …)`. | Certo. |
| C-4 | "Mesmo padrão do servidor do `knowledge-os`, que já funciona." | Funciona no Linux. O CI do `knowledge-os` roda só em `ubuntu-latest`. | **Incompleto.** Código copiado de lá nunca rodou no Windows. Risco R-13. |
| C-5 | "Toda chamada `tools/call` é auditada, inclusive as rejeitadas." | Confirmado no cabeçalho do módulo e no BL-20 (TC-MCP-03). | Certo. |

Lição: duas de cinco afirmações sobre reaproveitamento estavam erradas ou incompletas. Eu escrevi de memória do que tinha lido parcialmente. Esta é a mesma falha registrada na retrospectiva do `knowledge-os` ("afirmei um fato sem verificar"). Regra para a implementação: cada arquivo copiado é lido inteiro antes da cópia.

---

## 2. Ponto 1 — Repositório próprio

**Pressuposto.** O backend é um produto separado do site e do `knowledge-os`.

**Melhor argumento contrário.** Colocar o backend dentro do repositório do site simplifica a extração do instrumento: o HTML da página e o extrator ficariam no mesmo commit, e uma mudança no formulário quebraria um teste na hora.

**Por que não convence.**

1. Mesclar no `main` do site dispara deploy de produção. O pipeline do site não deve carregar um pacote Python com regras de dados sensíveis.
2. O repositório do site é público. O backend deve ficar fora de qualquer lugar onde uma fixture real possa ser publicada por engano.
3. O ganho de detectar mudança no formulário se obtém de outro jeito: a validação já recusa chave desconhecida (`VAL-006`), e a página pode gravar o id do instrumento no JSON exportado (recomendação I-01, §8).

**Outra alternativa: dentro do `knowledge-os`.** Recusada. Os domínios são diferentes (conhecimento técnico de repositórios × dados de pesquisa com dados sensíveis), os ciclos de release também, e o `knowledge-os` faz merge automático de todo PR verde na `main`.

**Pré-mortem.** "O repositório separado ficou parado; ninguém percebeu que o formulário mudou e os arquivos novos falharam na importação." Mitigação: I-01 e a mensagem de `VAL-004`/`VAL-006`, que diz qual instrumento falta.

**Recomendação.** Repositório próprio e privado, criado pelo Issei no início da implementação (etapa E0). Nome genérico se o ponto 2 for aceito (D-07). Público só depois de decisão explícita.

**Confiança:** alta.

---

## 3. Ponto 2 — Abstração para outras pesquisas

**Pressuposto.** Outras pesquisas terão estrutura parecida: formulário, respostas por pergunta, codificação, temas e achados.

**O que eu não sei.** Só existe uma pesquisa. Não sei se a próxima será formulário, entrevista transcrita, grupo focal ou diário.

**Melhor argumento contrário.** "Generalizar agora é desperdício." Uma abstração feita com um só caso tende a acertar o que não varia e errar o que varia. Esse é o desperdício de superprodução que a retrospectiva do `knowledge-os` (Lean) já apontou.

**Onde o argumento contrário acerta e onde erra.**

| Item | Varia entre pesquisas? | Custo de deixar genérico agora | Decisão |
| :-- | :-- | :-- | :-- |
| Importação com hash, eventos, estados, exportação, barreira MCP | Não | Zero: já é genérico | Manter |
| Perguntas, partes, campos sensíveis | Sim | Zero: o instrumento já é dado | Manter como dado |
| Situação (grupo de campos que se repete) | Sim: outra pesquisa pode ter "episódio", "dispositivo" ou nenhum | Baixo: o instrumento declara **grupos repetíveis** e seus campos | **Mudar agora** |
| Eixos A–E | Sim | Baixo: o instrumento declara **dimensões** e seus valores | **Mudar agora** |
| Regra de autorização (`aut-uso` + valores) | Sim | Baixo: o instrumento declara qual pergunta e quais valores liberam citação | **Mudar agora** |
| Formato do arquivo da página (`campos`, `situacoes`) | Sim | Baixo: um **leitor** por formato converte para a representação interna | **Mudar agora** |
| Tabela de normalização dos campos livres | Sim | Zero: já é dado versionado | Manter |
| Análises AN-01 a AN-05 | Parcialmente | Baixo: descrever por "dimensão" e "grupo", não por "eixo" e "situação" | **Mudar agora** |
| Entrevista transcrita sem perguntas fixas | Sim | Alto: exige modelo de segmento sem pergunta | **Não fazer.** Fora do escopo até existir o caso |
| Vários estudos na mesma base, consulta entre estudos | — | Médio | **Não fazer.** Uma base por estudo e natureza |
| Barreira de conteúdo e natureza da base | Não devem variar | — | **Invariantes.** Não viram configuração |

**Pré-mortem.** "Criamos um 'framework de pesquisa'; a segunda pesquisa era uma transcrição de áudio e nada serviu." Mitigação: não há framework. Há costuras baratas (instrumento declarativo e leitor por formato). Uma pesquisa de outro tipo pede um leitor novo, não um núcleo novo.

**Pré-mortem inverso.** "Não generalizamos; a segunda pesquisa exigiu copiar o repositório e trocar `situacao` e `eixo` em 40 arquivos." Mitigação: as mudanças "agora" da tabela acima. Teste de fronteira (RNF-11): nenhum arquivo do núcleo menciona chave do formulário de streaming.

**Recomendação.** Costuras, não framework. O núcleo fala de *instrumento, pergunta, dimensão, grupo repetível, item de grupo, regra de autorização*. O estudo de streaming é um **pacote de estudo**: instrumento, normalização, leitor e conjunto de análises. Neste estudo, "grupo repetível" = situação e "dimensão" = eixo.

**Confiança:** média. O valor real só aparece com a segunda pesquisa. O custo de errar é baixo.

---

## 4. Ponto 3 — Reaproveitamento do `knowledge-os`

**Pressuposto.** O código do `knowledge-os` resolve problemas iguais aos deste backend.

**O que conferi.** Ver §1. Em resumo, três partes servem quase sem mudança; três servem como ideia; três não servem.

| Origem no `knowledge-os` | O que serve | Adaptação | Forma |
| :-- | :-- | :-- | :-- |
| `store/schema.py` | Criação atômica (arquivo temporário e troca de nome), `initialize` idempotente, WAL, versão de esquema em tabela de metadados, `require_fts5()` com erro próprio | Uma base em vez de duas | Copiar |
| `errors.py` | Catálogo fechado de códigos e teste que compara o catálogo com o contrato | Códigos deste projeto (`VAL-*`, `TRC-*`…) | Copiar a ideia e o teste |
| `mcp/__init__.py` | JSON-RPC por linha, negociação de versão, erros do protocolo, `structuredContent`, anotações | Acrescentar `resources`, `outputSchema`, barreira de conteúdo, ferramentas de escrita | Copiar e estender |
| `store/dump.py` | Dump lógico sem ids inteiros nem carimbos de tempo, com digest | Usar no teste de ida e volta da exportação | Ideia |
| `audit/__init__.py` | Ordem "grava o evento e confirma antes de executar": nunca resultado sem evento | Aplicar à tabela `ChamadaMcp` | Ideia |
| `docs/ci-cd.md` e workflows | Classificação "só documentação × sistema", release por versão sem tag | Acrescentar `windows-latest` como obrigatório; merge automático é decisão do Issei (D-08) | Ideia |
| `search` (`snippet`) | — | Devolve texto: viola a barreira | **Não usar** no MCP |
| `cite`, `answer` (`ask_extractive`) | — | Devolvem texto citado | **Não usar** no MCP |
| `parsing/*`, `discovery/*` | — | Feitos para Git, Markdown e HTML de código | **Não usar** |

**Melhor argumento contrário.** "Extraia uma biblioteca comum (`mcp-stdio-minimo`) e use nos dois projetos." Evita duas cópias divergentes.

**Por que não agora.** Dois consumidores ainda não justificam uma biblioteca com versão e release próprios. A regra prática é extrair na terceira ocorrência. Até lá, a cópia leva um cabeçalho de origem (repositório, commit, caminho) e a ADR-ps-008 lista os arquivos copiados.

**Pré-mortem.** "Um defeito foi corrigido no servidor MCP do `knowledge-os` e a cópia continuou com ele." Mitigação: a lista de arquivos copiados na ADR-ps-008; revisão dessa lista a cada release do `knowledge-os`.

**Pré-mortem 2.** "O código copiado quebrou no Windows (codificação do stdio, caminhos)." Mitigação: CI `windows-latest` obrigatório desde a etapa E1; teste de stdio com acentos (RNF-09).

**Confiança:** alta para `schema`, `errors` e `mcp`; média para o restante.

---

## 5. Interações entre os três pontos

1. **Abstração × nome do repositório.** Se o núcleo é genérico, o nome `pesquisa-streaming` descreve só o primeiro pacote de estudo. Proposta: nome genérico para o repositório e o pacote, e `estudos/streaming-2026/` para o pacote de estudo (D-07).
2. **Reaproveitamento × barreira.** O que o `knowledge-os` tem de mais valioso (busca com trecho e resposta extrativa) é justamente o que a barreira proíbe. O reaproveitamento útil é de infraestrutura, não de recuperação.
3. **Abstração × barreira.** A tentação é tornar a barreira configurável por estudo. Recusado: a decisão do Issei é um princípio, não uma opção. Configurável, ela seria desligada no primeiro estudo com prazo curto.
4. **Repositório × reaproveitamento.** Dois repositórios privados do mesmo dono: a cópia de código não tem obstáculo de licença.

---

## 6. Pré-mortem geral (seis meses à frente)

| # | Cenário de falha | Sinal precoce | Mitigação na especificação |
| :-- | :-- | :-- | :-- |
| F-1 | A revisão pela CLI é cansativa; a pessoa volta para planilha | Fila de propostas cresce sem revisão | `caliope revisar --fila` em uma tela por proposta; teste de uso com o Issei na etapa E2, com a base fictícia |
| F-2 | O LLM sem acesso ao texto agrega pouco valor | Nenhuma regra proposta é aceita | Medir no MVP: taxa de aceitação por regra (`regras_listar`) |
| F-3 | Regras por termo erram em português (flexão, acento) | Taxa de aceitação baixa | Busca sem acento e com prefixo (`legend*`); regra versionada |
| F-4 | O formulário muda e os arquivos novos falham | `VAL-006` em importação real | I-01; leitor por formato |
| F-5 | Ninguém roda o CI no Windows | Falha só na máquina do Issei | `windows-latest` obrigatório desde E1 |
| F-6 | A abstração atrasa o MVP | Etapa E1 passa do prazo | Só as costuras da §3; nada de "transcrição" nem "vários estudos" |

---

## 7. Confiança calibrada nas recomendações principais

| Recomendação | Confiança | O que me faria mudar de ideia |
| :-- | :-- | :-- |
| SQLite, não Minigraf | Alta | Minigraf v3 com #371 corrigido e necessidade real de consulta temporal |
| Barreira de conteúdo invariante | Alta (decisão do Issei) | Nova decisão do Issei |
| Decisões humanas só na CLI | Alta | Cliente MCP com confirmação do usuário confiável (*elicitation*) |
| Regras determinísticas como forma de assistência da IA | **Média** | F-2 ou F-3 confirmados no MVP |
| Costuras de abstração | Média | A segunda pesquisa não for formulário |
| Copiar `schema`, `errors`, `mcp` do `knowledge-os` | Alta | Defeito encontrado ao ler o código inteiro |
| Repositório próprio e privado | Alta | — |

---

## 8. Recomendação para fora deste backend

**I-01 (site).** A página `/entrevista-acessibilidade-streaming` pode gravar `"instrumento": "entrevista-streaming@1"` no JSON exportado. Com isso, o backend sabe qual instrumento usar sem adivinhar. É mudança no site e exige PR próprio no `mauricio-site`; não fiz.

---

## 9. Mudanças aplicadas na especificação

| Documento | Mudança |
| :-- | :-- |
| `01-especificacao.md` | Nova §5.4 (pacote de estudo e costuras; camadas passam a §5.5); RF-25; RNF-11 (teste de fronteira); leitor por formato na importação; estrutura de diretórios com `leitores/` e `estudos/`; reaproveitamento na stack e no roadmap; riscos R-13 e R-14; decisões D-01 (atualizada), D-07, D-08 e D-09; validação V-01 com `require_fts5` |
| `02-contratos-mcp.md` | Saídas falam em `dimensao` e `grupo` |
| `03-adrs.md` | ADR-ps-005 corrigida (C-2); ADR-ps-008 (reaproveitamento por cópia); ADR-ps-009 (costuras de abstração) |
| `README.md` | Índice com este documento |
