import streamlit as st
import json
import pandas as pd
import re
import random
from io import BytesIO
from PIL import Image

def is_mocao(name):
    return bool(re.search(r'(\bEC\w*|Esta Casa)', name, re.IGNORECASE))

def get_responsavel(card, members_dict):
    id_members = card.get('idMembers', [])
    if not id_members:
        return None
    nomes = [members_dict[m] for m in id_members if m in members_dict]
    if not nomes:
        return None
    if len(nomes) == 1:
        return nomes[0]
    return nomes

def escape_quotes(obj):
    if isinstance(obj, str):
        return obj.replace('"', '\\"')
    elif isinstance(obj, list):
        return [escape_quotes(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: escape_quotes(v) for k, v in obj.items()}
    else:
        return obj

def unescape_quotes(obj):
    if isinstance(obj, str):
        return obj.replace('\\"', '"')
    elif isinstance(obj, list):
        return [unescape_quotes(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: unescape_quotes(v) for k, v in obj.items()}
    else:
        return obj

def is_excluido(nome, excluidos):
    if not nome:
        return False
    nome_lower = nome.strip().lower()
    return any(ex in nome_lower for ex in [n.strip().lower() for n in excluidos if n.strip()])

def is_dca(nome, dca_names):
    if not nome:
        return False
    nome_lower = nome.strip().lower()
    return any(dca in nome_lower for dca in [n.strip().lower() for n in dca_names if n.strip()])

def escolher_testadores(todos_membros, responsavel, excluidos, dca_names):
    if isinstance(responsavel, list):
        membros_validos = [m for m in todos_membros if m not in responsavel and not is_excluido(m, excluidos)]
    else:
        membros_validos = [m for m in todos_membros if m != responsavel and not is_excluido(m, excluidos)]
    random.shuffle(membros_validos)
    for i in range(len(membros_validos)):
        for j in range(i+1, len(membros_validos)):
            m1, m2 = membros_validos[i], membros_validos[j]
            if not (is_dca(m1, dca_names) and is_dca(m2, dca_names)):
                return [m1, m2]
    return membros_validos[:2]

def test_restricoes(cards, todos_membros, excluidos, dca_names):
    for card in cards:
        t1, t2 = card['testadores']
        responsavel = card['responsavel']
        assert not is_excluido(t1, excluidos), f"Testador {t1} é excluído"
        assert not is_excluido(t2, excluidos), f"Testador {t2} é excluído"
        if isinstance(responsavel, list):
            assert t1 not in responsavel, f"Testador {t1} é responsável"
            assert t2 not in responsavel, f"Testador {t2} é responsável"
        else:
            assert t1 != responsavel, f"Testador {t1} é responsável"
            assert t2 != responsavel, f"Testador {t2} é responsável"
        assert not (is_dca(t1, dca_names) and is_dca(t2, dca_names)), f"Ambos testadores são DCAs: {t1}, {t2}"
    st.warning("Todos os testes passaram!")

def main():
    st.markdown(
        '''
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
        body, .stApp {
            background-color: #f8bc64 !important;
        }
        .stApp {
            color: #d45c0c !important;
            font-family: 'Montserrat', 'Segoe UI', sans-serif !important;
        }
        .css-18e3th9, .stTextInput>div>div>input, .stNumberInput>div>input, .stDataFrame, .stDataFrame table {
            background: #ec7518 !important;
            color: #d45c0c !important;
            font-family: 'Montserrat', 'Segoe UI', sans-serif !important;
            font-weight: bold !important;
        }
        .stButton>button {
            background-color: #fff !important;
            color: #ec7518 !important;
            border: none;
            border-radius: 6px;
            padding: 0.5em 1.5em;
            font-weight: bold !important;
            font-family: 'Montserrat', 'Segoe UI', sans-serif !important;
            transition: background 0.2s;
        }
        .stButton>button:hover {
            background-color: #111 !important;
            color: #ec7518 !important;
        }
        /* Reduz tamanho do botão de upload */
        .stFileUploader button {
            font-size: 1em !important;
            padding: 0.4em 1em !important;
        }
        .stTextInput>div>div>input, .stNumberInput>div>input {
            background: #ec7518 !important;
            color: #fff !important;
            border: 2px solid #fff !important;
            border-radius: 6px;
            font-weight: bold !important;
        }
        .stDataFrame, .stDataFrame table {
            background: #ec7518 !important;
            color: #fff !important;
            font-weight: bold !important;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #d45c0c !important;
            font-family: 'Montserrat', 'Segoe UI', sans-serif !important;
            font-weight: bold !important;
        }
        .stDownloadButton>button {
            background-color: #fff !important;
            color: #ec7518 !important;
            border-radius: 6px;
            font-weight: bold !important;
            border: 2px solid #fff !important;
            font-family: 'Montserrat', 'Segoe UI', sans-serif !important;
        }
        .stDownloadButton>button:hover {
            background-color: #111 !important;
            color: #ec7518 !important;
        }
        label, .stTextInput label, .stNumberInput label, .stMarkdown, .st-bb, .st-c3, .st-c4, .st-c5, .st-c6, .st-c7, .st-c8, .st-c9 {
            font-weight: bold !important;
            color: #d45c0c !important;
        }
        </style>
        ''',
        unsafe_allow_html=True
    )
    # Adiciona o logo centralizado
    logo = Image.open("logo_sd.png")
    st.image(logo, width=120)
    st.markdown(
        "<div style='text-align:center; font-family:Montserrat,Segoe UI,sans-serif; color:#d45c0c; font-size:1.3em; font-weight:bold;'>"
        "SDUFRJ - Sociedade de Debates"
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown("<h2 style='color:#d45c0c; text-align:center; font-weight:bold;'>Distribuição de Moções para Testadores</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader('Faça upload do JSON exportado do Trello', type='json')
    if not uploaded_file:
        st.stop()

    col_name = st.text_input('Nome da coluna de teste (ex: Aprovadas para teste)', value='Aprovadas para teste')

    st.markdown('**Nomes dos DCAs (um por campo):**')
    dca_names = []
    dca_1 = st.text_input('DCA 1', key='dca_1')
    if dca_1:
        dca_names.append(dca_1.strip())
    dca_idx = 2
    while True:
        dca = st.text_input(f'DCA {dca_idx}', key=f'dca_{dca_idx}')
        if dca:
            dca_names.append(dca.strip())
            dca_idx += 1
        else:
            break

    st.markdown('**Nomes dos que NÃO vão testar (um por campo):**')
    excluidos = []
    exc_1 = st.text_input('Não testa 1', key='exc_1')
    if exc_1:
        excluidos.append(exc_1.strip())
    exc_idx = 2
    while True:
        exc = st.text_input(f'Não testa {exc_idx}', key=f'exc_{exc_idx}')
        if exc:
            excluidos.append(exc.strip())
            exc_idx += 1
        else:
            break

    qtd_mocoes = st.number_input('Quantidade de moções a serem testadas (para validação)', min_value=1, value=24)

    # Botão para iniciar o processamento
    if not st.button('Separar testes'):
        st.stop()

    with st.spinner('Processando...'):
        data = json.load(uploaded_file)
        # Mapeia membros
        members_dict = {}
        if 'members' in data:
            for m in data['members']:
                members_dict[m['id']] = m.get('fullName')

        # Busca id da lista
        id_list = None
        if 'lists' in data:
            for l in data['lists']:
                if l.get('name', '').strip().lower() == col_name.strip().lower():
                    id_list = l['id']
                    break
        if not id_list:
            st.error('Coluna não encontrada no JSON!')
            st.stop()

        # Filtra cards
        cards = data.get('cards', [])
        resultado = []
        for card in cards:
            if card.get('idList') != id_list:
                continue
            if not is_mocao(card.get('name', '')):
                continue
            card_dict = {
                'titulo': card.get('name', ''),
                'descricao': card.get('desc', ''),
                'responsavel': get_responsavel(card, members_dict)
            }
            resultado.append(escape_quotes(card_dict))

        # Seleção de testadores
        todos_membros = [m.get('fullName') for m in data.get('members', [])]
        for card in resultado:
            card['testadores'] = escolher_testadores(todos_membros, card['responsavel'], excluidos, dca_names)

        # Validação
        if len(resultado) != qtd_mocoes:
            st.warning(f"Atenção: Foram encontradas {len(resultado)} moções, mas o esperado era {qtd_mocoes}.")

        # Testa restrições
        try:
            test_restricoes(resultado, todos_membros, excluidos, dca_names)
        except AssertionError as e:
            st.error(str(e))

        # Monta DataFrame para Excel
        df = pd.DataFrame([
            {
                'Moção': unescape_quotes(c['titulo']),
                'Infoslide': unescape_quotes(c['descricao']),
                'Autor': unescape_quotes(c['responsavel']),
                'Testador 1': unescape_quotes(c['testadores'][0]) if c['testadores'] else None,
                'Testador 2': unescape_quotes(c['testadores'][1]) if c['testadores'] and len(c['testadores']) > 1 else None
            }
            for c in resultado
        ])

        # Download Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)

    # Banner de sucesso
    st.warning("Arquivo gerado com sucesso! Faça o download abaixo.")

    st.download_button(
        label='Baixar resultado em Excel',
        data=output.getvalue(),
        file_name='mocoes_testadores.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    st.dataframe(df)

    # Imagem divertida no final
    st.markdown("---")
    img = Image.open("dracotia.png")
    st.image(img, caption="Parabéns! Testes separados com sucesso.", width=300)

if __name__ == '__main__':
    main()
