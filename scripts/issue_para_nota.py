"""Transforma uma proposta de nota (issue com o formulário "nova-nota") num ficheiro de nota.

Usado pela automação do GitHub. Lê o texto da issue em ISSUE_BODY e escreve a nota em notas/.
Em caso de problema, escreve a explicação em _erro.txt e termina com código 1.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import biblia as B  # noqa: E402
import validar  # noqa: E402

CAMPOS = {
    "Versículo": "referencia", "Pergunta": "pergunta", "Tipo de dúvida": "tipo", "Resposta": "resposta",
    "Mais à frente na Bíblia (opcional)": "adiante", "O teu nome (opcional)": "nome",
}
TIPO_POR_NOME = {v: k for k, v in B.TIPOS.items()}
VAZIO = "_No response_"


def falhar(msg):
    open(os.path.join(B.RAIZ, "_erro.txt"), "w", encoding="utf-8").write(msg)
    print(msg)
    sys.exit(1)


def ler_formulario(corpo):
    secoes = re.split(r"^### ", corpo.replace("\r\n", "\n"), flags=re.M)
    out = {}
    for s in secoes[1:]:
        titulo, _, valor = s.partition("\n")
        chave = CAMPOS.get(titulo.strip())
        if chave:
            valor = valor.strip()
            out[chave] = "" if valor == VAZIO else valor
    return out


def main():
    f = ler_formulario(os.environ.get("ISSUE_BODY", ""))
    numero = os.environ.get("ISSUE_NUMBER", "0")
    ref = f.get("referencia", "")
    m = re.match(r"^\s*(.+?)\s+(\d+)\s*:\s*(\d+)\s*$", ref)
    if not m or m.group(1) not in B.CODIGO_POR_NOME:
        falhar(f"Não consegui ler o versículo \"{ref}\". Escreve-o assim: Êxodo 3:5")
    cod, cap, vers = B.CODIGO_POR_NOME[m.group(1)], int(m.group(2)), int(m.group(3))
    pl = B.plano()
    dia = B.dia_do_versiculo(pl, cod, cap, vers)
    if not dia:
        falhar(f"O versículo {ref} não existe ou não está no plano.")
    epoca = next(e["id"] for e in pl["epocas"] if e["dia_inicio"] <= dia <= e["dia_fim"])
    pasta = os.path.join(B.NOTAS_DIR, f"epoca-{epoca:02d}")
    i = 0
    while os.path.exists(os.path.join(pasta, B.nome_ficheiro(cod, cap, vers, i))):
        i += 1
    caminho = os.path.join(pasta, B.nome_ficheiro(cod, cap, vers, i))
    par = lambda t: [p.strip().replace("\n", " ") for p in re.split(r"\n\s*\n", t or "") if p.strip()]
    autor = f.get("nome") or os.environ.get("ISSUE_USER", "")
    B.escrever_nota(caminho, {
        "ref": f"{B.NOME[cod]} {cap}:{vers}", "livro": cod, "capitulo": cap, "versiculo": vers,
        "pergunta": f.get("pergunta", "").strip(), "tipo": TIPO_POR_NOME.get(f.get("tipo", ""), ""),
        "prioridade": "B", "diagrama": "", "estado": "rascunho", "autores": [autor] if autor else [],
        "resposta": par(f.get("resposta")), "adiante": par(f.get("adiante")),
    })
    erros, _ = validar.validar([B.ler_nota(caminho)])
    if erros:
        os.remove(caminho)
        falhar("A proposta ainda não pode entrar. O verificador encontrou isto:\n\n"
               + "\n".join(f"- {m}" for _, m in erros)
               + "\n\nEdita a issue para corrigir e volta a pôr a etiqueta `aprovar`.")
    rel = os.path.relpath(caminho, B.RAIZ)
    print(f"Nota criada: {rel} (proposta #{numero})")
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as o:
            o.write(f"ficheiro={rel}\nref={B.NOME[cod]} {cap}:{vers}\n")


if __name__ == "__main__":
    main()
