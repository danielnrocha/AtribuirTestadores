# 🟧 Distribuição de Moções para Testadores - SDUFRJ

![Logo SDUFRJ](logo_sd.png)

**Distribua moções e infoslides de forma justa, rápida e visualmente agradável!**

---

## ✨ Sobre o app

Este app Streamlit foi criado para a **SDUFRJ - Sociedade de Debates da UFRJ** e permite:

- Upload do JSON exportado do Trello
- Escolha da coluna de moções a serem testadas
- Cadastro dinâmico de DCAs e membros que não podem testar
- Sorteio automático de testadores, respeitando todas as restrições:
  - Nenhum testador pode ser o autor
  - Nenhum testador pode ser DCA junto com outro DCA
  - Nenhum testador pode estar na lista de excluídos
- Exportação do resultado em Excel
- Visual moderno, responsivo e customizado nas cores da SDUFRJ

---

## 🚀 Como rodar localmente

1. **Clone o repositório:**
   ```sh
   git clone https://github.com/seu-usuario/seu-repo.git
   cd seu-repo
   ```

2. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Rode o app:**
   ```sh
   streamlit run extract_trello_streamlit.py
   ```

---

## ☁️ Deploy na Streamlit Cloud

1. Suba este repositório para o GitHub.
2. Acesse [Streamlit Cloud](https://streamlit.io/cloud) e conecte seu GitHub.
3. Crie um novo app apontando para `extract_trello_streamlit.py`.
4. Pronto! Compartilhe o link com seu time.

---

## 📸 Visual

![Screenshot do app](screenshot.png)

---

## 🧡 Feito para a SDUFRJ

<div align="center">
  <img src="logo_sd.png" width="20"/><br>
  <b>SDUFRJ - Sociedade de Debates</b>
</div>

---

## 📄 Licença

MIT

---

> Dúvidas ou sugestões? Abra uma issue ou envie um pull request!
