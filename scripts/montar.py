"""Monta o site em _site/: a página do app com o plano, as notas e os diagramas,
os ficheiros do texto bíblico e o necessário para instalar e ler offline.

Uso:
  python scripts/montar.py                  # gera _site/
  python scripts/montar.py --pagina-unica X # gera só a página (para pré-visualizar), em X
"""
import hashlib
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import biblia as B  # noqa: E402

SITE = os.path.join(B.RAIZ, "_site")
REPO = os.environ.get("GITHUB_REPOSITORY", "claudi-tm/biblia-cronologica")

CABECALHO = """<!doctype html>
<html lang="pt">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>
:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0;font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
img{max-width:100%}
[hidden]{display:none!important}
</style>
"""
PWA_HEAD = """<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#F3F4EF" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#121519" media="(prefers-color-scheme: dark)">
<link rel="icon" href="icone-192.png">
<link rel="apple-touch-icon" href="icone-192.png">"""
PWA_REGISTO = """<script>
if ("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost")) {
  window.addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));
}
</script>"""


def notas_para_app(pl):
    out = []
    for n in sorted(B.todas_as_notas(), key=lambda n: n["ficheiro"]):
        out.append({
            "id": os.path.splitext(os.path.basename(n["ficheiro"]))[0],
            "ref": n["ref"], "codigo": n["livro"], "cap": n["capitulo"], "vers": n["versiculo"],
            "dia": B.dia_do_versiculo(pl, n["livro"], n["capitulo"], n["versiculo"]),
            "tipo": n["tipo"], "tipo_nome": B.TIPOS[n["tipo"]], "pergunta": n["pergunta"],
            "prioridade": n["prioridade"], "diagrama": n.get("diagrama") or "",
            "estado": n["estado"], "resposta": n["resposta"], "adiante": n["adiante"],
            "ficheiro": n["ficheiro"],
        })
    return out


def injetar(s, nome, conteudo):
    s, n = re.subn(rf"/\*{nome}_INICIO\*/.*?/\*{nome}_FIM\*/",
                   lambda m: f"/*{nome}_INICIO*/{conteudo}/*{nome}_FIM*/", s, flags=re.S)
    assert n == 1, f"marcadores {nome} não encontrados em app/index.html"
    return s


def pagina(pwa):
    pl = B.plano()
    s = open(os.path.join(B.RAIZ, "app", "index.html"), encoding="utf-8").read()
    s = injetar(s, "PLANO", json.dumps(pl, ensure_ascii=False, separators=(",", ":")))
    s = injetar(s, "NOTAS", json.dumps(notas_para_app(pl), ensure_ascii=False, separators=(",", ":")))
    s = injetar(s, "DIAGRAMAS", "\n" + open(os.path.join(B.RAIZ, "diagramas", "diagramas.js"), encoding="utf-8").read() + "\n")
    s = s.replace('const REPO = "claudi-tm/biblia-cronologica";', f'const REPO = "{REPO}";')
    if pwa:
        s = CABECALHO + s.replace("<!--PWA_HEAD-->", PWA_HEAD).replace("<!--PWA_REGISTO-->", PWA_REGISTO)
    return s


def site():
    if os.path.exists(SITE):
        shutil.rmtree(SITE)
    os.makedirs(os.path.join(SITE, "texto"))
    html = pagina(pwa=True)
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(html)
    textos = sorted(os.listdir(os.path.join(B.DADOS, "texto")))
    for f in textos:
        shutil.copy(os.path.join(B.DADOS, "texto", f), os.path.join(SITE, "texto", f))
    for f in os.listdir(os.path.join(B.RAIZ, "app")):
        if f != "index.html":
            shutil.copy(os.path.join(B.RAIZ, "app", f), os.path.join(SITE, f))
    # versão do cache = impressão digital do conteúdo, para o telemóvel buscar as atualizações
    h = hashlib.sha256(html.encode()).hexdigest()[:10]
    sw = open(os.path.join(SITE, "sw.js"), encoding="utf-8").read()
    sw = sw.replace("__VERSAO__", h).replace("__TEXTOS__", json.dumps([f"texto/{f}" for f in textos]))
    open(os.path.join(SITE, "sw.js"), "w", encoding="utf-8").write(sw)
    open(os.path.join(SITE, ".nojekyll"), "w").close()
    total = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(SITE) for f in fs)
    print(f"Site montado em _site/ ({total // 1024} KB, versão {h})")


if __name__ == "__main__":
    if "--pagina-unica" in sys.argv:
        destino = sys.argv[sys.argv.index("--pagina-unica") + 1]
        open(destino, "w", encoding="utf-8").write(pagina(pwa=False))
        print(f"Página montada em {destino}")
    else:
        site()
