# Bíblia Cronológica: contexto para o Claude

Lê isto antes de mexer no projeto. Resume o que já foi decidido e porquê, para não refazer discussões.

## O projeto

App para ler a Bíblia inteira pela ordem dos acontecimentos, em 365 dias, com notas que explicam o que costuma deixar dúvidas e diagramas de cada época. É uma PWA de página única que funciona offline e se instala no telemóvel. O público é a família e a igreja do dono do projeto, e quem mais quiser.

- Dono: Cláudio Tomás (Pitt), Maputo. Fala com ele em **português**, de forma direta.
- Repositório público: https://github.com/claudi-tm/biblia-cronologica
- Site: https://claudi-tm.github.io/biblia-cronologica/ (GitHub Pages, publicado pela automação)

## Decisões tomadas (não reabrir sem o Pitt pedir)

**Língua.** A interface e as notas estão em português de Moçambique e de Portugal: "Génesis", "telemóvel", "Deuteronómio", "Crónicas". O texto bíblico mantém a grafia brasileira original.

**Texto bíblico: Bíblia Livre (BLIVRE), CC BY 4.0.** Não é domínio público: exige crédito, data da versão (fevereiro de 2018) e indicação das alterações. O crédito aparece no fim de cada leitura e em `dados/texto/LEIA-ME.md`. A Almeida 1911 (domínio público) foi rejeitada pela ortografia antiga. As revisões modernas da SBB (ARA, ARC, NAA) têm direitos de autor e não se podem usar.

**Plano de leitura.** 12 épocas e 365 dias, com 1189 capítulos e 31 102 versículos, cada um lido exatamente uma vez (verificado em `scripts/gerar_plano.py`). As passagens guardam o versículo inicial e final (`vi`, `vf`) quando cortam um capítulo. Os dias são equilibrados pelo tempo de leitura (média de 3,3 capítulos por dia). Ajustes em relação ao pedido original:
- Joel foi acrescentado à época 6 (faltava na lista).
- Isaías está dividido: capítulos 1–35 na época 6, capítulos 36–66 na época 7, junto de 2 Reis 18–20.
- Os Salmos com contexto histórico estão intercalados na narrativa (o 51 depois de 2 Samuel 12, o 90 depois de Números 14, o 137 no exílio, e outros). Os restantes estão em 6 blocos ao longo do reinado de Davi.
- A harmonia dos Evangelhos é por blocos de acontecimentos, ainda não versículo a versículo.
- As datas são aproximadas e seguem a cronologia tradicional (Êxodo em c. 1446 a.C.). O app diz que são aproximadas.

**A regra mais importante das notas: nada do futuro na resposta principal.** Foi o Pitt que a levantou ("porque é que já estamos a falar de Jesus aqui?"). Quem lê por ordem ainda não chegou aos livros seguintes. Por isso:
- A pergunta e a resposta falam só do que o leitor já leu, ou do que vem dentro da época atual.
- As ligações a livros de épocas seguintes vão para a secção `## Mais à frente na Bíblia`, que no app aparece fechada.
- Nas épocas do Novo Testamento, as notas devem apontar para trás (por exemplo, em Mateus 27:51: "Lembras-te do véu de Êxodo 26?").
- `scripts/validar.py` impõe esta regra: recusa referências a dias depois do fim da época e palavras como "Jesus" ou "Cristo" no Antigo Testamento.

**Outras regras das notas** (estão também em `CONTRIBUTING.md`):
- As citações entre aspas "..." têm de existir tal e qual na Bíblia Livre, e o validador confirma. Para hebraico, traduções literais ou expressões que não são citações, usa-se «...».
- As notas usam as palavras desta tradução. Exemplos: "Não cometerás homicídio" (e não "Não matarás"), "coberta" e "propiciatório", "átrio", "Festa das Cabanas".
- Nas questões morais difíceis (guerras, escravatura, castigos), a nota apresenta as leituras principais e diz com franqueza quando não há uma resposta que resolva tudo.
- O texto é escrito para o projeto. Nunca se copia de Bíblias de estudo.
- O côvado conta como 45 cm.

**Tipos de dúvida:** `costumes`, `medidas`, `objetos`, `rituais`, `lugares`, `pessoas`, `palavras`, `contradicoes`, `morais`. O tipo "morais" foi criado no piloto. "Ligações AT–NT" deixou de ser um tipo e passou a ser a secção "Mais à frente".

**Prioridade** (é só a ordem de escrita, e o Pitt pode mudá-la):
- A: muita gente tropeça aqui, ou é essencial para entender passagens mais à frente, ou pode afastar o leitor.
- B: dúvida comum.
- C: curiosidade.

**Licenças:** notas, diagramas e plano em CC BY-SA 4.0 (`LICENCA-CONTEUDO.md`); código em MIT; texto bíblico em CC BY 4.0.

## Estrutura

| Caminho | O que é |
|---|---|
| `notas/epoca-XX/LIVRO-CAP-VERS.md` | Uma nota por ficheiro. Cabeçalho entre `---`, resposta em parágrafos, e a secção opcional `## Mais à frente na Bíblia`. Uma segunda pergunta no mesmo versículo termina em `-2.md`. |
| `dados/plano.json` | Épocas e dias, gerado por `scripts/gerar_plano.py`. |
| `dados/texto/CODIGO.json` | Texto por livro (`caps[c-1][v-1]`), gerado por `scripts/converter_texto.py`. |
| `diagramas/diagramas.js` | Objeto `DG` com 14 diagramas da época 3 e partilhados; `DG_EPOCA` diz que diagramas aparecem em cada época; `NOMES_DG` tem os títulos. |
| `app/index.html` | O app. Os dados são injetados entre os marcadores `/*PLANO_INICIO*/`, `/*NOTAS_INICIO*/` e `/*DIAGRAMAS_INICIO*/`. Tem também o objeto antigo `VIS`, com 4 visuais das épocas 1, 2, 3 e 6. |
| `app/sw.js`, `app/manifest.webmanifest`, ícones | Instalação e funcionamento offline. |
| `scripts/biblia.py` | Funções partilhadas: livros, tipos, leitura e escrita das notas. |
| `scripts/validar.py` | Verifica as notas. A automação corre-o em cada push e em cada pull request. |
| `scripts/montar.py` | Gera `_site/`. Com `--pagina-unica X` gera uma só página para pré-visualizar. |
| `scripts/issue_para_nota.py` | Converte uma proposta feita pelo formulário numa nota. |
| `.github/ISSUE_TEMPLATE/` | Formulários "Revisão de notas" e "Propor uma nota nova". |
| `.github/workflows/` | `validar.yml`, `publicar.yml` (Pages) e `proposta-para-nota.yml` (etiqueta `aprovar` → pull request). |

## Comandos

```
python scripts/validar.py            # tem de terminar com 0 erros antes de qualquer commit
python scripts/montar.py             # gera _site/
cd _site && python -m http.server 8000
```

`gerar_plano.py` e `converter_texto.py` só são precisos para mudar a ordem das leituras ou a tradução. Precisam de `pip install -r requirements.txt`, e o conversor precisa das fontes originais: `damarals/biblias` (BLIVRE) e `BibleNLP/ebible` (`por-porbr2018`).

## Fluxo de contribuição

- **Revisão:** cada nota tem os botões Clara, Confusa e Errada, com um comentário opcional, guardados no telemóvel (`localStorage`, chave `bc.revisao`). O cartão "Revisão das notas" no ecrã Hoje abre o formulário do GitHub já preenchido, ou copia o texto. Cada nota aparece pelo código, que é o nome do ficheiro (ex.: `EXO-020-026`).
- **Nota nova:** formulário no GitHub. Quem coordena põe a etiqueta `aprovar`, a automação valida e abre um pull request, e depois de juntado o site atualiza sozinho.
- `estado: rascunho` mostra "rascunho, por rever" no app. Passa a `revista` depois de revista por alguém de confiança.

Outras chaves do `localStorage`: `bc.lidos` (dias lidos), `bc.fonte`, `bc.tema`, `bc.notas`.

## Estado atual (4 de novembro de 2026)

Feito:
- O plano completo e o texto completo.
- A época 3, Êxodo e deserto (dias 30–76): levantamento de 120 dúvidas e as 120 notas escritas, todas como `rascunho`, de autoria do Claude.
- Os 14 diagramas da época 3, mais o mapa das tribos em Canaã, para a época 4.
- Revisão no app, formulários e automações, PWA offline.

Por confirmar: se o Pitt já ativou nas definições do GitHub (a sessão do Claude não tem acesso a esta parte):
1. **Settings → Pages → Source = GitHub Actions**.
2. **Settings → Actions → General → Read and write permissions** e **Allow GitHub Actions to create and approve pull requests**.
3. Correr **Actions → Publicar o app → Run workflow** uma vez.

Na app do GitHub para telemóvel estas definições não aparecem: é preciso usar o browser, se necessário com "Site para computador".

## Próximos passos (por ordem sugerida)

1. Confirmar que o site está no ar e testar uma proposta de nota com a etiqueta `aprovar`.
2. **Levantamento e notas das outras épocas**, com o mesmo método do piloto: percorrer os dias da época, registar dúvidas por tipo e prioridade, ligar cada uma ao versículo, e escrever as notas com as regras acima. Validar sempre.
3. **Diagramas que faltam** (em `DG_EPOCA` e nos campos `visual` de `plano.json`):
   - árvore de Davi a Jesus e mapa do reino de Salomão (época 5);
   - continuação da tabela dos reis de Judá (época 7);
   - mapa da deportação para a Babilónia (época 8);
   - as três ondas de regresso (época 9);
   - mapa da Galileia e da Judeia (época 10);
   - viagens de Paulo (época 11);
   - linha das cartas e das igrejas da Ásia Menor (época 12).
   Convém também passar os 4 visuais do objeto `VIS` de `app/index.html` para `DG` em `diagramas/diagramas.js`.
4. Harmonia dos Evangelhos versículo a versículo, na época 10.
5. Os extras pedidos para depois: lembrete diário, leitura em grupo, perguntas de reflexão por dia, áudio, e contas para sincronizar o progresso.

## Cuidados

- Os diagramas usam só tokens de cor (`var(--...)`), para funcionarem nos temas claro e escuro. Antes de publicar, verifica o resultado num ecrã de telemóvel (cerca de 390 px), nos dois temas, para apanhar etiquetas sobrepostas.
- Em Êxodo 20:26, algumas edições numeram o versículo como 25. Nesta tradução é o 26.
- O texto tem 31 103 versículos porque Apocalipse 12:18 existe nesta tradução. O plano conta 31 102 pela versificação de referência, mas lê o capítulo inteiro, por isso nada fica de fora.
- As mensagens de commit terminam com as linhas de atribuição que a sessão indicar.
