"""Funções partilhadas: livros, plano, texto bíblico e ficheiros de notas."""
import json
import os
import re
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS = os.path.join(RAIZ, "dados")
NOTAS_DIR = os.path.join(RAIZ, "notas")

# código, nome (pt-MZ/PT), abreviatura, outros nomes aceites nas notas
LIVROS = [
    ("GEN", "Génesis", "Gn", ["Gênesis"]), ("EXO", "Êxodo", "Ex", []), ("LEV", "Levítico", "Lv", []),
    ("NUM", "Números", "Nm", []), ("DEU", "Deuteronómio", "Dt", ["Deuteronômio"]), ("JOS", "Josué", "Js", []),
    ("JDG", "Juízes", "Jz", []), ("RUT", "Rute", "Rt", []), ("1SA", "1 Samuel", "1Sm", []),
    ("2SA", "2 Samuel", "2Sm", []), ("1KI", "1 Reis", "1Rs", []), ("2KI", "2 Reis", "2Rs", []),
    ("1CH", "1 Crónicas", "1Cr", ["1 Crônicas"]), ("2CH", "2 Crónicas", "2Cr", ["2 Crônicas"]),
    ("EZR", "Esdras", "Ed", []), ("NEH", "Neemias", "Ne", []), ("EST", "Ester", "Et", []),
    ("JOB", "Jó", "Jó", []), ("PSA", "Salmos", "Sl", ["Salmo"]), ("PRO", "Provérbios", "Pv", []),
    ("ECC", "Eclesiastes", "Ec", []), ("SNG", "Cânticos", "Ct", []), ("ISA", "Isaías", "Is", []),
    ("JER", "Jeremias", "Jr", []), ("LAM", "Lamentações", "Lm", []), ("EZK", "Ezequiel", "Ez", []),
    ("DAN", "Daniel", "Dn", []), ("HOS", "Oseias", "Os", []), ("JOL", "Joel", "Jl", []),
    ("AMO", "Amós", "Am", []), ("OBA", "Obadias", "Ob", []), ("JON", "Jonas", "Jn", []),
    ("MIC", "Miqueias", "Mq", []), ("NAM", "Naum", "Na", []), ("HAB", "Habacuque", "Hc", []),
    ("ZEP", "Sofonias", "Sf", []), ("HAG", "Ageu", "Ag", []), ("ZEC", "Zacarias", "Zc", []),
    ("MAL", "Malaquias", "Ml", []), ("MAT", "Mateus", "Mt", []), ("MRK", "Marcos", "Mc", []),
    ("LUK", "Lucas", "Lc", []), ("JHN", "João", "Jo", []), ("ACT", "Atos", "At", []),
    ("ROM", "Romanos", "Rm", []), ("1CO", "1 Coríntios", "1Co", []), ("2CO", "2 Coríntios", "2Co", []),
    ("GAL", "Gálatas", "Gl", []), ("EPH", "Efésios", "Ef", []), ("PHP", "Filipenses", "Fp", []),
    ("COL", "Colossenses", "Cl", []), ("1TH", "1 Tessalonicenses", "1Ts", []),
    ("2TH", "2 Tessalonicenses", "2Ts", []), ("1TI", "1 Timóteo", "1Tm", []), ("2TI", "2 Timóteo", "2Tm", []),
    ("TIT", "Tito", "Tt", []), ("PHM", "Filémon", "Fm", ["Filemom"]), ("HEB", "Hebreus", "Hb", []),
    ("JAS", "Tiago", "Tg", []), ("1PE", "1 Pedro", "1Pe", []), ("2PE", "2 Pedro", "2Pe", []),
    ("1JN", "1 João", "1Jo", []), ("2JN", "2 João", "2Jo", []), ("3JN", "3 João", "3Jo", []),
    ("JUD", "Judas", "Jd", []), ("REV", "Apocalipse", "Ap", []),
]
NOME = {c: n for c, n, _, _ in LIVROS}
CODIGO_POR_NOME = {}
for c, n, ab, outros in LIVROS:
    for x in [n, ab, *outros]:
        CODIGO_POR_NOME[x] = c

TIPOS = {
    "costumes": "Costumes e cultura",
    "medidas": "Medidas, pesos e moedas",
    "objetos": "Objetos e construções",
    "rituais": "Rituais e leis",
    "lugares": "Lugares e geografia",
    "pessoas": "Pessoas e parentescos",
    "palavras": "Palavras difíceis",
    "contradicoes": "Aparentes contradições",
    "morais": "Questões morais difíceis",
}
ESTADOS = {"rascunho", "revista"}
PRIORIDADES = {"A", "B", "C"}


def ler_json(*caminho):
    with open(os.path.join(DADOS, *caminho), encoding="utf-8") as f:
        return json.load(f)


_texto = {}


def texto(codigo):
    if codigo not in _texto:
        _texto[codigo] = ler_json("texto", f"{codigo}.json")["caps"]
    return _texto[codigo]


def plano():
    return ler_json("plano.json")


def dia_do_versiculo(pl, codigo, cap, vers=None):
    """Dia do plano em que se lê esse capítulo (e versículo)."""
    for d in pl["dias"]:
        for p in d["passagens"]:
            if p["codigo"] != codigo or not (p["ci"] <= cap <= p["cf"]):
                continue
            if vers is not None:
                if cap == p["ci"] and vers < p.get("vi", 1):
                    continue
                if cap == p["cf"] and vers > p.get("vf", 10_000):
                    continue
            return d["dia"]
    return None


def sem_acentos(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def normalizar(s):
    return re.sub(r"\s+", " ", re.sub(r"[^\w ]", " ", sem_acentos(s))).strip()


# ---------- Ficheiros de notas ----------
# Formato:
# ---
# chave: valor        (uma linha por campo; listas como [a, b])
# ---
# parágrafos da resposta, separados por linha em branco
# ## Mais à frente na Bíblia
# parágrafos
CAMPOS = ["ref", "livro", "capitulo", "versiculo", "pergunta", "tipo", "prioridade", "diagrama", "estado", "autores"]
TITULO_ADIANTE = "## Mais à frente na Bíblia"


def nome_ficheiro(codigo, cap, vers, i=0):
    return f"{codigo}-{cap:03d}-{vers:03d}" + (f"-{i + 1}" if i else "") + ".md"


def escrever_nota(caminho, nota):
    linhas = ["---"]
    for k in CAMPOS:
        v = nota.get(k, "")
        if isinstance(v, list):
            v = "[" + ", ".join(v) + "]"
        linhas.append(f"{k}: {v}")
    linhas += ["---", ""]
    linhas += [p + "\n" for p in nota["resposta"]]
    if nota.get("adiante"):
        linhas += [TITULO_ADIANTE, ""] + [p + "\n" for p in nota["adiante"]]
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas).rstrip() + "\n")


def ler_nota(caminho):
    with open(caminho, encoding="utf-8") as f:
        s = f.read().replace("\r\n", "\n")
    m = re.match(r"---\n(.*?)\n---\n(.*)", s, re.S)
    if not m:
        raise ValueError("falta o cabeçalho entre linhas ---")
    meta = {}
    for linha in m.group(1).split("\n"):
        if not linha.strip():
            continue
        k, _, v = linha.partition(":")
        k, v = k.strip(), v.strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        meta[k] = v
    corpo = m.group(2)
    resposta, _, adiante = corpo.partition(TITULO_ADIANTE)
    par = lambda t: [re.sub(r"\s*\n\s*", " ", p).strip() for p in re.split(r"\n\s*\n", t) if p.strip()]
    meta["resposta"] = par(resposta)
    meta["adiante"] = par(adiante)
    for k in ("capitulo", "versiculo"):
        if k in meta:
            meta[k] = int(meta[k])
    meta["ficheiro"] = os.path.relpath(caminho, RAIZ)
    return meta


def todas_as_notas():
    out = []
    for raiz, _, fs in os.walk(NOTAS_DIR):
        for f in sorted(fs):
            if f.endswith(".md") and not f.startswith("_"):
                out.append(ler_nota(os.path.join(raiz, f)))
    return out
