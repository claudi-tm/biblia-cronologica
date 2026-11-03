"""Converte a Bíblia Livre (BLIVRE, CC BY 4.0) num ficheiro JSON por livro.

Fontes:
  - damarals/biblias, data/canonical/BLIVRE (cópia do getBible, versificação protestante)
  - BibleNLP/ebible, corpus/por-porbr2018.txt (cópia oficial do eBible) para corrigir falhas

Saída: texto/<CÓDIGO>.json  ->  {"livro": "Génesis", "codigo": "GEN", "caps": [["v1", "v2", ...], ...]}
O versículo n do capítulo c está em caps[c-1][n-1].

Alterações ao texto original (exigido pela licença indicar):
  - espaços normalizados (início/fim, espaços duplos, espaço depois de pontuação colada)
  - Salmo 46:3 preenchido a partir da cópia do eBible (faltava na cópia do getBible)
  - Deuteronómio 32:5 sem a marcação de nota de rodapé
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gerar_plano import LIVRO  # noqa: E402

ORIGEM = os.environ.get("ORIGEM_BLIVRE", "fontes/biblias/data/canonical/BLIVRE")
EBIBLE = os.environ.get("ORIGEM_EBIBLE", "fontes/ebible")
SAIDA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dados", "texto")


def ebible_verso(ref):
    vref = open(f"{EBIBLE}/metadata/vref.txt").read().split("\n")
    texto = open(f"{EBIBLE}/corpus/por-porbr2018.txt", encoding="utf-8").read().split("\n")
    return texto[vref.index(ref)].strip()


def limpar(t):
    t = t.replace(" ", " ")
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"([,;:])(?=[A-Za-zÀ-ÿ])", r"\1 ", t)  # "Álefe:Bem" -> "Álefe: Bem"
    return t


def main():
    os.makedirs(SAIDA, exist_ok=True)
    total, por_codigo = 0, {v["codigo"]: v for v in LIVRO.values()}
    correcoes = {("PSA", 46, 3): ebible_verso("PSA 46:3"),
                 ("DEU", 32, 5): ebible_verso("DEU 32:5")}
    for codigo, info in por_codigo.items():
        d = json.load(open(f"{ORIGEM}/{codigo}.json", encoding="utf-8"))
        caps = []
        for cap in d["chapters"]:
            versos = {v["number"]: v["text"] for v in cap["verses"]}
            for (cod, c, n), txt in correcoes.items():
                if cod == codigo and c == cap["number"]:
                    versos[n] = txt
            nums = sorted(versos)
            assert nums == list(range(1, len(nums) + 1)), f"{codigo} {cap['number']}: numeração {nums}"
            caps.append([limpar(versos[n]) for n in nums])
            assert all(caps[-1]), f"{codigo} {cap['number']}: versículo vazio"
        assert "/fn" not in json.dumps(caps), f"{codigo}: marcação de nota"
        total += sum(len(c) for c in caps)
        with open(f"{SAIDA}/{codigo}.json", "w", encoding="utf-8") as f:
            json.dump({"livro": info["nome"], "codigo": codigo, "caps": caps}, f,
                      ensure_ascii=False, separators=(",", ":"))

    # Verificar o plano contra o texto: todas as passagens existem
    plano = json.load(open(os.path.join(os.path.dirname(SAIDA), "plano.json"), encoding="utf-8"))
    cache = {}
    for dia in plano["dias"]:
        for p in dia["passagens"]:
            caps = cache.setdefault(p["codigo"], json.load(open(f'{SAIDA}/{p["codigo"]}.json'))["caps"])
            assert p["cf"] <= len(caps), (dia["dia"], p)
            if "vf" in p:
                assert p["vf"] <= len(caps[p["cf"] - 1]), (dia["dia"], p)

    tamanho = sum(os.path.getsize(f"{SAIDA}/{f}") for f in os.listdir(SAIDA))
    print(f"OK: 66 livros, {total} versículos, {tamanho // 1024} KB. Todas as passagens do plano existem no texto.")


if __name__ == "__main__":
    main()
