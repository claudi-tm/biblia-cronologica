# Bíblia Cronológica

A Bíblia inteira pela ordem dos acontecimentos, em 365 dias, com notas que explicam o que costuma deixar dúvidas e diagramas de cada época. Em português, feita para o telemóvel.

**Abrir o app:** https://claudi-tm.github.io/biblia-cronologica/

No telemóvel, abre o link e escolhe **Adicionar ao ecrã principal** (ou **Instalar app**). Depois funciona sem internet.

---

## Como podes ajudar

### Rever notas (não precisa de saber programar)

1. Abre o app e lê normalmente.
2. Quando aparecer uma pergunta depois de um versículo, toca nela para abrir a nota.
3. No fim da nota, marca **Clara**, **Confusa** ou **Errada**. Se não estiver clara, escreve o que está mal.
4. No ecrã **Hoje**, no cartão **Revisão das notas**, toca em **Enviar para o GitHub**. Abre um formulário já preenchido; só tens de carregar em **Submit new issue**.

Para enviar pelo GitHub precisas de uma conta gratuita em https://github.com/signup. Se não quiseres criar conta, toca em **Copiar a revisão** e manda o texto por mensagem a quem coordena o projeto.

### Propor uma nota nova

Abre o formulário [Propor uma nota nova](https://github.com/claudi-tm/biblia-cronologica/issues/new?template=nova-nota.yml), escreve o versículo, a pergunta e a resposta, e envia. Antes, lê [Como escrever uma nota](CONTRIBUTING.md): são poucas regras.

---

## Para quem coordena

### Aprovar uma nota proposta

1. Abre a proposta em **Issues** e lê-a.
2. Se estiver bem, põe-lhe a etiqueta **aprovar**.
3. A automação verifica a nota. Se houver um problema, escreve um comentário na proposta a explicar o que corrigir.
4. Se estiver tudo certo, abre um **Pull request** com a nota. Lê-o e carrega em **Merge**.
5. Em poucos minutos o app é atualizado sozinho.

### Tratar uma revisão

As revisões chegam como issues com a etiqueta **revisão**. Cada nota tem um código (por exemplo `EXO-020-026`), que é o nome do ficheiro em `notas/`. Corrige o ficheiro, ou pede ajuda ao Claude colando a revisão na conversa.

Quando uma nota for revista por alguém de confiança, muda `estado: rascunho` para `estado: revista`. O app deixa de mostrar "rascunho, por rever".

---

## Como está organizado

| Pasta | O que tem |
|---|---|
| `notas/` | Uma nota por ficheiro, por época. É aqui que se escreve e corrige. |
| `dados/plano.json` | As 12 épocas e as leituras dos 365 dias. |
| `dados/texto/` | O texto da Bíblia Livre, um ficheiro por livro. |
| `diagramas/diagramas.js` | Os mapas, tabelas e desenhos. |
| `app/` | A página do app, o ícone e o funcionamento offline. |
| `scripts/` | Verificação das notas, montagem do site e geração dos dados. |

Para correr no computador (precisa de Python 3):

```
python scripts/validar.py   # verifica todas as notas
python scripts/montar.py    # monta o site em _site/
cd _site && python -m http.server 8000   # abre http://localhost:8000
```

O plano (`scripts/gerar_plano.py`) e o texto (`scripts/converter_texto.py`) já estão gerados; só é preciso voltar a corrê-los para mudar a ordem das leituras ou a tradução. Ver `requirements.txt`.

---

## Licenças

- **Texto bíblico:** Bíblia Livre (BLIVRE), de Diego Santos, Mario Sérgio e Marco Teles, versão de fevereiro de 2018, licença [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.pt_BR). Fonte: [eBible.org](https://ebible.org/porbr2018/copyright.htm). Alterações: espaçamento normalizado; Salmo 46:3 e Deuteronómio 32:5 corrigidos a partir da cópia do eBible. Ver [`dados/texto/LEIA-ME.md`](dados/texto/LEIA-ME.md).
- **Notas, diagramas e plano de leitura:** [CC BY-SA 4.0](LICENCA-CONTEUDO.md). Podes usar e adaptar, com crédito, partilhando com a mesma licença.
- **Código:** [MIT](LICENSE).
