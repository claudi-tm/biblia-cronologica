"""Gera e valida o plano de leitura cronológica da Bíblia (365 dias).

Saída: plano.json com as 12 épocas e os 365 dias.
Cada passagem: {"livro", "codigo", "ci", "cf"} para capítulos inteiros,
mais "vi" e "vf" quando começa ou acaba a meio de um capítulo.

Versificação: pythonbible (padrão protestante, igual à Almeida na quase
totalidade). Confirmar contra o texto escolhido na fase 3.
"""
import json
import os
import sys
from collections import Counter

import pythonbible as pb

# --- Livros: abreviatura, nome (pt-MZ/PT), código, enum pythonbible ---
LIVROS = [
    ("Gn", "Génesis", "GEN"), ("Ex", "Êxodo", "EXO"), ("Lv", "Levítico", "LEV"),
    ("Nm", "Números", "NUM"), ("Dt", "Deuteronómio", "DEU"), ("Js", "Josué", "JOS"),
    ("Jz", "Juízes", "JDG"), ("Rt", "Rute", "RUT"), ("1Sm", "1 Samuel", "1SA"),
    ("2Sm", "2 Samuel", "2SA"), ("1Rs", "1 Reis", "1KI"), ("2Rs", "2 Reis", "2KI"),
    ("1Cr", "1 Crónicas", "1CH"), ("2Cr", "2 Crónicas", "2CH"), ("Ed", "Esdras", "EZR"),
    ("Ne", "Neemias", "NEH"), ("Et", "Ester", "EST"), ("Jó", "Jó", "JOB"),
    ("Sl", "Salmos", "PSA"), ("Pv", "Provérbios", "PRO"), ("Ec", "Eclesiastes", "ECC"),
    ("Ct", "Cânticos", "SNG"), ("Is", "Isaías", "ISA"), ("Jr", "Jeremias", "JER"),
    ("Lm", "Lamentações", "LAM"), ("Ez", "Ezequiel", "EZK"), ("Dn", "Daniel", "DAN"),
    ("Os", "Oseias", "HOS"), ("Jl", "Joel", "JOL"), ("Am", "Amós", "AMO"),
    ("Ob", "Obadias", "OBA"), ("Jn", "Jonas", "JON"), ("Mq", "Miqueias", "MIC"),
    ("Na", "Naum", "NAM"), ("Hc", "Habacuque", "HAB"), ("Sf", "Sofonias", "ZEP"),
    ("Ag", "Ageu", "HAG"), ("Zc", "Zacarias", "ZEC"), ("Ml", "Malaquias", "MAL"),
    ("Mt", "Mateus", "MAT"), ("Mc", "Marcos", "MRK"), ("Lc", "Lucas", "LUK"),
    ("Jo", "João", "JHN"), ("At", "Atos", "ACT"), ("Rm", "Romanos", "ROM"),
    ("1Co", "1 Coríntios", "1CO"), ("2Co", "2 Coríntios", "2CO"), ("Gl", "Gálatas", "GAL"),
    ("Ef", "Efésios", "EPH"), ("Fp", "Filipenses", "PHP"), ("Cl", "Colossenses", "COL"),
    ("1Ts", "1 Tessalonicenses", "1TH"), ("2Ts", "2 Tessalonicenses", "2TH"),
    ("1Tm", "1 Timóteo", "1TI"), ("2Tm", "2 Timóteo", "2TI"), ("Tt", "Tito", "TIT"),
    ("Fm", "Filémon", "PHM"), ("Hb", "Hebreus", "HEB"), ("Tg", "Tiago", "JAS"),
    ("1Pe", "1 Pedro", "1PE"), ("2Pe", "2 Pedro", "2PE"), ("1Jo", "1 João", "1JN"),
    ("2Jo", "2 João", "2JN"), ("3Jo", "3 João", "3JN"), ("Jd", "Judas", "JUD"),
    ("Ap", "Apocalipse", "REV"),
]
ENUMS = list(pb.Book)[:66]
LIVRO = {ab: {"nome": n, "codigo": cod, "enum": ENUMS[i], "ordem": i}
         for i, (ab, n, cod) in enumerate(LIVROS)}


def ncap(ab):
    return pb.get_number_of_chapters(LIVRO[ab]["enum"])


def nvers(ab, c):
    return pb.get_number_of_verses(LIVRO[ab]["enum"], c)


# --- Notação da sequência ---
def C(ab, a=1, b=None):
    """Capítulos inteiros a..b (b=None: só o capítulo a)."""
    return ("C", ab, a, a if b is None else b)


def L(ab):
    """Livro inteiro."""
    return ("C", ab, 1, ncap(ab))


def V(ab, de, ate):
    """Intervalo com versículos: V('Mt', '3:1', '4:11')."""
    ci, vi = map(int, de.split(":"))
    cf, vf = map(int, ate.split(":"))
    return ("V", ab, ci, vi, cf, vf)


def S(*nums):
    return [C("Sl", n) for n in nums]


# --- Salmos colocados no seu contexto histórico ---
SL_EPOCA3 = [90]
SL_DAVI_CONTEXTO = [59, 34, 56, 52, 142, 54, 63, 57, 96, 105, 106, 60, 51, 32, 3, 18, 30, 72, 127, 132]
SL_EPOCA7 = [74, 79]
SL_EPOCA8 = [137]
SL_EPOCA9 = [126, 85]
colocados = set(SL_EPOCA3 + SL_DAVI_CONTEXTO + SL_EPOCA7 + SL_EPOCA8 + SL_EPOCA9)
restantes = [n for n in range(1, 151) if n not in colocados]
# Os restantes salmos são repartidos em 6 blocos ao longo do reinado de Davi
blocos = [restantes[i * len(restantes) // 6:(i + 1) * len(restantes) // 6] for i in range(6)]

SEQ = {
    1: [C("Gn", 1, 11)],
    2: [C("Gn", 12, 50), L("Jó")],
    3: [L("Ex"), L("Lv"), C("Nm", 1, 14), *S(90), C("Nm", 15, 36), L("Dt")],
    4: [L("Js"), L("Jz"), L("Rt")],
    5: [
        C("1Sm", 1, 19), *S(59), C("1Sm", 20, 21), *S(34, 56), C("1Sm", 22), *S(52, 142),
        C("1Sm", 23), *S(54, 63), C("1Sm", 24), *S(57), *S(*blocos[0]),
        C("1Sm", 25, 31), C("1Cr", 1, 10), C("2Sm", 1, 5), C("1Cr", 11, 12), *S(*blocos[1]),
        C("2Sm", 6), C("1Cr", 13, 16), *S(96, 105, 106), C("2Sm", 7), C("1Cr", 17),
        C("2Sm", 8), *S(60), C("1Cr", 18), C("2Sm", 9, 10), C("1Cr", 19), *S(*blocos[2]),
        C("2Sm", 11), C("1Cr", 20), C("2Sm", 12), *S(51, 32), C("2Sm", 13, 15), *S(3),
        *S(*blocos[3]), C("2Sm", 16, 22), *S(18), C("2Sm", 23, 24), C("1Cr", 21, 22), *S(30),
        *S(*blocos[4]), C("1Cr", 23, 29), *S(*blocos[5]),
        C("1Rs", 1, 4), C("2Cr", 1), *S(72), L("Pv"), C("1Rs", 5, 8), C("2Cr", 2, 7),
        *S(127, 132), C("Ct", 1, 8), C("1Rs", 9, 11), C("2Cr", 8, 9), L("Ec"),
    ],
    6: [
        C("1Rs", 12, 14), C("2Cr", 10, 12), C("1Rs", 15, 16), C("2Cr", 13, 16),
        C("1Rs", 17, 22), C("2Cr", 17, 20), C("2Rs", 1, 8), C("2Cr", 21, 22),
        C("2Rs", 9, 12), C("2Cr", 23, 24), L("Jl"), C("2Rs", 13, 14), C("2Cr", 25),
        L("Jn"), L("Am"), C("2Cr", 26), L("Os"), C("2Rs", 15, 16), C("2Cr", 27, 28),
        C("Is", 1, 12), L("Mq"), C("Is", 13, 35), C("2Rs", 17),
    ],
    7: [
        C("2Rs", 18, 19), C("Is", 36, 37), C("2Cr", 29, 32), C("2Rs", 20), C("Is", 38, 39),
        C("Is", 40, 66), C("2Rs", 21), C("2Cr", 33), L("Na"), C("2Rs", 22, 23),
        C("2Cr", 34, 35), L("Sf"), C("Jr", 1, 20), L("Hc"), C("2Rs", 24, 25), C("2Cr", 36),
        C("Jr", 21, 52), L("Lm"), *S(74, 79),
    ],
    8: [L("Ob"), *S(137), L("Ez"), L("Dn")],
    9: [
        C("Ed", 1, 4), L("Ag"), L("Zc"), C("Ed", 5, 6), *S(126, 85), L("Et"),
        C("Ed", 7, 10), L("Ne"), L("Ml"),
    ],
    # Harmonia dos Evangelhos por blocos: os mesmos acontecimentos ficam juntos
    10: [
        V("Jo", "1:1", "1:18"), C("Lc", 1), C("Mt", 1), C("Lc", 2), C("Mt", 2),
        V("Mc", "1:1", "1:13"), V("Mt", "3:1", "4:11"), V("Lc", "3:1", "4:13"),
        V("Jo", "1:19", "2:25"), C("Jo", 3, 4), V("Mt", "4:12", "4:25"),
        V("Mc", "1:14", "1:45"), V("Lc", "4:14", "5:39"), C("Mc", 2, 3), C("Jo", 5),
        C("Mt", 5, 7), C("Lc", 6), C("Mt", 8, 9), C("Lc", 7), C("Mt", 11, 12), C("Mt", 13),
        V("Mc", "4:1", "4:34"), C("Lc", 8), V("Mc", "4:35", "5:43"), C("Mt", 10), C("Mc", 6),
        V("Lc", "9:1", "9:17"), C("Mt", 14), C("Jo", 6), C("Mt", 15), V("Mc", "7:1", "8:26"),
        C("Mt", 16, 17), V("Mc", "8:27", "9:50"), V("Lc", "9:18", "9:50"), C("Mt", 18),
        V("Jo", "7:1", "10:21"), V("Lc", "9:51", "13:21"), V("Jo", "10:22", "10:42"),
        V("Lc", "13:22", "17:10"), C("Jo", 11), V("Lc", "17:11", "18:34"), C("Mt", 19, 20),
        C("Mc", 10), V("Lc", "18:35", "19:27"), C("Jo", 12), C("Mt", 21, 23), C("Mc", 11, 12),
        V("Lc", "19:28", "21:38"), C("Mt", 24, 25), C("Mc", 13), C("Jo", 13, 17),
        C("Mt", 26), C("Mc", 14), C("Lc", 22), C("Jo", 18, 19), C("Mt", 27), C("Mc", 15),
        C("Lc", 23), C("Mt", 28), C("Mc", 16), C("Lc", 24), C("Jo", 20, 21),
    ],
    11: [
        C("At", 1, 14), L("Tg"), L("Gl"), C("At", 15, 18), L("1Ts"), L("2Ts"),
        C("At", 19, 20), L("1Co"), L("2Co"), L("Rm"), C("At", 21, 28),
    ],
    12: [
        L("Ef"), L("Fp"), L("Cl"), L("Fm"), L("1Tm"), L("Tt"), L("1Pe"), L("2Tm"),
        L("2Pe"), L("Jd"), L("Hb"), L("1Jo"), L("2Jo"), L("3Jo"), L("Ap"),
    ],
}

EPOCAS = [
    (1, "Origens", "antes de 2000 a.C.", "AT", "genealogia-adao-abraao",
     "Da criação ao dilúvio e à torre de Babel. Mostra de onde vem o mundo, como entrou o pecado e a primeira promessa de Deus."),
    (2, "Patriarcas", "c. 2000–1800 a.C.", "AT", "arvore-12-tribos",
     "Deus chama Abraão e promete-lhe uma terra e uma descendência. A promessa passa a Isaque, Jacó e José, e a família acaba no Egito. Jó vive, provavelmente, nesta época."),
    (3, "Êxodo e deserto", "c. 1446–1406 a.C.", "AT", "rota-exodo",
     "Deus liberta Israel da escravidão no Egito, dá a Lei no monte Sinai e conduz o povo durante 40 anos pelo deserto, até à fronteira de Canaã."),
    (4, "Conquista e juízes", "c. 1406–1050 a.C.", "AT", "mapa-tribos-canaa",
     "Josué conduz a entrada em Canaã. Depois vêm ciclos de desobediência, opressão e libertação pelos juízes. Rute mostra fidelidade num tempo difícil."),
    (5, "Reino unido", "c. 1050–930 a.C.", "AT", "arvore-davi-jesus",
     "Saul, Davi e Salomão reinam sobre as 12 tribos. Davi recebe a promessa de um reino eterno e escreve muitos dos Salmos. Salomão constrói o templo."),
    (6, "Reino dividido", "930–722 a.C.", "AT", "tabela-reis",
     "O reino parte-se em Israel, a norte, e Judá, a sul. Os profetas avisam reis e povo, até que a Assíria destrói Israel e a sua capital, Samaria, em 722 a.C."),
    (7, "Judá sozinho", "722–586 a.C.", "AT", "tabela-reis-juda",
     "Judá resiste mais um século, com as reformas de Ezequias e Josias, até a Babilónia destruir Jerusalém e o templo em 586 a.C."),
    (8, "Exílio", "586–538 a.C.", "AT", "mapa-babilonia",
     "O povo vive deportado na Babilónia. Ezequiel e Daniel mostram que Deus continua presente, mesmo longe da terra e sem templo."),
    (9, "Retorno", "538–430 a.C.", "AT", "linha-regressos",
     "A Pérsia autoriza o regresso. Os judeus reconstroem o templo e as muralhas de Jerusalém. Malaquias fecha o Antigo Testamento."),
    (10, "Vida de Jesus", "c. 4 a.C.–30 d.C.", "NT", "mapa-galileia-judeia",
     "Nascimento, ministério, morte e ressurreição de Jesus. Os quatro Evangelhos são lidos em harmonia, com os mesmos acontecimentos juntos."),
    (11, "Igreja primitiva", "30–60 d.C.", "NT", "viagens-paulo",
     "A igreja nasce em Jerusalém e espalha-se pelo império. As primeiras cartas de Paulo e Tiago entram no momento em que foram escritas."),
    (12, "Últimas cartas", "60–95 d.C.", "NT", "linha-cartas",
     "Cartas escritas na prisão e no fim da vida dos apóstolos, até ao Apocalipse de João."),
]

MEDIA_VERS = 31102 / 1189  # versículos por capítulo, na Bíblia toda


# --- Unidades: um capítulo inteiro ou parte de um capítulo ---
def unidades(item):
    if item[0] == "C":
        _, ab, a, b = item
        return [(ab, c, 1, nvers(ab, c)) for c in range(a, b + 1)]
    _, ab, ci, vi, cf, vf = item
    out = []
    for c in range(ci, cf + 1):
        v0 = vi if c == ci else 1
        v1 = vf if c == cf else nvers(ab, c)
        out.append((ab, c, v0, v1))
    return out


def peso(u):
    """Metade pelo nº de capítulos, metade pelo tamanho em versículos."""
    ab, c, v0, v1 = u
    n = v1 - v0 + 1
    return 0.5 * (n / nvers(ab, c)) + 0.5 * (n / MEDIA_VERS)


def juntar(us):
    """Converte unidades consecutivas em passagens compactas."""
    ps = []
    for ab, c, v0, v1 in us:
        inteiro_ini = v0 == 1
        inteiro_fim = v1 == nvers(ab, c)
        last = ps[-1] if ps else None
        if (last and last["_ab"] == ab and last["cf"] == c - 1 and last["_fim_inteiro"]
                and inteiro_ini):
            last["cf"] = c
            last["vf"] = v1
            last["_fim_inteiro"] = inteiro_fim
        else:
            ps.append({"_ab": ab, "ci": c, "vi": v0, "cf": c, "vf": v1,
                       "_fim_inteiro": inteiro_fim})
    out = []
    for p in ps:
        ab = p["_ab"]
        d = {"livro": LIVRO[ab]["nome"], "codigo": LIVRO[ab]["codigo"], "ci": p["ci"], "cf": p["cf"]}
        if p["vi"] != 1 or p["vf"] != nvers(ab, p["cf"]):
            d["vi"], d["vf"] = p["vi"], p["vf"]
        out.append(d)
    return out


def ref(p):
    nome = p["livro"]
    if "vi" in p:
        if p["ci"] == p["cf"]:
            return f'{nome} {p["ci"]}:{p["vi"]}–{p["vf"]}'
        return f'{nome} {p["ci"]}:{p["vi"]}–{p["cf"]}:{p["vf"]}'
    if ncap_por_nome[nome] == 1:
        return nome
    return f'{nome} {p["ci"]}' + ("" if p["ci"] == p["cf"] else f'–{p["cf"]}')


ncap_por_nome = {v["nome"]: ncap(k) for k, v in LIVRO.items()}


def titulo(ps):
    """'Salmos 57; Salmos 1–2' passa a 'Salmos 57, 1–2'."""
    partes = []
    for i, p in enumerate(ps):
        r = ref(p)
        if i and ps[i - 1]["livro"] == p["livro"] and r.startswith(p["livro"] + " "):
            partes[-1] += ", " + r[len(p["livro"]) + 1:]
        else:
            partes.append(r)
    return "; ".join(partes)


def main():
    # 1. Unidades por época
    U = {e: [u for item in SEQ[e] for u in unidades(item)] for e in SEQ}
    W = {e: sum(peso(u) for u in U[e]) for e in U}
    total = sum(W.values())

    # 2. Dias por época, proporcionais ao peso (maiores restos)
    exato = {e: W[e] * 365 / total for e in W}
    dias_ep = {e: int(exato[e]) for e in exato}
    falta = 365 - sum(dias_ep.values())
    for e in sorted(exato, key=lambda e: exato[e] - int(exato[e]), reverse=True)[:falta]:
        dias_ep[e] += 1

    # 3. Cortes dentro de cada época, no limite de unidade mais próximo do alvo
    dias = []
    for e in sorted(U):
        us, d = U[e], dias_ep[e]
        acum, s = [0.0], 0.0
        for u in us:
            s += peso(u)
            acum.append(s)
        cortes = [0]
        for j in range(1, d):
            alvo = W[e] * j / d
            k = min(range(cortes[-1] + 1, len(us) - (d - j) + 1), key=lambda k: abs(acum[k] - alvo))
            cortes.append(k)
        cortes.append(len(us))
        for j in range(d):
            parte = us[cortes[j]:cortes[j + 1]]
            ps = juntar(parte)
            dias.append({"dia": len(dias) + 1, "epoca": e, "passagens": ps,
                         "titulo": titulo(ps),
                         "_peso": round(sum(peso(u) for u in parte), 2),
                         "_caps": round(sum((u[3] - u[2] + 1) / nvers(u[0], u[1]) for u in parte), 2)})

    # 4. Validação: cada versículo exatamente uma vez
    vistos = Counter()
    for e in U:
        for ab, c, v0, v1 in U[e]:
            for v in range(v0, v1 + 1):
                vistos[(ab, c, v)] += 1
    esperado = {(ab, c, v) for ab in LIVRO for c in range(1, ncap(ab) + 1) for v in range(1, nvers(ab, c) + 1)}
    faltam = esperado - set(vistos)
    repetidos = [k for k, n in vistos.items() if n > 1]
    extra = set(vistos) - esperado
    erros = []
    if faltam:
        erros.append(f"{len(faltam)} versículos em falta, ex.: {sorted(faltam)[:5]}")
    if repetidos:
        erros.append(f"{len(repetidos)} versículos repetidos, ex.: {sorted(repetidos)[:5]}")
    if extra:
        erros.append(f"{len(extra)} versículos inexistentes, ex.: {sorted(extra)[:5]}")
    if len(dias) != 365:
        erros.append(f"{len(dias)} dias em vez de 365")
    if any(not d["passagens"] for d in dias):
        erros.append("há dias vazios")
    if erros:
        print("ERROS:\n- " + "\n- ".join(erros))
        sys.exit(1)

    # 5. Escrever
    epocas = []
    for (i, nome, datas, t, vis, resumo) in EPOCAS:
        ds = [d for d in dias if d["epoca"] == i]
        epocas.append({"id": i, "nome": nome, "datas": datas, "testamento": t, "cor": t,
                       "visual": vis, "resumo": resumo,
                       "dia_inicio": ds[0]["dia"], "dia_fim": ds[-1]["dia"], "n_dias": len(ds)})
    caps = [d["_caps"] for d in dias]
    out = {
        "versao": 1,
        "versificacao": "protestante padrão (pythonbible); confirmar com o texto da Almeida na fase 3",
        "total": {"dias": 365, "capitulos": 1189, "versiculos": len(esperado)},
        "epocas": epocas,
        "dias": [{**{k: v for k, v in d.items() if not k.startswith("_")}, "capitulos": d["_caps"]} for d in dias],
    }
    destino = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dados", "plano.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"OK: {len(esperado)} versículos, cada um exatamente uma vez; 365 dias.")
    print("Capítulos por dia: min %.1f, max %.1f, média %.2f" % (min(caps), max(caps), sum(caps) / 365))
    for ep in epocas:
        print(f'  Época {ep["id"]:>2} {ep["nome"]:<20} dias {ep["dia_inicio"]:>3}–{ep["dia_fim"]:<3} ({ep["n_dias"]})')
    for n in (1, 60, 141, 290, 300, 365):
        d = dias[n - 1]
        print(f'  Dia {n}: {d["titulo"]}  [{d["_caps"]} cap.]')


if __name__ == "__main__":
    main()
