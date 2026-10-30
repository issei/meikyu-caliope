# ADRs

Todas **aceitas** pelo Issei em 30/10/2026 (D-06). Prefixo `ps` (pesquisa-streaming), para não colidir com `kos` e `ap`.

## ADR-ps-001 — SQLite como armazenamento, não base de grafos

- **Contexto.** O domínio é um grafo pequeno, de profundidade fixa (achado → tema → código → trecho → resposta). O volume é de dezenas de entrevistas. O pedido sugere avaliar o Minigraf.
- **Decisão.** SQLite (biblioteca padrão do Python), modo WAL, chaves estrangeiras ligadas, uma base por arquivo.
- **Motivos.** Integridade declarativa; transações com vários comandos; leitura simultânea por outro processo; FTS5; zero dependência. O Minigraf 2.0.11 tem defeito de integridade em relações com vários valores (#371, reproduzido), bloqueia leitura por outro processo e não expõe transação com vários comandos em Python (`04-avaliacao-minigraf.md`).
- **Consequências.** Histórico vira responsabilidade do projeto (ADR-ps-003). Consultas de rastreio usam junções.
- **Reavaliar quando.** Minigraf v3.0.0 publicada, com #371 corrigido e transação em Python, e houver necessidade que SQLite resolve mal.

## ADR-ps-002 — Camadas de dados e bruto imutável

- **Decisão.** Quatro camadas: bruto (bytes do arquivo), normalizado (derivável), interpretação (persistida), derivado (execuções). O bruto é imutável, salvo expurgo.
- **Consequências.** A camada normalizada pode ser reconstruída do bruto e do instrumento. Um defeito de normalização se corrige sem perder dado.

## ADR-ps-003 — Registro de eventos só de inclusão, sem reconstrução por eventos

- **Decisão.** Tabela `Evento` com antes e depois; gatilhos impedem alteração e exclusão; estado atual nas tabelas.
- **Alternativa recusada.** Reconstrução completa por eventos: mais código, sem ganho para as perguntas do pedido.
- **Exceção.** Expurgo de participante (LGPD e retirada de autorização), registrado sem conteúdo.

## ADR-ps-004 — MCP consulta e propõe; a pessoa decide pela CLI

- **Contexto.** O servidor MCP não distingue uma decisão da pessoa de uma decisão do LLM: as duas chegam pela mesma chamada de ferramenta.
- **Decisão.** Nenhuma ferramenta MCP produz estado `aceito`, `rejeitado` ou `retirado`, nem restaura, expurga ou lê identificação. Essas ações ficam na CLI, com motivo obrigatório.
- **Consequências.** Fluxo humano tem um passo fora do chat. Em troca, toda interpretação aceita tem um ato humano registrado.
- **Revisitar.** Se os clientes usados suportarem confirmação explícita do usuário (*elicitation*) de modo confiável.

## ADR-ps-005 — Servidor MCP por stdio com biblioteca padrão

- **Decisão.** Reaproveitar o padrão do `knowledge-os` (item de backlog BL-20): JSON-RPC 2.0 por linha, stdio, só biblioteca padrão, negociação de versão, `structuredContent`, registro de toda chamada. **Acréscimos deste projeto** (não existem no `knowledge-os`): `outputSchema` em toda ferramenta, recursos e barreira de conteúdo. A linha de procedência do `knowledge-os` não é necessária: o texto de participante não sai pelo MCP (ADR-ps-007). [Corrigido em 30/10/2026: a versão anterior atribuía o `outputSchema` ao `knowledge-os`.]
- **Alternativa.** SDK oficial `mcp`: muitas dependências para poucas mensagens. Adotar se surgir necessidade de HTTP ou de recursos avançados.
- **Acréscimo em relação ao `knowledge-os`.** Recursos (`resources`), cada um com ferramenta de leitura equivalente.

## ADR-ps-006 — Natureza da base (fictícia ou real) fixa e explícita

- **Decisão.** A natureza é obrigatória na criação, não tem padrão e não muda. Toda saída a carrega; base fictícia leva aviso fixo. Operação recomendada: uma base fictícia e uma real, em pastas e servidores MCP com nomes diferentes.
- **Motivo.** Impedir, por construção, que dado de demonstração vire evidência.

## ADR-ps-007 — O LLM orquestra; não lê respostas

- **Contexto.** Decisão do Issei (30/10/2026): o uso de LLM não deve ser sobre as respostas; só na orquestração da análise e do estudo.
- **Decisão.** Barreira de conteúdo no servidor MCP (especificação §8.3): nenhuma saída contém texto de resposta, de situação, de trecho ou de identificação. O LLM vê estrutura, ids, metadados e agregados. A importação pelo MCP aceita só nome de arquivo. Codificação assistida acontece por **regras determinísticas** que o LLM propõe e o backend aplica; a pessoa revisa o texto na CLI.
- **Escopo.** Vale para as bases fictícia e real, para que o teste com dados fictícios prove a barreira.
- **Garantia.** Projeções sem colunas de texto; teste de vazamento (RF-24) com janelas de 20 caracteres.
- **Consequências.** Leitura, recorte e revisão de texto ficam no terminal ou no notebook. A IA perde a capacidade de sugerir códigos a partir do texto; em troca, nenhum conteúdo sai da máquina e o risco de instrução embutida em resposta desaparece.
- **Limite.** Outro servidor MCP com acesso a arquivos, no mesmo cliente, pode contornar a barreira. A pasta de dados deve ficar fora do alcance dele.

## ADR-ps-008 — Reaproveitar o `knowledge-os` por cópia registrada

- **Contexto.** O `knowledge-os` já resolve infraestrutura parecida (criação de base SQLite, catálogo de erros, servidor MCP por stdio). Conferência no código em `feefe4d` (`05-metacognicao.md` §1 e §4).
- **Decisão.** Copiar, com cabeçalho de origem (repositório, commit, caminho), `src/kos/store/schema.py`, `src/kos/errors.py` (e o teste que compara o catálogo com o contrato) e `src/kos/mcp/__init__.py`. Reaproveitar como ideia `store/dump.py` (digest lógico) e `audit` (evento gravado antes do resultado). Não usar `search`, `cite` nem `answer` no MCP: devolvem texto e violam a barreira (ADR-ps-007).
- **Alternativa recusada.** Biblioteca comum entre os dois projetos. Dois consumidores não justificam versão e release próprios. Reavaliar na terceira ocorrência.
- **Consequências.** Cada arquivo copiado é lido inteiro antes da cópia. A lista acima é revista a cada release do `knowledge-os`. O código copiado roda no CI `windows-latest` desde a etapa E1, porque o `knowledge-os` só testa no Linux.

## ADR-ps-009 — Costuras de abstração, não framework

- **Contexto.** Pergunta do Issei (30/10/2026): o sistema pode ser abstraído para outras pesquisas? Só existe uma pesquisa hoje.
- **Decisão.** O núcleo usa termos genéricos (instrumento, dimensão, grupo repetível, regra de autorização, campos sensíveis). Cada estudo é um pacote de dados com instrumento, normalização, leitor de formato e conjunto de análises (`01-especificacao.md` §5.4). Teste de fronteira impede o núcleo de mencionar o estudo de streaming.
- **Invariantes.** Barreira de conteúdo e natureza da base não são configuráveis.
- **Fora do escopo.** Transcrição livre sem perguntas fixas; vários estudos na mesma base.
- **Reavaliar quando.** Chegar a segunda pesquisa. Se ela não for formulário, o caminho é um leitor de formato novo; se nem isso bastar, revisar o modelo.
