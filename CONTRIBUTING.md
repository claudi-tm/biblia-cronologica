# Como escrever uma nota

Uma nota responde a uma dúvida que aparece ao ler um versículo. Aparece no app logo depois desse versículo, como uma pergunta que se abre.

## As regras

**1. A pergunta é sobre o que o leitor tem à frente.**
Escreve-a como um leitor a faria: "Porque é que Moisés teve de tirar o calçado?". Não menciones livros que o leitor ainda não leu.

**2. A resposta fica no tempo da época.**
O app segue a ordem dos acontecimentos. Quem está no Êxodo ainda não leu os Evangelhos. Explica a passagem como a entenderia alguém daquela época. Podes citar livros já lidos, ou que ainda vêm na mesma época.

**3. As ligações ao futuro vão para "Mais à frente na Bíblia".**
Se a passagem se liga a Jesus, aos apóstolos ou a livros de épocas seguintes, escreve isso nessa secção. No app, aparece fechada, para quem quiser abrir.

**4. As citações são exatas.**
O que estiver entre aspas "assim" tem de estar tal e qual na Bíblia Livre, que é o texto do app. Para palavras em hebraico, traduções literais ou expressões que não são citações, usa «assim».

**5. Curta e clara.**
Dois ou três parágrafos curtos. Frases simples, como quem explica a um amigo. Português de Moçambique e de Portugal ("Génesis", "telemóvel").

**6. Honesta nas questões difíceis.**
Quando os estudiosos não concordam, diz isso e apresenta as leituras principais. Nas questões morais (guerras, escravatura, castigos), não escondas a dificuldade nem feches a questão com uma resposta só.

**7. Texto nosso.**
Não copies notas de Bíblias de estudo ou de sites: têm direitos de autor. Podes aprender com elas, mas escreve com as tuas palavras.

## O formato do ficheiro

Cada nota é um ficheiro em `notas/epoca-XX/`, com o nome `LIVRO-CAP-VERS.md` (por exemplo `EXO-020-026.md`). Se houver duas perguntas no mesmo versículo, a segunda termina em `-2.md`.

```
---
ref: Êxodo 20:26
livro: EXO
capitulo: 20
versiculo: 26
pergunta: Como é que nos degraus do altar se via a nudez?
tipo: costumes
prioridade: A
diagrama: 
estado: rascunho
autores: [Claude]
---

Primeiro parágrafo da resposta.

Segundo parágrafo.

## Mais à frente na Bíblia

Ligação a um livro que o leitor ainda não leu.
```

- **tipo:** `costumes`, `medidas`, `objetos`, `rituais`, `lugares`, `pessoas`, `palavras`, `contradicoes` ou `morais`.
- **prioridade:** `A` (muita gente tropeça aqui ou afeta a leitura mais à frente), `B` ou `C` (curiosidade).
- **diagrama:** o nome de um diagrama de `diagramas/diagramas.js`, ou vazio.
- **estado:** `rascunho` até alguém de confiança rever; depois `revista`.

## A verificação automática

Cada proposta é verificada antes de entrar. O verificador confirma que o versículo existe, que as citações estão na Bíblia Livre, que a resposta principal não fala do futuro, e que o tipo e o diagrama são válidos. Se algo falhar, diz exatamente o quê e como corrigir.
