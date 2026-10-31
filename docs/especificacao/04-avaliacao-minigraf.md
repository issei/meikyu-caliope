# Avaliação técnica do Minigraf

| Campo | Valor |
| :-- | :-- |
| Versão avaliada | `minigraf` 2.0.11 (crate Rust e pacote Python), publicada em 26/10/2026 |
| Fonte | Repositório `project-minigraf/minigraf`, commit `4a77092a` (29/10/2026); PyPI `minigraf` |
| Método | Leitura de `README.md`, `PHILOSOPHY.md`, `ROADMAP.md`, `CHANGELOG.md`, `Cargo.toml` e `docs/ERROR_REFERENCE.md`; instalação do pacote Python num ambiente isolado; dois scripts de sondagem (`anexos/minigraf-sondagem-1.py` e `-2.py`) |
| Data | 30/10/2026 |
| Conclusão | **Não usar como armazenamento do MVP.** Reavaliar depois da v3.0.0 (ver §5). |

## 1. O que o Minigraf é

O Minigraf é um banco de dados de grafos embutido, num arquivo único (`.graph`). Ele grava fatos no formato entidade–atributo–valor e responde a consultas em Datalog. Cada fato tem dois tempos: o tempo da transação (quando o fato foi gravado) e o tempo de validade (quando o fato era verdadeiro). O núcleo é escrito em Rust. A licença é MIT ou Apache-2.0.

## 2. Fatos verificados

Legenda: **[F]** = li na fonte; **[T]** = confirmei com teste; **[I]** = inferência minha.

| # | Fato | Evidência |
| :-- | :-- | :-- |
| M-01 | A versão atual é 2.0.11. A primeira versão do `CHANGELOG.md` é a 0.1.0, de 15/01/2026. O projeto tem cerca de nove meses. | [F] `Cargo.toml`, `CHANGELOG.md` |
| M-02 | O `Cargo.toml` declara um único autor. | [F] `Cargo.toml` (`authors`) |
| M-03 | Python é binding de nível 1 ("Tier 1"): testado e publicado junto com cada versão do núcleo. Windows em NTFS, disco local, também é nível 1. | [F] `PHILOSOPHY.md`, "Support tiers" |
| M-04 | O PyPI tem roda (`wheel`) para `win_amd64`, além de Linux e macOS. Requer Python ≥ 3.9. | [F] API JSON do PyPI |
| M-05 | A API Python expõe só `MiniGrafDb.open`, `open_in_memory`, `execute` e `checkpoint`. `execute` recebe texto Datalog e devolve texto JSON. | [T] `dir()` do módulo instalado |
| M-06 | A API Python **não** expõe transação explícita com vários comandos. O `begin_write` do README existe só na API Rust. Cada `execute` é uma transação. | [T] `(begin)` devolve `PRS-011 Unknown command`; [F] README |
| M-07 | **Defeito conhecido #371:** dois valores do mesmo atributo, na mesma entidade, gravados no mesmo `transact`, podem voltar como um só valor. A correção muda o formato do arquivo e sai só na v3.0.0. A versão 2.x não terá correção. | [F] README, `ROADMAP.md`, `PHILOSOPHY.md` |
| M-08 | Reproduzi o #371. Gravei `[:e :tag :x] [:e :tag :y] [:e :tag :z]` num `transact`. Na mesma sessão, a consulta devolveu só `:z`. Depois de fechar e abrir o arquivo, a consulta devolveu os três valores. A mesma consulta deu respostas diferentes antes e depois de reabrir. | [T] `anexos/minigraf-sondagem-2.py` |
| M-09 | Um só processo pode abrir o arquivo. Um segundo processo recebe `STG-026 Database is locked by another process`, **mesmo só para ler**. No mesmo processo, uma segunda abertura recebe `STG-025`. | [T] sondagem 2; [F] `ERROR_REFERENCE.md` |
| M-10 | Consulta "como era" funciona: `:as-of <n>` devolveu um valor depois de ele ser retirado (`retract`). | [T] sondagem 1 |
| M-11 | Um `transact` com fato malformado é recusado inteiro: nenhum fato do comando foi gravado. | [T] sondagem 1 (`PRS-046`) |
| M-12 | Há predicado de texto `contains?`. Não há busca textual com ranqueamento (equivalente ao FTS5). `str/includes?` não existe. | [T] sondagem 1 (`PRS-067`) |
| M-13 | Agregações comuns na v2: `count`, `count-distinct`, `sum`, `sum-distinct`, `min`, `max`. Média só como função de janela. | [F] README |
| M-14 | A v3.0.0 muda o formato do arquivo (v7 → v8). A migração roda sozinha ao abrir. O projeto pede cópia de segurança antes de abrir com uma versão maior nova. | [F] `ROADMAP.md`, `PHILOSOPHY.md` §7 |
| M-15 | O projeto lista como fora do escopo: autenticação, replicação, análise OLAP e aprendizado de máquina. | [F] `PHILOSOPHY.md`, "Non-Goals" |
| M-16 | Não consegui ler o número de estrelas, de contribuidores nem de issues: a API do GitHub não respondeu deste ambiente. | Limite desta avaliação |

## 3. Adequação ao problema

| Critério | Avaliação | Base |
| :-- | :-- | :-- |
| Modelo de domínio | Adequado em tese. Rastreio é um caminho curto e fixo (achado → tema → código → trecho → resposta). Não exige recursão. | [I] |
| Relações com vários valores | **Inadequado na v2.** Codificar é, por natureza, ligar um trecho a vários códigos e um código a vários trechos. O #371 atinge exatamente esse caso. A solução de contorno (um `transact` por valor) quebra a atomicidade da importação (M-06). | M-06, M-07, M-08 |
| Integridade | Não há esquema, chave estrangeira nem restrição de unicidade. Toda regra de integridade ficaria no código Python. | [I], M-05 |
| Histórico | Ponto forte: o histórico bitemporal vem pronto. Mas o problema precisa só do tempo da transação, que uma tabela de eventos resolve. | M-10, [I] |
| Concorrência | Fraca para o caso de uso. O servidor MCP mantém o arquivo aberto. Com ele aberto, nenhum notebook nem comando de linha consegue ler. | M-09 |
| Consultas e análises | Contagens servem. Busca textual não existe. Cruzamentos exigem consultas que o próprio projeto diz serem de outro domínio (OLAP). | M-12, M-13, M-15 |
| Windows e Python | Bom: nível 1 e roda pronta. | M-03, M-04 |
| Maturidade e manutenção | Risco alto para dado de pesquisa: projeto de nove meses, um autor declarado, defeito de integridade aberto e mudança de formato prevista. | M-01, M-02, M-07, M-14 |
| Cópia e restauração | Cópia do arquivo funciona. Não há exportação documentada para JSON; o produto teria de escrevê-la. | [I] |

## 4. Conclusão

Um banco relacional (SQLite) atende o mesmo modelo com menos risco. Ele tem esquema, chaves estrangeiras, transações com vários comandos, leitura simultânea de vários processos (modo WAL), busca textual (FTS5) e consultas recursivas, se forem necessárias. Ele vem na biblioteca padrão do Python.

O que o Minigraf oferece a mais é o histórico bitemporal e o Datalog. O histórico de que o projeto precisa é só o da transação. Uma tabela de eventos só de inclusão resolve isso (ver `01-especificacao.md` §13).

## 5. Quando reavaliar

Reavaliar o Minigraf se **todas** estas condições forem verdadeiras:

1. A v3.0.0 foi publicada e corrige o #371.
2. A API Python expõe transação com vários comandos.
3. Existe uma necessidade real que SQLite resolve mal, por exemplo: consultas de caminho de profundidade variável, ou consultas "como era a análise na data X" frequentes.

Mesmo assim, o uso recomendado seria como **projeção derivada**: um arquivo `.graph` gerado a partir da exportação JSON, para exploração, sem ser a fonte de verdade.
