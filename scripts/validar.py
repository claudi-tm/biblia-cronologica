"""Valida todas as notas (ou só as indicadas).

Uso:
  python scripts/validar.py                 # todas as notas
  python scripts/validar.py notas/x.md ...  # só estas

Erros (impedem a entrada da nota):
  - campos em falta ou com valores inválidos
  - versículo que não existe no texto
  - citação entre aspas "..." que não aparece tal e qual na Bíblia Livre
  - resposta principal que fala de livros ou capítulos que o leitor ainda não leu
    (essas ligações vão para a secção "## Mais à frente na Bíblia")
  - diagrama que não existe
Avisos (não impedem): pergunta sem ponto de interrogação, nome de ficheiro fora do padrão.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import biblia as B  # noqa: E402

GITHUB = os.environ.get("GITHUB_ACTIONS") == "true"
NOMES_LIVROS = sorted({n for n in B.CODIGO_POR_NOME if len(n) > 3 or n in ("Jó",)}, key=len, reverse=True)
RE_REF = re.compile(r"(?<![\w])(" + "|".join(re.escape(n) for n in NOMES_LIVROS) + r")\s+(\d+)(?::(\d+))?")
PALAVRAS_NT = ["Jesus", "Cristo", "Novo Testamento", "Evangelho", "apóstolo", "Paulo"]


def diagramas_existentes():
    with open(os.path.join(B.RAIZ, "diagramas", "diagramas.js"), encoding="utf-8") as f:
        return set(re.findall(r'DG\["([^"]+)"\]\s*=', f.read()))


def epocas_por_dia(pl):
    return {d: e for e in pl["epocas"] for d in range(e["dia_inicio"], e["dia_fim"] + 1)}


def versiculos_normalizados():
    out = []
    for c, *_ in B.LIVROS:
        for cap in B.texto(c):
            out += [B.normalizar(v) for v in cap]
    return out


def validar(notas):
    pl = B.plano()
    ep_dia = epocas_por_dia(pl)
    dgs = diagramas_existentes()
    corpus = None
    erros, avisos = [], []
    vistos = {}

    for n in notas:
        f = n["ficheiro"]
        E = lambda m: erros.append((f, m))
        W = lambda m: avisos.append((f, m))

        for k in ("ref", "livro", "capitulo", "versiculo", "pergunta", "tipo", "prioridade", "estado"):
            if not n.get(k):
                E(f"falta o campo '{k}'")
        if erros and erros[-1][0] == f and "falta o campo" in erros[-1][1]:
            continue
        if n["livro"] not in B.NOME:
            E(f"livro '{n['livro']}' desconhecido (usa o código de 3 letras, ex.: EXO)")
            continue
        caps = B.texto(n["livro"])
        c, v = n["capitulo"], n["versiculo"]
        if not (1 <= c <= len(caps)) or not (1 <= v <= len(caps[c - 1])):
            E(f"{B.NOME[n['livro']]} {c}:{v} não existe no texto")
            continue
        esperado = f"{B.NOME[n['livro']]} {c}:{v}"
        if n["ref"] != esperado:
            E(f"ref '{n['ref']}' não corresponde a livro/capítulo/versículo (esperado '{esperado}')")
        if n["tipo"] not in B.TIPOS:
            E(f"tipo '{n['tipo']}' inválido. Opções: {', '.join(B.TIPOS)}")
        if n["prioridade"] not in B.PRIORIDADES:
            E("prioridade tem de ser A, B ou C")
        if n["estado"] not in B.ESTADOS:
            E(f"estado tem de ser um de: {', '.join(sorted(B.ESTADOS))}")
        if n.get("diagrama") and n["diagrama"] not in dgs:
            E(f"diagrama '{n['diagrama']}' não existe em diagramas/diagramas.js")
        if not n["resposta"]:
            E("a resposta está vazia")
        if not n["pergunta"].rstrip().endswith("?"):
            W("a pergunta não termina com '?'")
        base = os.path.basename(f)
        if not re.match(rf"{n['livro']}-{c:03d}-{v:03d}(-\d+)?\.md$", base):
            W(f"o nome do ficheiro devia começar por {n['livro']}-{c:03d}-{v:03d}")
        chave = (n["livro"], c, v, B.normalizar(n["pergunta"]))
        if chave in vistos:
            E(f"pergunta repetida (já existe em {vistos[chave]})")
        vistos[chave] = f

        # Citações exatas
        for q in re.findall(r'"([^"]+)"', " ".join(n["resposta"] + n["adiante"])):
            if len(q.split()) < 2:
                continue
            corpus = corpus or versiculos_normalizados()
            if not any(B.normalizar(q) in x for x in corpus):
                E(f'citação não encontrada na Bíblia Livre: "{q}". Copia o texto exato, ou usa «...» se não for citação')

        # Nada do futuro na resposta principal
        dia = B.dia_do_versiculo(pl, n["livro"], c, v)
        ep = ep_dia[dia]
        principal = " ".join([n["pergunta"]] + n["resposta"])
        for m in RE_REF.finditer(principal):
            cod = B.CODIGO_POR_NOME[m.group(1)]
            d2 = B.dia_do_versiculo(pl, cod, int(m.group(2)), int(m.group(3)) if m.group(3) else None) \
                or B.dia_do_versiculo(pl, cod, int(m.group(2)))
            if d2 and d2 > ep["dia_fim"]:
                E(f"'{m.group(0)}' só é lido no dia {d2}, depois do fim desta época (dia {ep['dia_fim']}). "
                  f"Passa esta ligação para a secção '{B.TITULO_ADIANTE[3:]}'")
        if ep["id"] < 10:
            for w in PALAVRAS_NT:
                if re.search(rf"(?<!\w){w}(?!\w)", principal):
                    E(f"a resposta principal fala de '{w}', mas o leitor ainda está no Antigo Testamento. "
                      f"Passa isso para a secção '{B.TITULO_ADIANTE[3:]}'")
    return erros, avisos


def main(args):
    if args:
        notas = [B.ler_nota(os.path.abspath(a)) for a in args]
    else:
        notas = B.todas_as_notas()
    erros, avisos = validar(notas)
    for f, m in avisos:
        print(f"::warning file={f}::{m}" if GITHUB else f"AVISO  {f}: {m}")
    for f, m in erros:
        print(f"::error file={f}::{m}" if GITHUB else f"ERRO   {f}: {m}")
    print(f"\n{len(notas)} notas verificadas: {len(erros)} erros, {len(avisos)} avisos.")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
