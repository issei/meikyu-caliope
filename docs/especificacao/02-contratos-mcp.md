# Contratos MCP e de erro

Complementa `01-especificacao.md` §8–§10. Os nomes de campo ficam em português, sem acento, em `snake_case`, para coincidir com o esquema da base.

Os contratos usam os termos genéricos do núcleo (`01-especificacao.md` §5.4). No estudo de streaming, `dimensao` é o eixo do roteiro (valores `A` a `E`), `grupo` é a situação e `item_grupo` é uma situação preenchida.

## 1. Regras gerais

1. Todo `inputSchema` tem `additionalProperties: false`. Argumento desconhecido → erro `-32602` do protocolo.
2. Toda ferramenta declara `outputSchema`. O resultado tem `content` (texto legível) e `structuredContent` (JSON que valida no esquema).
3. Anotações: leitura → `readOnlyHint: true`; escrita → `readOnlyHint: false`, `destructiveHint: false`, `idempotentHint: true` quando a regra da §4 vale. Todas: `openWorldHint: false`.
4. Paginação: `limite` (1–100, padrão 50) e `cursor` (texto opaco). A resposta traz `proximo_cursor` ou `null`.
5. Texto livre de entrada: no máximo 4.000 caracteres por campo, salvo indicação.
6. Identificadores têm prefixo: `P-` participante, `S-` submissão, `R-` resposta, `SIT-` situação, `TRC-` trecho, `COD-` código, `CDF-` codificação, `TEM-` tema, `ACH-` achado, `EXE-` execução, `EV-` evento.
7. **Barreira de conteúdo** (especificação §8.3; decisão do Issei, 30/10/2026). Nenhuma saída MCP contém texto de resposta, de campo de situação, de trecho ou de identificação, nem parte dele. Respostas aparecem só como metadados (`preenchida`, `tamanho`, `sha256`). Erros e avisos citam chave e posição, nunca o valor.
8. Textos livres gravados pela CLI (nota, justificativa, enunciado) não saem pelo MCP, salvo se a pessoa os marcar com `--visivel-mcp`.

## 2. Envelope de resultado

Sucesso (`isError: false`):

```json
{
  "ok": true,
  "natureza": "ficticio",
  "aviso_natureza": "DADOS FICTÍCIOS — resultado demonstrativo, não é evidência de pesquisa.",
  "dados": { },
  "avisos": [ { "codigo": "AVI-001", "mensagem": "…", "onde": "aut-uso" } ],
  "evento_ate": "EV-000123"
}
```

- `aviso_natureza` aparece só em base fictícia.
- `evento_ate` é o último evento visível na leitura: permite repetir a consulta sobre o mesmo estado.

Erro de domínio (`isError: true`; o protocolo não falha):

```json
{
  "ok": false,
  "natureza": "ficticio",
  "erros": [
    { "codigo": "VAL-006", "mensagem": "A chave 'rotina-9' não existe no instrumento entrevista-streaming@1.",
      "onde": "campos.rotina-9", "acao": "Confira se o arquivo veio da página atual ou peça um instrumento novo." }
  ]
}
```

O texto em `content` repete a mensagem e a ação, em frases curtas.

## 3. Catálogo de erros

| Código | Quando | Ação sugerida |
| :-- | :-- | :-- |
| `CFG-001` | Base sem natureza, ou natureza inválida | Criar a base com `--natureza ficticio` ou `real` |
| `CFG-002` | Base não encontrada ou esquema mais novo que o pacote | Conferir o caminho; atualizar o pacote |
| `ARQ-001` | Nome de arquivo com separador, `..`, unidade ou caminho absoluto | Usar só o nome de um arquivo em `entrada/` |
| `ARQ-002` | Arquivo não existe em `entrada/` | Copiar o arquivo para `entrada/` |
| `VAL-001` … `VAL-010` | Regras da especificação §12.1 | Ver a mensagem |
| `PAR-001` | Participante informado não existe | Listar com `participantes_listar` |
| `PAR-002` | Participante retirado ou expurgado | Não importar; falar com quem coordena |
| `TRC-001` | Resposta não existe ou está vazia | — |
| `TRC-002` | `texto_citado` diferente do recorte `inicio`–`fim` | Recalcular as posições |
| `TRC-003` | Posições fora do texto, ou `inicio ≥ fim` | — |
| `TRC-004` | Resposta de pergunta `sensivel` | Trechos não podem vir de identificação |
| `COD-001` | Rótulo de código já existe com outra definição | Usar o código existente ou propor outro rótulo |
| `CDF-001` | Trecho ou código inexistente, rejeitado ou retirado | — |
| `ACH-001` | Hipótese sem base agregada | Informar ao menos um `execucao_id` ou `tema_id` |
| `ACH-002` | Aceitação (CLI) sem trecho aceito ligado | Ligar um trecho com `caliope achado evidencia` |
| `REG-001` | Regra sem termos, com termo de menos de 3 caracteres ou com mais de 50 termos | Ajustar a regra |
| `ANL-001` | Análise desconhecida ou parâmetro inválido | Listar com `analises_listar` |
| `EXP-001` | Restauração: formato ou versão desconhecida | — |
| `EXP-002` | Restauração: hash não confere | O arquivo foi alterado; usar outra cópia |
| `EXP-003` | Restauração: referência quebrada | — |
| `LIM-001` | Limite de tamanho ou de quantidade excedido | Reduzir a entrada |
| `INT-001` | Erro interno; nada foi gravado | Ver `logs/`; relatar |

## 4. Idempotência

Nenhuma ferramenta exige chave de idempotência. Cada escrita tem uma **chave natural**; repetir a chamada devolve o objeto existente com `duplicado: true`:

| Ferramenta | Chave natural |
| :-- | :-- |
| `json_importar` | SHA-256 dos bytes do arquivo |
| `caliope trecho criar` (CLI) | (`resposta_id`, `inicio`, `fim`) |
| `codigo_propor` | `rotulo` normalizado (minúsculas, NFC, espaços simples) + `definicao` |
| `regra_propor` | (`codigo_id`, critério canônico) |
| `regra_aplicar` | (`regra_id`, `regra_versao`, impressão das respostas) — cada codificação: (`trecho_id`, `codigo_id`, `codigo_versao`, `regra_id`) |
| `tema_propor` | `rotulo` normalizado |
| `tema_vincular_codigo` | (`tema_id`, `codigo_id`) |
| `achado_propor` | `enunciado` normalizado + conjunto de bases (`execucao_ids`, `tema_ids`) |
| `analise_executar` | (`analise`, `analise_versao`, `parametros` canônicos, impressão das entradas) |
| `exportar` | último `evento_id` + opções |

## 5. Contratos das ferramentas

Notação: `!` = obrigatório.

### 5.1 `estudo_resumo` (leitura)

Entrada: nenhuma.
Saída `dados`: `estudo {id, nome, natureza}`, `instrumento_vigente`, `contagens {participantes, submissoes_vigentes, respostas_preenchidas, itens_grupo, trechos, codigos, achados}`, `pacote_versao`, `esquema_versao`.

### 5.2 `instrumento_obter` (leitura)

Entrada: `instrumento_id` (texto; padrão: o vigente).
Saída: `id`, `fonte_commit`, `fonte_sha256`, `partes [{id, titulo, dimensao}]`, `dimensoes [{id, valores [{id, rotulo}]}]`, `perguntas [{chave, parte, dimensao, tipo, rotulo, opcoes, sensivel, ordem}]`, `grupos [{id, rotulo, parte, campos [{chave, rotulo}]}]`, `regra_autorizacao {pergunta, valores_que_permitem_citar}`.

### 5.3 `participantes_listar` (leitura)

Entrada: `limite`, `cursor`.
Saída: `itens [{id, submissao_vigente, versoes, autorizacao_uso, citavel, retirado}]`.

### 5.4 `json_validar` (leitura)

Entrada: `arquivo!` (nome em `entrada/`). Não há argumento de conteúdo: o arquivo não passa pelo cliente.
Saída: `valido` (lógico), `sha256`, `formato_versao`, `contagens {campos, preenchidos, itens_grupo}`, `erros []`, `avisos []`, `ja_importado` (id da submissão ou `null`).
Regras: não grava nada. Devolve **todos** os erros, não só o primeiro.

### 5.5 `json_importar` (escrita idempotente)

Entrada: `arquivo!` (nome em `entrada/`); `participante` (`P-nnn`, opcional).
Saída: `duplicado`, `arquivo_id`, `submissao_id`, `participante_id`, `versao`, `diferencas {incluidas [], alteradas [], removidas []}`, `trechos_reancorados []`, `objetos_desatualizados []`, `avisos []`.
Erros: `ARQ-*`, `VAL-*`, `PAR-*`, `LIM-001`.
Regras: valida antes; uma transação; evento `importacao`; com erro, nada é gravado.

### 5.6 `respostas_consultar` (leitura)

Entrada: `participante`, `submissao`, `pergunta` (chave), `parte`, `dimensao` (valor), `incluir_grupos` (lógico, padrão verdadeiro), `so_vigentes` (padrão verdadeiro), `limite`, `cursor`.
Saída: `itens [{resposta_id, participante_id, submissao_id, pergunta, rotulo_pergunta, dimensao, item_grupo_id, campo_grupo, preenchida, tamanho, sha256}]`. **Sem texto de resposta.**
Regras: pelo menos um filtro; ordem por (`participante_id`, ordem da pergunta, `item_grupo_id`).

### 5.6a `respostas_buscar` (leitura)

Entrada: `termos!` (1 a 20 termos, cada um com 3 a 50 caracteres), `modo` (`qualquer` | `todos`), `pergunta`, `dimensao`, `so_vigentes`.
Saída: `total`, `por_pergunta [{pergunta, n}]`, `por_dimensao [{dimensao, n}]`, `participantes` (quantidade), `resposta_ids []` (ordenados). **Sem texto, sem destaque, sem palavra vizinha.**
Regras: busca FTS5 sobre o texto normalizado [Validar V-01].

### 5.7 Criação de trecho (só CLI)

Não há ferramenta MCP: escolher um recorte exige ler o texto. Comando `caliope trecho criar <resposta_id> --inicio N --fim M --texto "…"`.
Regras: posições em caracteres (pontos de código Unicode) do texto normalizado; `origem = humano_cli`; `estado = aceito`. Erros: `TRC-001` a `TRC-004`. Trechos também nascem de `regra_aplicar` (§5.14), como `proposto`.

### 5.8 `trechos_consultar` (leitura)

Entrada: `participante`, `pergunta`, `dimensao`, `codigo`, `estado`, `citavel`, `limite`, `cursor`.
Saída: `itens [{trecho_id, resposta_id, pergunta, dimensao, tamanho, origem, estado, citavel, codigos [ids]}]`. **Sem `texto_citado`.**

### 5.9 `analises_listar` (leitura)

Saída: `analises [{id, versao, descricao, parametros_schema}]`, `execucoes_recentes [{id, analise, executado_em, desatualizada}]`.

### 5.10 `analise_executar` (escrita idempotente)

Entrada: `analise!` (`AN-01` …), `parametros` (objeto validado pelo `parametros_schema` da análise).
Saída: `execucao_id`, `duplicado`, `analise`, `analise_versao`, `parametros`, `impressao_entrada`, `n_participantes`, `resultado`, `resultado_sha256`, `executado_em`.
Regras: se já existe execução com a mesma chave natural e entrada atual igual, devolve a existente.

### 5.11 `exportar` (escrita em `saida/`)

Entrada: nenhuma (o MCP não exporta identificação).
Saída: `nome_arquivo`, `sha256`, `bytes`, `evento_ate`, `inclui_identificacao: false`.

### 5.12 `restauracao_verificar` (leitura)

Entrada: `arquivo!` (nome em `saida/` ou `entrada/`).
Saída: `valido`, `formato_versao`, `natureza`, `contagens`, `erros [EXP-*]`.

### 5.13 `eventos_listar` (leitura)

Entrada: `desde` (`EV-nnn`), `objeto` (id), `acao`, `limite`, `cursor`.
Saída: `itens [{id, momento, ator, acao, objeto_tipo, objeto_id}]`. Antes, depois e justificativa só pela CLI (podem conter texto de resposta ou dado pessoal).

### 5.14 Incremento 2

- `codigo_propor`: `rotulo!` (≤ 80), `definicao!`, `criterio_inclusao`, `criterio_exclusao`, `pai_id`, `criado_por`. Saída: código `proposto`. Erro `COD-001`.
- `codigos_listar`: `estado`, `pai_id`. Saída: árvore de códigos com versão, estado e número de codificações aceitas.
- `regra_propor`: `codigo_id!`, `termos!` (1 a 50, cada um com 3 a 50 caracteres), `modo` (`qualquer` | `todos`), `perguntas []`, `dimensoes []`, `criado_por`. Saída: regra com `id` e `versao`. Erros `REG-001`, `CDF-001`.
- `regra_aplicar`: `regra_id!`. Divide cada resposta alvo em frases (regra determinística e versionada), cria um trecho `proposto` por frase que casa e uma codificação `proposta` com `origem = regra`. Saída: `trechos_criados`, `codificacoes_criadas`, `por_pergunta`, `por_dimensao`, `ids []`. **Sem texto.**
- `regras_listar`: saída por regra: `versao`, `propostas`, `aceitas`, `rejeitadas`, `pendentes` (o LLM ajusta a regra pela taxa de aceitação).

### 5.15 Incremento 3

- `tema_propor`: `rotulo!`, `descricao!`, `codigo_ids []`.
- `tema_vincular_codigo`: `tema_id!`, `codigo_id!`.
- `temas_listar`: `estado`.
- `achado_propor`: `tipo!` (`achado` | `hipotese`), `enunciado!`, `bases!` (≥ 1: `execucao_ids`, `tema_ids`), `alcance` (texto, ex.: "4 de 12"). Erro `ACH-001`. A pessoa liga trechos e aceita na CLI (`ACH-002`).
- `achados_consultar`: `tipo`, `estado`, `tema_id`.
- `rastrear`: `objeto_id!`, `direcao!` (`origem` | `dependentes`). Saída: lista de caminhos `[[{tipo, id, estado}], …]`, ordenada.
- `impacto`: `objeto_id!`. Saída: `afetados [{tipo, id, estado_atual, motivo}]`, `execucoes_desatualizadas []`.

## 6. Comandos só da CLI

| Comando | Efeito |
| :-- | :-- |
| `caliope iniciar --base <nome> --natureza ficticio\|real` | Cria a base e as pastas |
| `caliope servir --base <nome>` | Inicia o servidor MCP (stdio) |
| `caliope importar <arquivo> [--participante P-nnn]` | Mesmo efeito de `json_importar` |
| `caliope respostas <filtros>` | Lê o texto das respostas (só no terminal) |
| `caliope trecho criar <R-…> --inicio N --fim M --texto "…"` | Cria trecho aceito |
| `caliope codificar <TRC-…> <COD-…> --motivo "…"` | Codificação humana aceita |
| `caliope revisar --fila [--regra REG-…]` | Mostra propostas com o texto, uma por vez, para aceitar ou rejeitar |
| `caliope achado evidencia <ACH-…> <TRC-…>` | Liga evidência a achado |
| `caliope revisar <id> --aceitar\|--rejeitar\|--retirar --motivo "…" [--visivel-mcp]` | Transição de estado humana |
| `caliope participante mover <S-…> --para <P-…> --motivo "…"` | Corrige associação |
| `caliope expurgar <P-…>` | Expurgo (pede confirmação digitada) |
| `caliope exportar [--com-identificacao]` | Exportação |
| `caliope restaurar <arquivo> --base <nova>` | Restauração em base nova |
| `caliope diagnostico` | Versão, caminhos, natureza, contagens, `integrity_check`, aviso de pasta sincronizada |

## 7. Exemplo de configuração de cliente (Windows)

Exemplo genérico; o arquivo e o formato dependem do cliente [Validar V-02].

```json
{
  "mcpServers": {
    "pesquisa-demo": {
      "command": "C:\\caminho\\pesquisa-streaming\\.venv\\Scripts\\caliope.exe",
      "args": ["servir", "--base", "demo"]
    }
  }
}
```
