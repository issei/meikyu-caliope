---
name: redigir-documento
description: Padrão de redação dos documentos novos do meikyu-caliope — português do Brasil em linguagem simples (ABNT NBR ISO 24495-1), ASD-STE100 adaptado ao PT-BR e princípios Lean. Use ao escrever ou revisar especificação, ADR, relatório, README ou mensagem de PR.
---

# Redação de documentos

Regra do Issei (22/10/2026, aplicada no `knowledge-os`): documentos **novos** seguem este padrão. Não reescreva documento existente só para mudar o estilo.
Se a skill `ptbr-controlado` estiver disponível na conta, use-a como referência detalhada de estilo.

## Cabeçalho

```yaml
---
id: CAL-<TIPO>-<NN>
titulo: <frase curta>
data: AAAA-MM-DD
leitor: <quem lê e o que decide>
padrao_de_redacao: ABNT NBR ISO 24495-1 (linguagem simples) e ASD-STE100 adaptado ao PT-BR
---
```

## Linguagem simples (ISO 24495-1)

1. Comece pelo leitor: diga para quem é, o que ele precisa fazer e quanto tempo leva.
2. A informação mais importante vem primeiro. Decisões pedidas ficam numa seção própria e numerada.
3. Use títulos que dizem o conteúdo ("O que muda no CI"), não rótulos ("Contexto").
4. Defina a sigla no primeiro uso.

## ASD-STE100 adaptado

1. Uma ideia por frase. Frase de instrução com até 20 palavras; descrição com até 25.
2. Voz ativa, com sujeito explícito. "A CI roda os testes", não "os testes são rodados".
3. Um termo para um conceito. Use os termos da especificação (resposta, trecho, código, tema, achado, natureza).
4. Instrução no imperativo: "Rode", "Confira".
5. Sem advérbio vago ("basicamente", "praticamente") e sem adjetivo de marketing.

## Pensamento enxuto (Lean)

- Escreva o que alguém vai ler ou usar agora. Detalhe de etapa futura é estoque e envelhece.
- Prefira tabela a parágrafo quando o leitor compara itens.
- Cada afirmação sobre código foi conferida no código, com caminho e commit. Se não conferiu, marque **[Validar]**.

## Revisão

Peça ao agente `revisor-redacao` uma revisão do documento antes do PR.
