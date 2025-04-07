# 📝 Identificador de Erros Ortográficos em PDFs

Este projeto em Python utiliza OCR e verificação ortográfica para identificar **erros de ortografia em arquivos PDF** e **marcá-los visualmente em vermelho**. Além disso, possui uma **interface gráfica com abas** feita em Tkinter para facilitar a visualização e o controle de palavras ignoradas.

---

## 📸 Funcionalidades

- ✅ Detecção automática de erros ortográficos em português.
- 🖍️ Marcação em vermelho sobre as palavras incorretas.
- 📂 Visualização do PDF diretamente na interface.
- 🚫 Lista de palavras ignoradas personalizável.
- 💾 Salvamento das palavras ignoradas em arquivo.
- ➕ Adicionar/Remover palavras ignoradas facilmente via interface.

---

## 🛠️ Tecnologias Usadas

- Python 3.10+
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- [PySpellChecker](https://github.com/barrust/pyspellchecker)
- Tkinter (interface gráfica)
- Pillow (para exibir imagens)

---

## 📦 Instalação

```bash
pip install pymupdf pyspellchecker pillow
