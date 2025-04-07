import fitz  # PyMuPDF
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from spellchecker import SpellChecker
from PIL import Image, ImageTk
import io
import os

ARQUIVO_IGNORADAS = "palavras_ignoradas.txt"

# ==== Funções de Palavras Ignoradas ====
def carregar_palavras_ignoradas():
    if os.path.exists(ARQUIVO_IGNORADAS):
        with open(ARQUIVO_IGNORADAS, "r", encoding="utf-8") as f:
            return [p.strip() for p in f.read().split(",") if p.strip()]
    return []

def salvar_palavras_ignoradas(palavras):
    with open(ARQUIVO_IGNORADAS, "w", encoding="utf-8") as f:
        f.write(", ".join(palavras))

def adicionar_palavra():
    nova_palavra = campo_ignorar.get().strip()
    if nova_palavra and nova_palavra.lower() not in [p.lower() for p in palavras_ignoradas]:
        palavras_ignoradas.append(nova_palavra)
        atualizar_lista()
        campo_ignorar.delete(0, tk.END)

def remover_palavra():
    selecionada = listbox_palavras.curselection()
    if selecionada:
        indice = selecionada[0]
        palavra = listbox_palavras.get(indice)
        palavras_ignoradas.remove(palavra)
        atualizar_lista()

def salvar_lista_manual():
    salvar_palavras_ignoradas(palavras_ignoradas)
    messagebox.showinfo("Salvo", "Lista de palavras ignoradas salva com sucesso!")

def atualizar_lista():
    listbox_palavras.delete(0, tk.END)
    for palavra in palavras_ignoradas:
        listbox_palavras.insert(tk.END, palavra)

# ==== Processar PDF ====
def processar_pdf_com_erros(caminho_pdf, ignorar=[]):
    spell = SpellChecker(language='pt')
    doc = fitz.open(caminho_pdf)

    for page in doc:
        texto = page.get_text()
        palavras = re.findall(r'\b\w+\b', texto)
        palavras_unicas = set(palavras)

        for palavra in palavras_unicas:
            if (
                re.fullmatch(r'[\d.,]+', palavra) or
                re.fullmatch(r'(R\$|\$)?\d+[.,]?\d*', palavra) or
                (len(palavra) == 1 and palavra.lower() != "é") or
                palavra.lower() in [p.lower() for p in ignorar]
            ):
                continue

            if palavra.lower() not in spell:
                areas = page.search_for(palavra)
                for area in areas:
                    highlight = page.add_highlight_annot(area)
                    highlight.set_colors(stroke=(1, 0, 0))  # Vermelho
                    highlight.update()

    return doc

def exibir_pdf_na_tela(doc):
    for widget in frame_paginas.winfo_children():
        widget.destroy()

    for page in doc:
        pix = page.get_pixmap(dpi=120)
        img_data = Image.open(io.BytesIO(pix.tobytes("ppm")))
        img_tk = ImageTk.PhotoImage(img_data)

        label = tk.Label(frame_paginas, image=img_tk)
        label.image = img_tk
        label.pack(pady=5)

def selecionar_arquivo():
    caminho_pdf = filedialog.askopenfilename(
        title="Selecione um arquivo PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )

    if caminho_pdf:
        doc_com_erros = processar_pdf_com_erros(caminho_pdf, ignorar=palavras_ignoradas)
        exibir_pdf_na_tela(doc_com_erros)
        doc_com_erros.close()

# ==== INTERFACE ====
janela = tk.Tk()
janela.title("Visualizador de PDF com Erros Ortográficos")
janela.geometry("850x650")

notebook = ttk.Notebook(janela)
notebook.pack(fill="both", expand=True)

# ==== Aba 1: Visualizar PDF ====
aba_visualizar = ttk.Frame(notebook)
notebook.add(aba_visualizar, text="Visualizar PDF")

frame_topo = tk.Frame(aba_visualizar)
frame_topo.pack(pady=10)

botao_pdf = tk.Button(frame_topo, text="Selecionar PDF", command=selecionar_arquivo, font=("Arial", 11), bg="lightblue")
botao_pdf.pack()

canvas = tk.Canvas(aba_visualizar)
scroll_y = tk.Scrollbar(aba_visualizar, orient="vertical", command=canvas.yview)
frame_paginas = tk.Frame(canvas)

frame_paginas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=frame_paginas, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)

canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

# ==== Aba 2: Palavras Ignoradas ====
aba_ignorar = ttk.Frame(notebook)
notebook.add(aba_ignorar, text="Palavras Ignoradas")

frame_ignorar = tk.Frame(aba_ignorar, pady=20)
frame_ignorar.pack()

tk.Label(frame_ignorar, text="Adicionar nova palavra a ignorar:", font=("Arial", 11)).pack(pady=5)

campo_ignorar = tk.Entry(frame_ignorar, width=40)
campo_ignorar.pack(pady=5)

botao_adicionar = tk.Button(frame_ignorar, text="Adicionar", command=adicionar_palavra, font=("Arial", 10), bg="#ccc")
botao_adicionar.pack(pady=5)

botao_remover = tk.Button(frame_ignorar, text="Remover Palavra Selecionada", command=remover_palavra, font=("Arial", 10), bg="#f08080")
botao_remover.pack(pady=5)

botao_salvar = tk.Button(frame_ignorar, text="Salvar Lista", command=salvar_lista_manual, font=("Arial", 10), bg="lightgreen")
botao_salvar.pack(pady=5)

tk.Label(frame_ignorar, text="Palavras ignoradas:", font=("Arial", 11)).pack(pady=5)

listbox_palavras = tk.Listbox(frame_ignorar, width=50, height=10)
listbox_palavras.pack(pady=5)

# ==== Inicializar lista ====
palavras_ignoradas = carregar_palavras_ignoradas()
atualizar_lista()

janela.mainloop()
