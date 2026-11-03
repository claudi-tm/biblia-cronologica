# Texto bíblico

**Bíblia Livre (BLIVRE)**, de Diego Santos, Mario Sérgio e Marco Teles, versão de fevereiro de 2018.
Licença: Creative Commons Atribuição 4.0 Brasil (CC BY 4.0) — https://creativecommons.org/licenses/by/4.0/deed.pt_BR
Fonte e direitos: https://ebible.org/porbr2018/copyright.htm

Os autores e licenciantes originais não aprovam necessariamente estas alterações.

## Alterações feitas a partir do texto original

- Espaçamento normalizado (espaços no início e no fim, espaços duplos, espaço depois de pontuação colada).
- Salmo 46:3 preenchido a partir da cópia do eBible (faltava na cópia usada como base).
- Deuteronómio 32:5: retirada a marcação de nota de rodapé que estava colada ao texto.

## Formato

Um ficheiro por livro, com o código de 3 letras: `{"livro": "Génesis", "codigo": "GEN", "caps": [["v1", "v2", ...], ...]}`.
O versículo n do capítulo c está em `caps[c-1][n-1]`. Versificação protestante habitual; Apocalipse 12 tem 18 versículos nesta tradução.
Gerado por `scripts/converter_texto.py`.
