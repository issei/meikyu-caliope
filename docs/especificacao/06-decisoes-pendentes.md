# Decisões pendentes — guia para o Issei

Data: 30/10/2026. Fonte: `01-especificacao.md` §19.3 e §19.4.

Já decididas por você: D-01 (a especificação fica na pasta do projeto por enquanto) e D-02 (o LLM não processa o conteúdo das respostas; só orquestra).

Para responder, basta uma mensagem curta, por exemplo: "D-03 ok, D-04 ok, D-07 nome X". O que você não responder fica com a recomendação, e eu registro assim na especificação.

## Ordem sugerida

| Grupo | Decisões | Bloqueia |
| :-- | :-- | :-- |
| **Agora** | D-06, D-07 | Criar o repositório e começar a etapa E0 |
| **Antes da primeira resposta real** | D-04, D-05, D-09, V-06 | Importar dados reais |
| **Pode esperar** | D-03, D-08 | Nada no MVP |

---

## D-06 — Aceitar as nove ADRs

**O que é.** As ADRs registram as decisões de arquitetura. Aceitar quer dizer: "a implementação segue isto até alguém revisar".

| ADR | Decisão em uma linha |
| :-- | :-- |
| ps-001 | SQLite, não base de grafos (Minigraf fica para depois da v3) |
| ps-002 | Arquivo original guardado sem alteração; o resto pode ser recalculado a partir dele |
| ps-003 | Histórico de mudanças só de inclusão; a única exceção é o expurgo |
| ps-004 | O MCP consulta e propõe; aceitar e rejeitar só no terminal, por você |
| ps-005 | Servidor MCP próprio e leve, como o do `knowledge-os` |
| ps-006 | Cada base é fictícia ou real desde a criação, sem mistura |
| ps-007 | O LLM não vê texto de resposta (sua decisão D-02) |
| ps-008 | Copiar três arquivos de infraestrutura do `knowledge-os`, com origem registrada |
| ps-009 | Núcleo genérico; cada pesquisa entra como um pacote de dados |

**Recomendação:** aceitar as nove. A que mais muda o dia a dia é a ps-004: toda aprovação passa pelo terminal, não pelo chat.

---

## D-07 — Nome do repositório e do pacote

**O que é.** O núcleo serve para outras pesquisas (ADR-ps-009). Um nome com "streaming" descreveria só a primeira.

**Opções:**

1. Nome genérico, por exemplo `bancada-pesquisa`, `acervo-pesquisa` ou `pesquisa-local`. O estudo fica em `estudos/streaming-2026/`.
2. Nome do estudo, `pesquisa-streaming`. Mais claro hoje; enganoso quando chegar a segunda pesquisa.

**Recomendação:** opção 1. O nome é seu; os três exemplos são só sugestões. Depois de escolher, você cria o repositório **privado** no GitHub (a integração não cria repositórios na sua conta) e eu abro o PR com a especificação.

---

## D-04 — Quem dá o código do participante

**O que é.** O arquivo da página não tem identificador de pessoa. O backend precisa de um código estável (pseudônimo) para ligar várias versões das respostas da mesma pessoa, sem usar o nome.

**Opções:**

1. O backend gera em sequência na importação: `P-001`, `P-002`… Quem importa informa o código quando o arquivo é de alguém que já existe.
2. A Liga tem uma regra própria de códigos (por exemplo, a mesma usada na reportagem). O backend aceita o código informado.

**Recomendação:** opção 1, a menos que a Liga já tenha uma regra. A pergunta para a Liga é só: "vocês já codificam participantes de algum jeito?".

---

## D-05 — Por quanto tempo guardar os dados reais e quando apagar

**O que é.** As respostas trazem nome, contato e informação sobre deficiência. A página promete que a pessoa pode retirar a autorização antes da publicação. O backend já tem o expurgo; falta a regra de quando usá-lo.

**O que precisa ser definido com a Liga:**

1. Até quando os dados identificáveis (nome, contato, arquivo original) ficam guardados. Ponto de partida para a conversa: apagar depois da publicação da reportagem, ou numa data fixa.
2. O que fica depois disso: códigos, trechos aceitos e achados, sem identificação.
3. Quem pode pedir o expurgo e em quanto tempo ele é feito.

**Recomendação:** definir antes da primeira importação real. Não proponho prazo: é decisão da pesquisa e, em parte, jurídica (V-06).

---

## V-06 — Enquadramento na LGPD

**O que é.** Informação sobre deficiência provavelmente é dado pessoal sensível (LGPD, art. 5º, II, "dado referente à saúde"). Isso muda a base legal e os cuidados exigidos.

**Recomendação:** pedir a quem responde juridicamente pela Liga uma confirmação curta, antes da primeira resposta real. Eu não sou fonte jurídica; a especificação só prevê os controles técnicos (separação da identificação, expurgo, barreira de conteúdo).

---

## D-09 — Gravar o id do questionário no arquivo exportado pela página

**O que é.** Hoje o JSON da página diz a versão do **formato** (`versao: 1`), mas não a versão das **perguntas**. Se o questionário mudar, o backend não saberá qual texto a pessoa leu.

**Mudança proposta no site:** a página grava `"instrumento": "entrevista-streaming@1"` no JSON. É uma linha no `modelo.js` e um teste. Arquivos antigos, sem esse campo, continuam aceitos como versão 1.

**Recomendação:** fazer num PR próprio do `mauricio-site` antes da primeira coleta real. Se a coleta real já começou, fazer mesmo assim; os arquivos já recebidos entram como versão 1.

---

## D-03 — Quantas pessoas revisam a codificação

**O que é.** Em pesquisa qualitativa, duas pessoas podem codificar os mesmos trechos e comparar o resultado (concordância entre codificadores). Isso aumenta a confiabilidade, mas dobra o trabalho e exige o backend com vários revisores.

**Opções:**

1. Uma pessoa revisa tudo no MVP. Concordância fica para depois do incremento 2.
2. Duas pessoas desde o início. O MVP passa a registrar quem revisou e a calcular a concordância.

**Recomendação:** opção 1, a menos que a metodologia da Liga exija concordância. Nesse caso, avise antes do incremento 2.

---

## D-08 — Merge automático de PR

**O que é.** No `knowledge-os`, todo PR com testes verdes entra sozinho na `main`. Aqui o código vai tratar dados sensíveis.

**Opções:**

1. Igual ao `knowledge-os`: merge automático para tudo.
2. Merge automático só para documentação; código espera a sua aprovação.
3. Tudo espera a sua aprovação.

**Recomendação:** opção 2. Documentação não toca dados; código pode mudar a barreira de conteúdo ou o expurgo, então merece um olhar humano.
