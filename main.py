import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog, ttk, messagebox
import csv, os
import matplotlib.colors as mcolors

file_path = None
contexto = None

def quantitativa_continua(df, coluna):
    # Ordena os valores da coluna selecionada
    df_sorted = df[coluna].dropna().sort_values()
    # Cálculos estatísticos
    menor_valor = df_sorted.min()
    maior_valor = df_sorted.max()
    amplitude = maior_valor - menor_valor
    n = len(df_sorted)
    k = max(round(n ** 0.5), 1)  # Garante que k seja pelo menos 1
    bins = np.linspace(menor_valor, maior_valor, k + 1)
    # Alteração: right=True para incluir o valor máximo
    intervalos = pd.cut(df_sorted, bins=bins, include_lowest=True, right=True)
    freq_absoluta = intervalos.value_counts().sort_index()
    freq_relativa = freq_absoluta / n
    freq_percentual = freq_relativa * 100
    freq_acumulada = freq_absoluta.cumsum()
    freq_percentual_acumulada = freq_percentual.cumsum()
    # Formata os intervalos
    intervalos_formatados = [
        f"{interval.left:.2f} -- {interval.right:.2f}" 
        for interval in freq_absoluta.index
    ]
    tabela = pd.DataFrame({
        'Classes': intervalos_formatados,
        'Freq. Absoluta': freq_absoluta.values,
        'Freq. Relativa': freq_relativa.values,
        'Freq. Percentual (%)': freq_percentual.values,
        'Freq. Percentual Acumulada (%)': freq_percentual_acumulada.values,
        'Freq. Acumulada': freq_acumulada.values
    })
    return tabela

def quantitativa_discreta(df, coluna):
    # Cálculo das frequências
    freq_absoluta = df[coluna].value_counts().sort_index()
    freq_relativa = freq_absoluta / len(df)
    freq_percentual = freq_relativa * 100
    freq_acumulada = freq_absoluta.cumsum()
    freq_percentual_acumulada = freq_percentual.cumsum()
    # Criação do DataFrame de resultados
    tabela = pd.DataFrame({
        'Values': freq_absoluta.index,
        'Freq. Absoluta': freq_absoluta.values,
        'Freq. Relativa': freq_relativa.values,
        'Freq. Percentual': freq_percentual.values,
        'Freq. Percentual Acumulada': freq_percentual_acumulada.values,
        'Freq. Acumulada': freq_acumulada.values
    })
    return tabela
def qualitativa(df, coluna):
   # Cálculo das frequências
    freq_absoluta = df[coluna].value_counts().sort_index()
    freq_relativa = freq_absoluta / len(df)
    freq_percentual = freq_relativa * 100
    freq_acumulada = freq_absoluta.cumsum()
    freq_percentual_acumulada = freq_percentual.cumsum()
    # Criação do DataFrame de resultados
    tabela = pd.DataFrame({
        'Categoria': freq_absoluta.index,
        'Freq. Absoluta': freq_absoluta.values,
        'Freq. Relativa': freq_relativa.values,
        'Freq. Percentual (%)': freq_percentual.values,
        'Freq. Percentual Acumulada (%)': freq_percentual_acumulada.values,
        'Freq. Acumulada': freq_acumulada.values
    })
    return tabela
def extrair_amostra():
    banco_dados = input('Digite o nome do banco de que vc deseja extrair a amostra ou o caminho caso esteja fora da pasta padrão: ')
    dados = pd.read_csv(banco_dados)
    tamanho = int(input('Qual o tamanho da amostra que você deseja extrair: '))
    amostra = dados.sample(n=tamanho, random_state=42)
    nome = input('Digite o nome do novo arquivo a ser salvo: ')
    amostra.to_csv(nome + '.csv', index=False)
def grafico_barras(dataframe, nome_x, nome_y):
    plt.rcParams['axes.titlepad'] = 16  # Ajusta o espaço entre o título e o gráfico
    plt.rcParams['axes.labelsize'] = 12  # Tamanho das legendas dos eixos
    plt.rcParams['xtick.labelsize'] = 10  # Tamanho das legendas do eixo X
    plt.rcParams['ytick.labelsize'] = 10  # Tamanho das legendas do eixo Y
    try:
        valores = dataframe.iloc[:, 0]  # Primeiro coluna (valores para o eixo X)
        frequencias = dataframe.iloc[:, 1]  # Segunda coluna (frequências para o eixo Y)
        plt.figure(figsize=(10, 6))
        plt.bar(valores, frequencias, color=plt.cm.coolwarm(frequencias / max(frequencias)), edgecolor='black')  
        plt.title('Gráfico de Barras')
        plt.xlabel(nome_x)
        plt.ylabel(nome_y)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Erro ao gerar o gráfico: {e}")
             
def grafico_cruzado_barras(dataframe, col_x, col_y, titulo):
        plt.figure(figsize=(8, 6))
        sns.barplot(data=dataframe, x=col_x, y=col_y, palette=["red", "blue"])
        plt.title(titulo, fontsize=16)
        plt.xlabel(col_x, fontsize=14)
        plt.ylabel(col_y, fontsize=14)
        plt.xticks(rotation=45, fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()
        plt.show()
def grafico_cruzado_linhas(dataframe, col_x, col_y, titulo, labels=None):
    plt.figure(figsize=(8, 6))
    if labels:
        # Se houver labels, assumimos que os grupos estão indicados em uma coluna do DataFrame
        sns.lineplot(data=dataframe, x=col_x, y=col_y, hue=labels, marker="o")
    else:
        # Sem labels, traça uma única linha
        sns.lineplot(data=dataframe, x=col_x, y=col_y, marker="o", color="blue")
    plt.title(titulo, fontsize=16)
    plt.xlabel(col_x, fontsize=14)
    plt.ylabel(col_y, fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.tight_layout()
    plt.show()
def create_formatted_button(parent, text, command):
    button = tk.Button(parent, text=text, command=command, font=("Helvetica", 14), bg="white", relief="solid", bd=1)
    return button

def create_formatted_buttonII(parent, text, command):
    button = tk.Button(parent, text=text, command=command, font=("Helvetica", 14), bg="white", relief="solid", bd=1, width=26)
    return button

def create_formatted_buttonIII(parent, text, command):
    button = tk.Button(parent, text=text, command=command, font=("Helvetica", 14), bg="blue", fg="white", relief="solid", bd=1, width=15, height=2)
    return button

def show_initial_screen():
    for widget in root.winfo_children():
        widget.destroy()
    img = Image.open('probabilidade.png')
    img = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    label = tk.Label(root, image=img)
    label.image = img
    label.pack(expand=True)
    label.bind("<Button-1>", lambda e: show_menu_screen())

def show_menu_screen():
    for widget in root.winfo_children():
        widget.destroy()
    
    # Carregar a imagem de fundo
    bg_image = Image.open("background.png")
    bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    # Criar um Label para exibir a imagem de fundo
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo  # Manter uma referência da imagem para evitar que seja coletada pelo garbage collector
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    frame_width = root.winfo_screenwidth() * 0.5  # 50% da largura da tela
    frame_height = root.winfo_screenheight()
    frame = tk.Frame(root, bg="black", width=frame_width, height=frame_height)
    frame.place(relx=0.25, rely=0, relwidth=0.5, relheight=1)  # Centraliza o frame horizontalmente
    title = tk.Label(frame, text="Menu de opções", font=("Helvetica", 24), bg="black", fg='white')
    title.pack(pady=90)
    
    # Carregar a pequena imagem
    small_image = Image.open("cvw.png")
    small_image = small_image.resize((150, 150), Image.LANCZOS)
    small_photo = ImageTk.PhotoImage(small_image)
    
    # Criar um Label para exibir a pequena imagem
    small_label = tk.Label(root, image=small_photo, bg="white")
    small_label.image = small_photo  # Manter uma referência da imagem para evitar que seja coletada pelo garbage collector
    small_label.place(relx=1.0, rely=1.0, anchor='se')  # Posicionar no canto inferior direito

    buttons_frame = tk.Frame(frame, bg="black")
    buttons_frame.pack(pady=20)  # Adiciona um pouco de espaço ao redor dos botões
    buttons = [
        ("Atividade II", "atividade_II"),
        ("Atividade III A", "atividade_IIIA"),
        ("Atividade III B", "atividade_IIIB"),
        ("Atividade III C", "atividade_IIIC"),
        ("Nova Quantitativa D", "quantitativa_discreta"),
        ("Nova Quantitativa C", "quantitativa_continua"),
        ("Nova Qualitativa", "qualitativa"),
        ("Sair", "sair")
    ]
    for i, (text, contexto) in enumerate(buttons):
        if contexto == "sair":
            btn_command = root.quit
        else:
            btn_command = lambda ctx=contexto: show_activity_screen(ctx)
        btn = create_formatted_buttonII(buttons_frame, text, btn_command)
        btn.grid(row=i % 4, column=i // 4, padx=40, pady=20, sticky='nsew')
    for row_index in range(4):
        buttons_frame.grid_rowconfigure(row_index, weight=0)  # Não expande as linhas
    for col_index in range(2):
        buttons_frame.grid_columnconfigure(col_index, weight=1)  # Expande as colunas igualmente

def show_activity_screen(ctx):
    global contexto
    contexto = ctx
    for widget in root.winfo_children():
        widget.destroy()
    left_frame = tk.Frame(root, bg="darkblue", width=root.winfo_screenwidth() // 3)
    left_frame.pack(side="left", fill="y")
    right_frame = tk.Frame(root, bg="white")
    right_frame.pack(side="left", expand=True, fill="both")
    buttons_frame = tk.Frame(left_frame, bg="darkblue")
    buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
    criar_botoes(buttons_frame)
def criar_botoes(frame):
    global contexto
    buttons = []
    if file_path:
        nome_arquivo = os.path.basename(file_path)
        titulo_label = tk.Label(frame, text=f"Arquivo: {nome_arquivo}", font=("Helvetica", 14, "bold"), bg="darkblue", fg="white")
        titulo_label.pack(pady=10)
   
    if contexto == "atividade_II":
        buttons = [
            ("Demonstração I", lambda: atvII_arquivoI()),
            ("Arquivo", lambda: mostrar_tabela(file_path)),
            ("Valores", lambda: mostrar_valoresQC(file_path)),
            ("Gráfico bloxplot", lambda: show_bloxplot()),
            ("Voltar ao Menu", show_menu_screen)
        ]
    elif contexto == "atividade_IIIA":
        buttons = [
            ("Demonstração I", lambda: atvIIIA_arquivoI()),
            ("Mostrar arquivo", lambda: mostrar_tabela(file_path)),
            ("Tabela de frequencias", lambda: show_qualitativa()),
            ("Grafico de barras", lambda: show_grafico_barras()),
            ("Grafico circular", lambda: show_grafico_pizza()), 
            ("Voltar ao Menu", show_menu_screen)
        ]
    elif contexto == "atividade_IIIB":
        buttons = [
            ("Demonstração I", lambda: atvIIIB_arquivoI()),
            ("Mostrar arquivo", lambda: mostrar_tabela(file_path)),
            ("Tabela de frequencias", lambda: show_quantitativa_discreta()),
            ("Grafico de barras", lambda: show_grafico_barras()),
            ("Grafico circular", lambda: show_grafico_pizza()),
            ("Voltar ao Menu", show_menu_screen)
        ]
    elif contexto == "atividade_IIIC":
        buttons = [
            ("Demonstração I", lambda: atvIIIC_arquivoI()),
            ("Mostrar arquivo", lambda: mostrar_tabela(file_path)),
            ("Tabela de frequencias", lambda: show_tableQC()),
            ("Valores", lambda: mostrar_valoresQC(file_path)),
            ("Grafico de barras", lambda: show_grafico_barras()),
            ("Grafico circular", lambda: show_grafico_pizza()), 
            ("Gráfico bloxplot", lambda: show_bloxplot()),
            ("Voltar ao Menu", show_menu_screen)
        ]
    elif contexto == "quantitativa_discreta":
        buttons = [
            ("Ler novo csv", lambda: reset_interfaceCSV()),
            ("Extrair amostra", lambda: show_extrair_amostra()),
            ("Mostrar arquivo", lambda: mostrar_tabela(file_path)),
            ("Tabela de frequencias", lambda: show_quantitativa_discreta()),
            ("Grafico de barras", lambda: show_grafico_barras()),
            ("Grafico circular", lambda: show_grafico_pizza()), 
            ("Gráfico bloxplot", lambda: show_bloxplot()),
            ("Voltar ao Menu", show_menu_screen)  
        ]
    elif contexto == "quantitativa_continua":
        buttons = [
            ("Ler novo csv", lambda: reset_interfaceCSV()),
            ("Extrair amostra", lambda: show_extrair_amostra()),
            ("Mostrar arquivo", lambda: mostrar_tabela(file_path)),
            ("Tabela de frequencias", lambda: show_tableQC()),
            ("Valores", lambda: mostrar_valoresQC(file_path)),
            ("Grafico de barras", lambda: show_grafico_barras()),
            ("Grafico circular", lambda: show_grafico_pizza()), 
            ("Gráfico bloxplot", lambda: show_bloxplot()),
            ("Voltar ao Menu", show_menu_screen)  
        ]
    elif contexto == "qualitativa":
            buttons = [
            ("Ler novo csv", lambda: reset_interfaceCSV()),
            ("Extrair amostra", lambda: show_extrair_amostra()),
            ("Mostrar arquivo", lambda: mostrar_tabela(file_path)),
            ("Tabela de frequencias", lambda: show_qualitativa()),
            ("Grafico de barras", lambda: show_grafico_barras()),
            ("Grafico circular", lambda: show_grafico_pizza()), 
            ("Voltar ao Menu", show_menu_screen)
            ]
    for i, (btn_text, btn_command) in enumerate(buttons):
        btn = create_formatted_buttonII(frame, btn_text, btn_command)
        btn.pack(pady=10, padx=20, ipadx=0, ipady=10)
def reset_interfaceCSV():
    global contexto
    for widget in root.winfo_children():
        widget.destroy()
    left_frame = tk.Frame(root, bg="darkblue", width=root.winfo_screenwidth() // 3)
    left_frame.pack(side="left", fill="y")
    right_frame = tk.Frame(root, bg="white")
    right_frame.pack(side="left", expand=True, fill="both")
    def chamar_csv():
        global file_path
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            df = pd.read_csv(file_path)
            print(f"Caminho do arquivo CSV: {file_path}")  # Armazena o caminho do arquivo CSV
            success_label.config(text="Arquivo CSV lido com sucesso!", fg="green")
        else:
            success_label.config(text="Erro ao ler o arquivo", fg="red")
 
    btn = create_formatted_buttonIII(right_frame, "Chamar CSV", chamar_csv)
    btn.place(relx=0.5, rely=0.4, anchor="center")
    success_label = tk.Label(right_frame, text="", font=("Helvetica", 12), bg="white")
    success_label.place(relx=0.5, rely=0.5, anchor="center")
    buttons_frame = tk.Frame(left_frame, bg="darkblue")
    buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
    criar_botoes(buttons_frame)
def show_extrair_amostra():
    global contexto
    for widget in root.winfo_children():
        widget.destroy()
    left_frame = tk.Frame(root, bg="darkblue", width=root.winfo_screenwidth() // 3)
    left_frame.pack(side="left", fill="y")
    right_frame = tk.Frame(root, bg="white")
    right_frame.pack(side="left", expand=True, fill="both")
    def ler_outro_csv():
        global file_path
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            file_label.config(text=f"Arquivo atual: {file_path}")
            success_label.config(text="Arquivo CSV lido com sucesso!", fg="green")
        else:
            success_label.config(text="Erro ao ler o arquivo", fg="red")
    def extrair_amostra_func():
        if file_path:
            try:
                dados = pd.read_csv(file_path)
                tamanho = int(tamanho_entry.get())
                amostra = dados.sample(n=tamanho, random_state=42)
                nome = nome_entry.get()
                amostra.to_csv(nome + '.csv', index=False)
                success_label.config(text="Amostra extraída e salva com sucesso!", fg="green")
            except Exception as e:
                success_label.config(text=f"Erro ao salvar a amostra: {e}", fg="red")
        else:
            success_label.config(text="Nenhum arquivo CSV selecionado", fg="red")
    # Exibe o nome do arquivo atual
    file_label = tk.Label(right_frame, text=f"Arquivo atual: {file_path}", font=("Helvetica", 12), bg="white")
    file_label.pack(pady=10)
    # Botão para ler outro CSV
    btn_ler_csv = create_formatted_buttonIII(right_frame, "Ler outro CSV", ler_outro_csv)
    btn_ler_csv.pack(pady=10)
    # Entrada para a quantidade de dados a serem extraídos
    tk.Label(right_frame, text="Quantidade de dados a serem extraídos:", font=("Helvetica", 12), bg="white").pack(pady=10)
    tamanho_entry = tk.Entry(right_frame, font=("Helvetica", 12))
    tamanho_entry.pack(pady=10)
    # Entrada para o nome do novo arquivo
    tk.Label(right_frame, text="Nome do novo arquivo:", font=("Helvetica", 12), bg="white").pack(pady=10)
    nome_entry = tk.Entry(right_frame, font=("Helvetica", 12))
    nome_entry.pack(pady=10)
    # Botão para extrair a amostra
    btn_extrair = create_formatted_buttonIII(right_frame, "Extrair Amostra", extrair_amostra_func)
    btn_extrair.pack(pady=10)
    # Label para exibir mensagens de sucesso ou erro
    success_label = tk.Label(right_frame, text="", font=("Helvetica", 12), bg="white")
    success_label.pack(pady=10)
    # Recria os botões no lado esquerdo
    buttons_frame = tk.Frame(left_frame, bg="darkblue")
    buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
    criar_botoes(buttons_frame)

def mostrar_valoresQC(file_path):
    for widget in root.winfo_children():
        widget.destroy()
    left_frame = tk.Frame(root, bg="darkblue", width=root.winfo_screenwidth() // 3)
    left_frame.pack(side="left", fill="y")
    right_frame = tk.Frame(root, bg="white")
    right_frame.pack(side="left", expand=True, fill="both")
    if file_path:
        df = pd.read_csv(file_path)
        def analisar_coluna():
            global contexto
            coluna = coluna_entry.get()
            if coluna not in df.columns:
                success_label.config(text="Coluna não encontrada no arquivo CSV", fg="red")
                return
            df_coluna = df[coluna].sort_values()
            menor_valor = df_coluna.min()
            maior_valor = df_coluna.max()
            amplitude = maior_valor - menor_valor
            q1 = df_coluna.quantile(0.25)
            q2 = df_coluna.quantile(0.50)
            q3 = df_coluna.quantile(0.75)
            moda = df_coluna.mode()
            media = df_coluna.mean()
            mediana = df_coluna.median()
            variancia = df_coluna.var()
            desvio_padrao = df_coluna.std()
            coeficiente_variacao = desvio_padrao / media
            variaveis = [
                f"Menor valor = {menor_valor}",
                f"Maior valor = {maior_valor}",
                f"Amplitude = {amplitude}",
                f"Quartil 1 = {q1}",
                f"Quartil 2 = {q2}",
                f"Quartil 3 = {q3}",
                f"Moda = {moda[0] if not moda.empty else 'N/A'}",
                f"Média = {media}",
                f"Mediana = {mediana}",
                f"Variância = {variancia}",
                f"Desvio padrão = {desvio_padrao}",
                f"Coeficiente de variação = {coeficiente_variacao}"
            ]
            for widget in lista_frame.winfo_children():
                widget.destroy()
            for var in variaveis:
                tk.Label(lista_frame, text=var, font=("Helvetica", 12), bg="white").pack(anchor="w")
            success_label.config(text="Análise concluída com sucesso!", fg="green")
        titulo_label = tk.Label(right_frame, text=f"Título do arquivo: {file_path.split('/')[-1]}", font=("Helvetica", 16, "bold"), bg="white")
        titulo_label.pack(pady=10)
        tk.Label(right_frame, text="Nome da coluna:", font=("Helvetica", 12), bg="white").pack(pady=10)
        coluna_entry = tk.Entry(right_frame, font=("Helvetica", 12))
        coluna_entry.pack(pady=10)
        btn_analisar = create_formatted_buttonIII(right_frame, "Analisar Coluna", analisar_coluna)
        btn_analisar.pack(pady=10)
        lista_frame = tk.Frame(right_frame, bg="white")
        lista_frame.pack(fill="both", expand=True, padx=10, pady=10)
        success_label = tk.Label(right_frame, text="", font=("Helvetica", 12), bg="white")
        success_label.pack(pady=10)
    else:
        success_label = tk.Label(right_frame, text="Nenhum arquivo CSV selecionado", font=("Helvetica", 12), bg="white", fg="red")
        success_label.pack(pady=10)
    buttons_frame = tk.Frame(left_frame, bg="darkblue")
    buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
    criar_botoes(buttons_frame)

def show_tableQC():
    global contexto, file_path
    if not file_path:
        messagebox.showerror("Erro", "Nenhum arquivo CSV selecionado.")
        return
    for widget in root.winfo_children():
        widget.destroy()
    left_frame = tk.Frame(root, bg="darkblue", width=root.winfo_screenwidth() // 3)
    left_frame.pack(side="left", fill="y")
    right_frame = tk.Frame(root, bg="white")
    right_frame.pack(side="right", expand=True, fill="both")
    df = pd.read_csv(file_path)
    coluna_entry = tk.Entry(right_frame, font=("Helvetica", 12))
    success_label = tk.Label(right_frame, text="", font=("Helvetica", 12), bg="white")
    
    def analisar_coluna():
        
        coluna = coluna_entry.get()
        if coluna not in df.columns:
            success_label.config(text="Coluna não encontrada no arquivo CSV", fg="red")
            return
        df_coluna = df[coluna].dropna()
        if not pd.api.types.is_numeric_dtype(df_coluna):
            success_label.config(text="A coluna selecionada não é numérica", fg="red")
            return
        # Utiliza a função corrigida
        tabela = quantitativa_continua(df, coluna)
        if tabela['Freq. Absoluta'].sum() != len(df_coluna):
            success_label.config(text="Aviso: A soma das frequências não corresponde ao total de dados.", fg="orange")
        else:
            success_label.config(text="Análise concluída com sucesso!", fg="green")
        
        for widget in right_frame.winfo_children():
            if widget != coluna_entry and widget != success_label and isinstance(widget, tk.Label):
                widget.destroy()
        
        # Frame para Treeview e Scrollbars
        tree_frame = tk.Frame(right_frame)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        tree = ttk.Treeview(tree_frame, columns=list(tabela.columns), show='headings')
        for col in tabela.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=150)
        for index, row in tabela.iterrows():
            tree.insert("", "end", values=list(row))
        tree.pack(side="left", fill="both", expand=True)
        
        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")
        
        scrollbar_x = ttk.Scrollbar(right_frame, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(fill="x")
        
        success_label.pack(pady=10)
    
    titulo_label = tk.Label(
        right_frame,
        text=f"Título do arquivo: {os.path.basename(file_path)}",
        font=("Helvetica", 16, "bold"),
        bg="white"
    )
    titulo_label.pack(pady=10)
    tk.Label(right_frame, text="Nome da coluna:", font=("Helvetica", 12), bg="white").pack(pady=5)
    coluna_entry.pack(pady=5)
    btn_analisar = create_formatted_buttonIII(right_frame, "Mostrar Tabela", analisar_coluna)
    btn_analisar.pack(pady=10)
    success_label.pack(pady=5)
    buttons_frame = tk.Frame(left_frame, bg="darkblue")
    buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
    criar_botoes(buttons_frame)
    
def mostrar_tabela(file_path):
    for widget in root.winfo_children():
        widget.destroy()
    left_frame = tk.Frame(root, bg="darkblue", width=root.winfo_screenwidth() // 3)
    left_frame.pack(side="left", fill="y")
    right_frame = tk.Frame(root, bg="white")
    right_frame.pack(side="left", expand=True, fill="both")
    if file_path:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            dados = list(reader)
        cabecalhos = dados[0]
        tree = ttk.Treeview(right_frame, columns=cabecalhos, show="headings")
        for col in cabecalhos:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        for row in dados[1:]:
            tree.insert("", "end", values=row)
        tree.pack(padx=10, pady=10, fill="both", expand=True)
        scroll_y = tk.Scrollbar(right_frame, orient="vertical", command=tree.yview)
        scroll_y.pack(side="right", fill="y")
        tree.config(yscrollcommand=scroll_y.set)
        scroll_x = tk.Scrollbar(right_frame, orient="horizontal", command=tree.xview)
        scroll_x.pack(side="bottom", fill="x")
        tree.config(xscrollcommand=scroll_x.set)
    buttons_frame = tk.Frame(left_frame, bg="darkblue")
    buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
    criar_botoes(buttons_frame)  # Chamada com apenas 'buttons_frame'
             
def show_grafico_pizza():
    global file_path, contexto, root
    if not file_path:
        messagebox.showerror("Erro", "Nenhum arquivo CSV selecionado.")
        return
    # Limpa todos os widgets existentes na janela principal
    for widget in root.winfo_children():
        widget.destroy()
    # Frame Esquerdo (Botões)
    left_frame = tk.Frame(root, bg="darkblue", width=root.winfo_screenwidth() // 3)
    left_frame.pack(side="left", fill="y")
    # Frame Direito (Interação e Gráfico)
    right_frame = tk.Frame(root, bg="white")
    right_frame.pack(side="right", expand=True, fill="both")
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao ler o arquivo CSV: {e}")
        return
    # Frame para entradas
    entradas_frame = tk.Frame(right_frame, bg="white")
    entradas_frame.pack(pady=20, padx=20, fill="x")
    tk.Label(entradas_frame, text="Nome da Coluna:", font=("Helvetica", 12), bg="white").pack(pady=5)
    coluna_entry = tk.Entry(entradas_frame, font=("Helvetica", 12))
    coluna_entry.pack(pady=5, fill="x")
    # Rótulo de status para mensagens
    status_label = tk.Label(right_frame, text="", font=("Helvetica", 12), bg="white", fg="green")
    status_label.pack(pady=5)
    def gerar_grafico_pizza():
        coluna = coluna_entry.get().strip()
        if coluna not in df.columns:
            status_label.config(text="Coluna não encontrada no arquivo CSV.", fg="red")
            return
        try:
            if contexto == "qualitativa" or contexto == "atividade_IIIA":
                tabela = qualitativa(df, coluna)
                labels = tabela['Categoria']
                sizes = tabela['Freq. Absoluta']
                autopct_format = '%1.1f%%'
            elif contexto == "quantitativa_continua" or contexto == "atividade_IIIC":
                tabela = quantitativa_continua(df, coluna)
                labels = tabela['Classes']
                sizes = tabela['Freq. Absoluta']
                autopct_format = '%1.1f%%'
            elif contexto == "quantitativa_discreta" or contexto == "atividade_IIIB":
                tabela = quantitativa_discreta(df, coluna)
                labels = tabela['Values']
                sizes = tabela['Freq. Absoluta']
                autopct_format = '%1.1f%%'
            else:
                status_label.config(text=f"Contexto '{contexto}' não suportado.", fg="red")
                return
            cmap = plt.get_cmap("rainbow")
            cores = cmap(np.linspace(0, 1, len(sizes)))
            plt.figure(figsize=(7, 7))
            patches, texts, autotexts = plt.pie(
                sizes,
                labels=labels,
                autopct=autopct_format,
                startangle=90,
                colors=cores,
                textprops={'fontsize': 8},
                pctdistance=0.85  # Define a distância das porcentagens em relação ao centro
            )
            # Ajusta as porcentagens para melhor legibilidade
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(10)
            plt.title('Gráfico Circular')
            plt.axis('equal')  # Mantém o círculo
            plt.savefig("grafico_pizza_temp.png")
            plt.close()
            # Remove widgets de interação
            entradas_frame.destroy()
            # Frame para exibir o gráfico com Canvas e Scrollbar Vertical
            grafico_frame = tk.Frame(right_frame, bg="white")
            grafico_frame.pack(fill="both", expand=True, padx=20, pady=20)
            # Canvas para o gráfico
            canvas = tk.Canvas(grafico_frame, bg="white")
            canvas.pack(side="left", fill="both", expand=True)
            # Scrollbar Vertical
            scrollbar_v = ttk.Scrollbar(grafico_frame, orient="vertical", command=canvas.yview)
            scrollbar_v.pack(side="right", fill="y")
            canvas.configure(yscrollcommand=scrollbar_v.set)
            # Frame interno dentro do Canvas
            inner_frame = tk.Frame(canvas, bg="white")
            canvas.create_window((0, 0), window=inner_frame, anchor="nw")
            # Carrega a imagem do gráfico
            try:
                image = Image.open("grafico_pizza_temp.png")
                photo = ImageTk.PhotoImage(image)
                imagem_label = tk.Label(inner_frame, image=photo, bg="white")
                imagem_label.image = photo  # Mantém uma referência
                imagem_label.pack(padx=20, pady=20)
            except Exception as img_e:
                messagebox.showerror("Erro", f"Erro ao exibir a imagem do gráfico: {img_e}")
                return
            # Atualiza a região de rolagem para o tamanho do conteúdo
            inner_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Atualiza o status
            status_label.config(text="Gráfico gerado com sucesso!", fg="green")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar o gráfico: {e}")
    btn_gerar_pizza = tk.Button(
        entradas_frame, 
        text="Mostrar Gráfico de Pizza", 
        command=gerar_grafico_pizza, 
        bg="blue", 
        fg="white", 
        font=("Helvetica", 12)
    )
    btn_gerar_pizza.pack(pady=20, fill="x")
    # Frame para Botões Esquerdo
    buttons_frame = tk.Frame(left_frame, bg="darkblue")
    buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
    # Criação dos Botões
    if 'criar_botoes' in globals():
        criar_botoes(buttons_frame)
    else:
        print("A função 'criar_botoes' não está definida.")
def show_grafico_linhas():
    global file_path
    for widget in root.winfo_children():
        widget.destroy()
    left_frame = tk.Frame(root, bg="darkblue", width=root.winfo_screenwidth() // 3)
    left_frame.pack(side="left", fill="y")
    right_frame = tk.Frame(root, bg="white")
    right_frame.pack(side="left", expand=True, fill="both")
    entradas_frame = tk.Frame(right_frame, bg="white")
    entradas_frame.pack(pady=20, padx=20, fill="x")
    tk.Label(
        entradas_frame, 
        text="Nomes das Colunas (separados por vírgula):", 
        font=("Helvetica", 12), 
        bg="white"
    ).pack(pady=5)
    colunas_entry = tk.Entry(entradas_frame, font=("Helvetica", 12))
    colunas_entry.pack(pady=5, fill="x")
    tk.Label(
        entradas_frame, 
        text="Nome do Eixo X:", 
        font=("Helvetica", 12), 
        bg="white"
    ).pack(pady=5)
    eixo_x_entry = tk.Entry(entradas_frame, font=("Helvetica", 12))
    eixo_x_entry.pack(pady=5, fill="x")
    tk.Label(
        entradas_frame, 
        text="Nome do Eixo Y:", 
        font=("Helvetica", 12), 
        bg="white"
    ).pack(pady=5)
    eixo_y_entry = tk.Entry(entradas_frame, font=("Helvetica", 12))
    eixo_y_entry.pack(pady=5, fill="x")
    mensagem_erro = tk.Label(
        entradas_frame, 
        text="", 
        font=("Helvetica", 10), 
        fg="red", 
        bg="white"
    )
    mensagem_erro.pack(pady=5)
    def gerar_grafico():
        mensagem_erro.config(text="")
        if not file_path:
            mensagem_erro.config(text="Nenhum arquivo CSV selecionado.")
            return
        colunas = [col.strip() for col in colunas_entry.get().split(',')]
        eixo_x = eixo_x_entry.get().strip()
        eixo_y = eixo_y_entry.get().strip()
        if len(colunas) != 2:
            mensagem_erro.config(text="Por favor, insira exatamente duas colunas separadas por vírgula.")
            return
        col1, col2 = colunas
        try:
            df = pd.read_csv(file_path)
            tabela1 = quantitativa_continua(df, col1)
            tabela2 = quantitativa_continua(df, col2)
        except Exception as e:
            mensagem_erro.config(text=f"Erro ao processar as colunas: {e}")
            return
        try:
            
            tabela1[['Inicio', 'Fim']] = tabela1['Classes'].str.split(r"\s*\|\s*--\s*", expand=True).astype(float)
            tabela2[['Inicio', 'Fim']] = tabela2['Classes'].str.split(r"\s*\|\s*--\s*", expand=True).astype(float)
            tabela1['Ponto_Medio'] = (tabela1['Inicio'] + tabela1['Fim']) / 2
            tabela2['Ponto_Medio'] = (tabela2['Inicio'] + tabela2['Fim']) / 2
            plt.figure(figsize=(10, 6))
            plt.plot(tabela1['Ponto_Medio'], tabela1['Freq. Absoluta'], marker='o', label=col1)
            plt.plot(tabela2['Ponto_Medio'], tabela2['Freq. Absoluta'], marker='s', label=col2)
            plt.title('Gráfico de Linhas Cruzadas')
            plt.xlabel(eixo_x if eixo_x else 'Classes')
            plt.ylabel(eixo_y if eixo_y else 'Frequência Absoluta')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig("grafico_temp.png")
            plt.close()
            for widget in right_frame.winfo_children():
                widget.destroy()
            grafico_frame = tk.Frame(right_frame, bg="white")
            grafico_frame.pack(fill="both", expand=True, padx=20, pady=20)
            canvas = tk.Canvas(grafico_frame, bg="white")
            canvas.pack(side="top", fill="both", expand=True)
            scrollbar_x = tk.Scrollbar(grafico_frame, orient="horizontal", command=canvas.xview)
            scrollbar_x.pack(side="bottom", fill="x")
            canvas.configure(xscrollcommand=scrollbar_x.set)
            inner_frame = tk.Frame(canvas, bg="white")
            canvas.create_window((0,0), window=inner_frame, anchor="nw")
            try:
                imagem = tk.PhotoImage(file="grafico_temp.png")
                imagem_label = tk.Label(inner_frame, image=imagem, bg="white")
                imagem_label.image = imagem  # Mantém uma referência
                imagem_label.pack(padx=20, pady=20)
            except Exception as img_e:
                tk.Label(
                    inner_frame, 
                    text=f"Erro ao exibir a imagem do gráfico: {img_e}", 
                    fg="red", 
                    bg="white"
                ).pack(pady=10)
                return
            inner_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
        except Exception as e:
            mensagem_erro.config(text=f"Erro ao gerar o gráfico: {e}")
    btn_gerar = create_formatted_button(
        entradas_frame, 
        "Mostrar Gráfico de Linhas Cruzadas", 
        gerar_grafico
    )
    btn_gerar.pack(pady=20, fill="x")
    # Frame para os botões no left_frame
    buttons_frame = tk.Frame(left_frame, bg="darkblue")
    buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
    # Cria os botões usando a função criar_botoes
    criar_botoes(buttons_frame)
def show_quantitativa_discreta():
    global contexto, file_path
    if not file_path:
        messagebox.showerror("Erro", "Nenhum arquivo CSV selecionado.")
        return
    for widget in root.winfo_children():
        widget.destroy()
    # Frame Esquerdo (Botões)
    left_frame = tk.Frame(root, bg="darkblue", width=root.winfo_screenwidth() // 3)
    left_frame.pack(side="left", fill="y")
    # Frame Direito (Interação e Tabela)
    right_frame = tk.Frame(root, bg="white")
    right_frame.pack(side="right", expand=True, fill="both")
    # Carrega o DataFrame
    df = pd.read_csv(file_path)
    # Entry para Nome da Coluna
    coluna_entry = tk.Entry(right_frame, font=("Helvetica", 12))
    success_label = tk.Label(right_frame, text="", font=("Helvetica", 12), bg="white")
    def analisar_coluna():
        coluna = coluna_entry.get()
        if coluna not in df.columns:
            success_label.config(text="Coluna não encontrada no arquivo CSV", fg="red")
            return
        df_coluna = df[coluna].dropna()
        if not pd.api.types.is_numeric_dtype(df_coluna):
            success_label.config(text="A coluna selecionada não é numérica", fg="red")
            return
        # Chama a função quantitativa_discreta
        tabela = quantitativa_discreta(df, coluna)
        # Remove widgets anteriores no right_frame
        for widget in right_frame.winfo_children():
            widget.destroy()
        # Exibe o título novamente
        titulo_label = tk.Label(
            right_frame,
            text=f"Título do arquivo: {os.path.basename(file_path)}",
            font=("Helvetica", 16, "bold"),
            bg="white"
        )
        titulo_label.pack(pady=10)
        # Criação do Treeview
        tree = ttk.Treeview(right_frame, columns=list(tabela.columns), show='headings')
        # Definição das Colunas
        for col in tabela.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=150)
        # Inserção dos Dados
        for index, row in tabela.iterrows():
            tree.insert("", "end", values=list(row))
        # Adiciona o Treeview ao frame
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        # Configuração das Scrollbars
        scrollbar_y = ttk.Scrollbar(right_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x = ttk.Scrollbar(right_frame, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side="bottom", fill="x")
        success_label.config(text="Análise concluída com sucesso!", fg="green")
        success_label.pack(pady=10)
    # Título do Arquivo
    titulo_label = tk.Label(
        right_frame,
        text=f"Título do arquivo: {os.path.basename(file_path)}",
        font=("Helvetica", 16, "bold"),
        bg="white"
    )
    titulo_label.pack(pady=10)
    # Label e Entry para Nome da Coluna
    tk.Label(right_frame, text="Nome da coluna:", font=("Helvetica", 12), bg="white").pack(pady=5)
    coluna_entry.pack(pady=5)
    # Botão para Analisar
    btn_analisar = create_formatted_buttonIII(right_frame, "Mostrar Tabela", analisar_coluna)
    btn_analisar.pack(pady=10)
    # Label de Sucesso ou Erro
    success_label.pack(pady=5)
    # Frame para Botões Esquerdo
    buttons_frame = tk.Frame(left_frame, bg="darkblue")
    buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
    # Criação dos Botões
    criar_botoes(buttons_frame)
def show_qualitativa():
    global contexto, file_path
    if not file_path:
        messagebox.showerror("Erro", "Nenhum arquivo CSV selecionado.")
        return
    for widget in root.winfo_children():
        widget.destroy()
    left_frame = tk.Frame(root, bg="darkblue", width=root.winfo_screenwidth() // 3)
    left_frame.pack(side="left", fill="y")
    right_frame = tk.Frame(root, bg="white")
    right_frame.pack(side="right", expand=True, fill="both")
    df = pd.read_csv(file_path)
    coluna_entry = tk.Entry(right_frame, font=("Helvetica", 12))
    success_label = tk.Label(right_frame, text="", font=("Helvetica", 12), bg="white")
    def analisar_coluna():
        coluna = coluna_entry.get()
        if coluna not in df.columns:
            success_label.config(text="Coluna não encontrada no arquivo CSV", fg="red")
            return
        df_coluna = df[coluna].dropna()
        if pd.api.types.is_numeric_dtype(df_coluna):
            df_coluna = df_coluna.astype(str)
        tabela = qualitativa(df, coluna)
        for widget in right_frame.winfo_children():
            widget.destroy()
        tree = ttk.Treeview(right_frame, columns=list(tabela.columns), show='headings')
        for col in tabela.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=120)
        for index, row in tabela.iterrows():
            tree.insert("", "end", values=list(row))
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        scrollbar_y = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x = ttk.Scrollbar(tree, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side="bottom", fill="x")
        success_label.config(text="Análise concluída com sucesso!", fg="green")
        success_label.pack(pady=10)
    titulo_label = tk.Label(
        right_frame,
        text=f"Título do arquivo: {os.path.basename(file_path)}",
        font=("Helvetica", 16, "bold"),
        bg="white"
    )
    titulo_label.pack(pady=10)
    tk.Label(right_frame, text="Nome da coluna:", font=("Helvetica", 12), bg="white").pack(pady=5)
    coluna_entry.pack(pady=5)
    btn_analisar = create_formatted_buttonIII(right_frame, "Mostrar Tabela", analisar_coluna)
    btn_analisar.pack(pady=10)
    success_label.pack(pady=5)
    buttons_frame = tk.Frame(left_frame, bg="darkblue")
    buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
    criar_botoes(buttons_frame)     
def show_grafico_barras(): 
    global contexto, file_path, root
    if not file_path:
        messagebox.showerror("Erro", "Nenhum arquivo CSV selecionado.")
        return
    # Limpa todos os widgets existentes na janela principal
    for widget in root.winfo_children():
        widget.destroy()
    # Frame Esquerdo (Botões)
    left_frame = tk.Frame(root, bg="darkblue", width=root.winfo_screenwidth() // 3)
    left_frame.pack(side="left", fill="y")
    # Frame Direito (Interação e Gráfico)
    right_frame = tk.Frame(root, bg="white")
    right_frame.pack(side="right", expand=True, fill="both")
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao ler o arquivo CSV: {e}")
        return
    # Frame para entradas
    entradas_frame = tk.Frame(right_frame, bg="white")
    entradas_frame.pack(pady=20, padx=20, fill="x")
    tk.Label(entradas_frame, text="Nome da Coluna:", font=("Helvetica", 12), bg="white").pack(pady=5)
    coluna_entry = tk.Entry(entradas_frame, font=("Helvetica", 12))
    coluna_entry.pack(pady=5, fill="x")
    tk.Label(entradas_frame, text="Nome do Eixo X:", font=("Helvetica", 12), bg="white").pack(pady=5)
    eixo_x_entry = tk.Entry(entradas_frame, font=("Helvetica", 12))
    eixo_x_entry.pack(pady=5, fill="x")
    tk.Label(entradas_frame, text="Nome do Eixo Y:", font=("Helvetica", 12), bg="white").pack(pady=5)
    eixo_y_entry = tk.Entry(entradas_frame, font=("Helvetica", 12))
    eixo_y_entry.pack(pady=5, fill="x")
    # Rótulo de status para mensagens
    success_label = tk.Label(right_frame, text="", font=("Helvetica", 12), bg="white", fg="green")
    success_label.pack(pady=5)
    def gerar_grafico():
        coluna = coluna_entry.get().strip()
        eixo_x = eixo_x_entry.get().strip()
        eixo_y = eixo_y_entry.get().strip()
        if coluna not in df.columns:
            success_label.config(text="Coluna não encontrada no arquivo CSV.", fg="red")
            return
        try:
            df_coluna = df[coluna].dropna()
            # Mapeia 0 para 'n' e 1 para 's' se for qualitativa
            if contexto == "qualitativa" or contexto == "atividade_IIIA":
                df_coluna = df_coluna.replace({0: 'n', 1: 's'}).astype(str)
            # Gera a tabela de frequência
            if contexto == "qualitativa" or contexto == "atividade_IIIA" or contexto == "atividade_II":
                tabela = qualitativa(df_coluna.to_frame(), coluna)
                plt.figure(figsize=(10, 6))
                plt.bar(tabela['Categoria'], tabela['Freq. Absoluta'], color='lightgreen')
                plt.xlabel(eixo_x if eixo_x else 'Categorias')
                plt.ylabel(eixo_y if eixo_y else 'Frequência Absoluta')
                plt.title(f'Gráfico de Barras - {coluna}')
            elif contexto in ["quantitativa_continua", "quantitativa_discreta", "atividade_IIIB", "atividade_IIIC"]:
                tabela = quantitativa_discreta(df, coluna) if contexto == "quantitativa_discreta" or contexto == "atividade_IIIB" else quantitativa_continua(df, coluna)
                plt.bar(tabela.iloc[:,0], tabela['Freq. Absoluta'], color='skyblue')
                plt.xlabel(eixo_x if eixo_x else 'Classes' if contexto == "quantitativa_continua" or contexto == "atividade_IIIC" else 'Values')
                plt.ylabel(eixo_y if eixo_y else 'Frequência Absoluta')
                plt.title(f'Gráfico de Barras - {coluna}')
            else:
                success_label.config(text=f"Contexto '{contexto}' não suportado.", fg="red")
                return
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            # Salva o gráfico como imagem temporária
            plt.savefig("grafico_barras_temp.png")
            plt.close()
        except Exception as e:
            success_label.config(text="Erro ao gerar o gráfico.", fg="red")
            return
        try:
            # Remove widgets de interação, mas mantém o success_label
            for widget in right_frame.winfo_children():
                if widget != success_label:
                    widget.destroy()
            # Frame para exibir o gráfico com barras de rolagem
            grafico_frame = tk.Frame(right_frame, bg="white")
            grafico_frame.pack(fill="both", expand=True, padx=20, pady=20)
            # Canvas para o gráfico
            canvas = tk.Canvas(grafico_frame, bg="white")
            canvas.pack(side="left", fill="both", expand=True)
            # Barras de rolagem
            scrollbar_v = ttk.Scrollbar(grafico_frame, orient="vertical", command=canvas.yview)
            scrollbar_v.pack(side="right", fill="y")
            scrollbar_h = ttk.Scrollbar(grafico_frame, orient="horizontal", command=canvas.xview)
            scrollbar_h.pack(side="bottom", fill="x")
            canvas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
            # Frame dentro do Canvas
            inner_frame = tk.Frame(canvas, bg="white")
            canvas.create_window((0,0), window=inner_frame, anchor="nw")
            # Carrega a imagem do gráfico
            try:
                image = Image.open("grafico_barras_temp.png")
                photo = ImageTk.PhotoImage(image)
                imagem_label = tk.Label(inner_frame, image=photo, bg="white")
                imagem_label.image = photo  # Mantém uma referência
                imagem_label.pack(padx=20, pady=20)
            except Exception as img_e:
                success_label.config(text="Erro ao exibir o gráfico.", fg="red")
                return
            # Atualiza a região de rolagem para o tamanho do conteúdo
            inner_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            success_label.config(text="Gráfico gerado com sucesso!", fg="green")
        except Exception as img_e:
            success_label.config(text="Erro ao exibir o gráfico.", fg="red")
            return
    # Botão para gerar o gráfico
    btn_gerar = tk.Button(
        entradas_frame, 
        text="Mostrar Gráfico de Barras", 
        command=gerar_grafico, 
        bg="blue", 
        fg="white", 
        font=("Helvetica", 12)
    )
    btn_gerar.pack(pady=10, fill="x")
    # Label de Sucesso ou Erro
    success_label.pack(pady=5)
    # Frame para Botões Esquerdo
    buttons_frame = tk.Frame(left_frame, bg="darkblue")
    buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
    # Criação dos Botões
    if 'criar_botoes' in globals():
        criar_botoes(buttons_frame)
    else:
        print("A função 'criar_botoes' não está definida.") 
def show_bloxplot(): 
    global contexto, file_path, root
    if not file_path:
        messagebox.showerror("Erro", "Nenhum arquivo CSV selecionado.")
        return
    # Limpa todos os widgets existentes na janela principal
    for widget in root.winfo_children():
        widget.destroy()
    # Frame Esquerdo (Botões)
    left_frame = tk.Frame(root, bg="darkblue", width=root.winfo_screenwidth() // 3)
    left_frame.pack(side="left", fill="y")
    # Frame Direito (Interação e Gráfico)
    right_frame = tk.Frame(root, bg="white")
    right_frame.pack(side="right", expand=True, fill="both")
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao ler o arquivo CSV: {e}")
        return
    # Frame para entradas
    entradas_frame = tk.Frame(right_frame, bg="white")
    entradas_frame.pack(pady=20, padx=20, fill="x")
    tk.Label(entradas_frame, text="Nome da Coluna:", font=("Helvetica", 12), bg="white").pack(pady=5)
    coluna_entry = tk.Entry(entradas_frame, font=("Helvetica", 12))
    coluna_entry.pack(pady=5, fill="x")
    # Rótulo de status para mensagens
    success_label = tk.Label(right_frame, text="", font=("Helvetica", 12), bg="white", fg="green")
    success_label.pack(pady=5)
    def gerar_boxplot():
        coluna = coluna_entry.get().strip()
        if coluna not in df.columns:
            success_label.config(text="Coluna não encontrada no arquivo CSV.", fg="red")
            return
        try:
            df_renomeado = df.rename(columns={coluna: "Valor"})
            q1 = df_renomeado["Valor"].quantile(0.25)
            q3 = df_renomeado["Valor"].quantile(0.75)
            iqr = q3 - q1
            limite_inferior = q1 - 1.5 * iqr
            limite_superior = q3 + 1.5 * iqr
            if limite_inferior <= 0:
                limite_inferior = 0
            plt.figure(figsize=(8, 6))
            sns.boxplot(y="Valor", data=df_renomeado, showfliers=False)  # Remove outliers
            plt.axhline(limite_inferior, color="red", linestyle="--", label=f"Limite Inferior ({limite_inferior:.2f})")
            plt.axhline(limite_superior, color="blue", linestyle="--", label=f"Limite Superior ({limite_superior:.2f})")
            plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=1)
            plt.title(f"Boxplot para {coluna}")
            plt.tight_layout()
            plt.savefig("boxplot_temp.png")
            plt.close()
        except Exception as e:
            success_label.config(text="Erro ao gerar o boxplot.", fg="red")
            return
        try:
            # Remove widgets de interação, mas mantém o success_label
            for widget in right_frame.winfo_children():
                if widget != success_label:
                    widget.destroy()
            # Frame para exibir o gráfico com barras de rolagem
            grafico_frame = tk.Frame(right_frame, bg="white")
            grafico_frame.pack(fill="both", expand=True, padx=20, pady=20)
            # Canvas para o gráfico
            canvas = tk.Canvas(grafico_frame, bg="white")
            canvas.pack(side="left", fill="both", expand=True)
            # Barras de rolagem
            scrollbar_v = ttk.Scrollbar(grafico_frame, orient="vertical", command=canvas.yview)
            scrollbar_v.pack(side="right", fill="y")
            scrollbar_h = ttk.Scrollbar(grafico_frame, orient="horizontal", command=canvas.xview)
            scrollbar_h.pack(side="bottom", fill="x")
            canvas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
            # Frame dentro do Canvas
            inner_frame = tk.Frame(canvas, bg="white")
            canvas.create_window((0,0), window=inner_frame, anchor="nw")
            # Carrega a imagem do gráfico
            try:
                image = Image.open("boxplot_temp.png")
                photo = ImageTk.PhotoImage(image)
                imagem_label = tk.Label(inner_frame, image=photo, bg="white")
                imagem_label.image = photo  # Mantém uma referência
                imagem_label.pack(padx=20, pady=20)
            except Exception as img_e:
                success_label.config(text="Erro ao exibir o boxplot.", fg="red")
                return
            # Atualiza a região de rolagem para o tamanho do conteúdo
            inner_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            success_label.config(text="Boxplot gerado com sucesso!", fg="green")
        except Exception as img_e:
            success_label.config(text="Erro ao exibir o boxplot.", fg="red")
            return
    btn_gerar = tk.Button(
        entradas_frame, 
        text="Mostrar Boxplot", 
        command=gerar_boxplot, 
        bg="blue", 
        fg="white", 
        font=("Helvetica", 12)
    )
    btn_gerar.pack(pady=10, fill="x")
    success_label.pack(pady=5)
    buttons_frame = tk.Frame(left_frame, bg="darkblue")
    buttons_frame.place(relx=0.5, rely=0.5, anchor="center")

    criar_botoes(buttons_frame)
    
def atvII_arquivoI():
    global file_path
    file_path = 'Oysters.csv'
def atvIIIA_arquivoI():
    global file_path
    file_path = 'amostra_backpak.csv'
def atvIIIB_arquivoI():
    global file_path
    file_path = "amostra_fertility.csv"
def atvIIIC_arquivoI():
    global file_path
    file_path = "amostra_Forbes2000.csv"


root = tk.Tk()
root.attributes('-fullscreen', True)
show_initial_screen()
root.mainloop()