import customtkinter as ctk
from tkinter import ttk, messagebox

from customtkinter import set_appearance_mode, set_default_color_theme
from tkcalendar import Calendar
import mysql.connector
from datetime import datetime, timedelta

# Conexão com o banco de dados
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="x5"
)
cursor = conn.cursor()

set_appearance_mode("dark")
set_default_color_theme("dark-blue")

# Funções auxiliares
def dias_uteis(data_inicio, dias):
    count = 0
    while count < dias:
        data_inicio += timedelta(days=1)
        if data_inicio.weekday() < 5:
            count += 1
    return data_inicio


def verificar_disponibilidade(id_laboratorio, data_reserva, hora_inicio):
    query = """
    SELECT data_reserva FROM Reservas 
    WHERE id_laboratorio = %s AND data_reserva = %s AND hora_inicio = %s AND status = 'confirmada'
    """
    cursor.execute(query, (id_laboratorio, data_reserva, hora_inicio))
    if cursor.fetchone():
        return False, None

    query = """
    SELECT MAX(data_reserva) FROM Reservas 
    WHERE id_laboratorio = %s AND status = 'confirmada'
    """
    cursor.execute(query, (id_laboratorio,))
    ultimo_agendamento = cursor.fetchone()[0]

    if ultimo_agendamento:
        proximo_dia_disponivel = dias_uteis(ultimo_agendamento, 15)
        if datetime.strptime(data_reserva, '%Y-%m-%d').date() <= proximo_dia_disponivel:
            return False, proximo_dia_disponivel

    return True, None


def cadastrar_usuario():
    nome = nome_entry.get()
    email = email_entry.get()
    senha = senha_entry.get()
    tipo = tipo_combobox.get()
    usuario_name = usuario_name_entry.get()

    if not nome or not email or not senha or not tipo or not usuario_name:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
        return

    query = """
    INSERT INTO Usuarios (nome, email, senha, tipo, usuario_name) 
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (nome, email, senha, tipo, usuario_name))
        conn.commit()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso.")
        cadastro_window.destroy()
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {err}")


def tela_cadastro_usuario():
    global nome_entry, email_entry, senha_entry, tipo_combobox, usuario_name_entry, cadastro_window

    root.iconify()

    cadastro_window = ctk.CTkToplevel(root)
    cadastro_window.title("Cadastro de Usuário")

    cadastro_window.geometry("500x430")
    cadastro_window.resizable(False, False)

    ctk.CTkLabel(cadastro_window, text="Nome:").pack(padx=(0, 100), pady=(20, 0))
    nome_entry = ctk.CTkEntry(cadastro_window)
    nome_entry.pack(pady=(1, 0))

    ctk.CTkLabel(cadastro_window, text="Email:").pack(padx=(0, 105), pady=(10, 0))
    email_entry = ctk.CTkEntry(cadastro_window)
    email_entry.pack(pady=(1, 0))

    ctk.CTkLabel(cadastro_window, text="Senha:").pack(padx=(0, 100), pady=(10, 0))
    senha_entry = ctk.CTkEntry(cadastro_window, show="*")
    senha_entry.pack(pady=(1, 0))

    ctk.CTkLabel(cadastro_window, text="Tipo:").pack(padx=(0, 110), pady=(10, 0))
    tipo_combobox = ctk.CTkComboBox(cadastro_window, values=["admin", "usuario"])
    tipo_combobox.pack(pady=(1, 0))

    ctk.CTkLabel(cadastro_window, text="Nome de Usuário:").pack(padx=(0, 40), pady=(10, 0))
    usuario_name_entry = ctk.CTkEntry(cadastro_window)
    usuario_name_entry.pack(pady=(1, 0))

    ctk.CTkButton(cadastro_window, text="Cadastrar", font=("", 13, "bold"), command=cadastrar_usuario).pack(
        pady=(18, 0))


def login():
    usuario_name = username_entry.get()
    senha = password_entry.get()

    query = "SELECT id_usuario, tipo FROM Usuarios WHERE usuario_name = %s AND senha = %s"
    cursor.execute(query, (usuario_name, senha))
    result = cursor.fetchone()

    if result:
        id_usuario, tipo_usuario = result
        root.iconify()
        if tipo_usuario == 'admin':
            tela_admin()  # Abre a tela de administração

        else:
            user_dashboard(id_usuario)  # Redireciona para a tela de agendamentos do usuário
    else:
        messagebox.showerror("Erro de Login", "Usuário ou senha incorretos.")


def agendar(id_usuario):
    data_reserva = cal.get_date()  # Isso retorna um objeto date
    if isinstance(data_reserva, str):
        data_reserva = datetime.strptime(data_reserva, '%d/%m/%Y').date()  # Verifica e converte se necessário

    data_reserva_str = data_reserva.strftime('%Y-%m-%d')  # Converte para string no formato YYYY-MM-DD
    id_laboratorio = id_laboratorio_combobox.get().split(" - ")[0]
    hora_inicio = hora_combobox.get()
    hora_fim = hora_fim_combobox.get()

    if not data_reserva or not hora_inicio or not hora_fim:
        messagebox.showwarning("Aviso", "Por favor, selecione uma data e hora.")
        return

    print(f"Data Reserva: {data_reserva_str}")

    # Verifica se a hora de fim é menor que a hora de início
    hora_inicio_dt = datetime.strptime(hora_inicio, '%H:%M')
    hora_fim_dt = datetime.strptime(hora_fim, '%H:%M')

    if hora_fim_dt <= hora_inicio_dt:
        messagebox.showwarning("Aviso", "A hora de término deve ser maior que a hora de início.")
        return

    # Verifica a disponibilidade do laboratório
    disponivel, proximo_dia_disponivel = verificar_disponibilidade(id_laboratorio, data_reserva_str, hora_inicio)
    if not disponivel:
        if proximo_dia_disponivel:
            messagebox.showwarning("Aviso",
                                   f"Este laboratório só poderá ser agendado novamente após {proximo_dia_disponivel.strftime('%d/%m/%Y')}.")
        else:
            messagebox.showwarning("Aviso", "Este horário já está reservado.")
        return

    query = """
    INSERT INTO Reservas (id_usuario, id_laboratorio, data_reserva, hora_inicio, hora_fim, status) 
    VALUES (%s, %s, %s, %s, %s, 'confirmada')
    """

    print(
        f"Inserindo reserva: id_usuario={id_usuario}, id_laboratorio={id_laboratorio}, data_reserva={data_reserva_str}, hora_inicio={hora_inicio}, hora_fim={hora_fim}")

    cursor.execute(query, (id_usuario, id_laboratorio, data_reserva_str, hora_inicio, hora_fim))
    conn.commit()

    messagebox.showinfo("Sucesso", "Reserva realizada com sucesso.")
    user_window.destroy()


def tela_agendamento_usuario(id_usuario):
    global cal, hora_combobox, hora_fim_combobox, user_window, id_laboratorio_combobox

    user_window = ctk.CTkToplevel(root)
    user_window.title("Agendar Laboratório")

    user_window.geometry("500x520")
    user_window.resizable(False, False)

    ctk.CTkLabel(user_window, text="Laboratório:").pack(pady=(20, 0))
    id_laboratorio_combobox = ctk.CTkComboBox(user_window, values=["1 - Laboratório A", "2 - Laboratório B"])
    id_laboratorio_combobox.pack(pady=(3, 10))

    ctk.CTkLabel(user_window, text="Data:").pack()
    cal = Calendar(user_window, date_pattern="dd/mm/yyyy", mindate=datetime.now())
    cal.pack(pady=(3, 10))

    ctk.CTkLabel(user_window, text="Hora Início:").pack()
    horarios = ["19:00", "19:30", "20:00", "20:30", "21:00"]
    hora_combobox = ctk.CTkComboBox(user_window, values=horarios)
    hora_combobox.pack(pady=(3, 10))

    ctk.CTkLabel(user_window, text="Hora Fim:").pack()
    horarios = ["19:00", "19:30", "20:00", "20:30", "21:00", "21:30"]
    hora_fim_combobox = ctk.CTkComboBox(user_window, values=horarios)
    hora_fim_combobox.pack(pady=(3, 10))

    ctk.CTkButton(user_window, text="Agendar", font=("", 13, "bold"), command=lambda: agendar(id_usuario)).pack()


def tela_admin():
    admin_window = ctk.CTkToplevel(root)
    admin_window.title("Administração de Agendamentos")

    root.iconify()
    # Estilo para Treeview
    style = ttk.Style()
    style.theme_use('clam')  # Usar o tema clam
    style.configure("Treeview",
                    background="#2E2E2E",  # Cor de fundo
                    foreground="white",  # Cor do texto
                    rowheight=25,
                    fieldbackground="#2E2E2E")  # Cor de fundo das células
    style.map("Treeview",
              background=[('selected', '#4A4A4A')],  # Cor de fundo quando selecionado
              foreground=[('selected', 'gray')])  # Cor do texto quando selecionado

    # Criar o Treeview
    tree = ttk.Treeview(admin_window,
                        columns=("ID", "Usuário", "Laboratório", "Data", "Hora Início", "Hora Fim", "Status"),
                        show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Usuário", text="Usuário")
    tree.heading("Laboratório", text="Laboratório")
    tree.heading("Data", text="Data")
    tree.heading("Hora Início", text="Hora Início")
    tree.heading("Hora Fim", text="Hora Fim")
    tree.heading("Status", text="Status")
    tree.pack(padx=30, pady=15, fill="x")

    # Definir o tamanho das colunas
    tree.column("ID", width=50)
    tree.column("Usuário", width=100)
    tree.column("Laboratório", width=150)
    tree.column("Data", width=80)
    tree.column("Hora Início", width=80)
    tree.column("Hora Fim", width=80)
    tree.column("Status", width=100)

    # Consultar dados
    query = """
    SELECT r.id_reserva, u.nome, l.nome, 
           DATE_FORMAT(r.data_reserva, '%d/%m/%Y') AS data_reserva, 
           r.hora_inicio, r.hora_fim, r.status
    FROM Reservas r
    JOIN Usuarios u ON r.id_usuario = u.id_usuario
    JOIN Laboratorio l ON r.id_laboratorio = l.id_laboratorio
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            print("Nenhum dado encontrado.")
        for row in rows:
            if None in row:
                print(f"Row com valor nulo: {row}")
            else:
                tree.insert("", "end", values=row)
    except mysql.connector.Error as err:
        print(f"Erro ao executar a consulta: {err}")

    # Função para excluir um agendamento
    def excluir_agendamento():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um agendamento para excluir.")
            return

        id_reserva = tree.item(selected_item)['values'][0]  # Obter ID da reserva selecionada
        confirmar = messagebox.askyesno("Confirmação", f"Deseja realmente excluir o agendamento ID {id_reserva}?")

        if confirmar:
            query = "DELETE FROM Reservas WHERE id_reserva = %s"
            try:
                cursor.execute(query, (id_reserva,))
                conn.commit()
                messagebox.showinfo("Sucesso", "Agendamento excluído com sucesso.")
                tree.delete(selected_item)  # Remover agendamento da árvore
            except mysql.connector.Error as err:
                messagebox.showerror("Erro", f"Erro ao excluir agendamento: {err}")

    # Botão para excluir agendamento
    ctk.CTkButton(admin_window, text="Excluir Agendamento", command=excluir_agendamento).pack(pady=10)


def user_dashboard(id_usuario):
    user_window = ctk.CTkToplevel(root)
    user_window.title("Área do Usuário")

    root.iconify()

    user_window.geometry("500x300")
    user_window.resizable(False, False)

    ctk.CTkLabel(user_window, text="Bem-vindo!").pack(pady=(35, 10))

    ctk.CTkButton(user_window, text="Agendar Laboratório", font=("", 14, "bold"), border_spacing=10,
                  command=lambda: tela_agendamento_usuario(id_usuario)).pack(pady=10)
    ctk.CTkButton(user_window, text="Agendamentos do Usuário", font=("", 14, "bold"), border_spacing=10,
                  command=lambda: ver_agendamentos_usuario(id_usuario)).pack(pady=10)
    ctk.CTkButton(user_window, text="Sair", font=("", 14, "bold"), border_spacing=10, command=user_window.destroy).pack(
        pady=10)


def ver_agendamentos_usuario(id_usuario):
    agendamentos_window = ctk.CTkToplevel(root)
    agendamentos_window.title("Meus Agendamentos")

    root.iconify()

    # Estilo para Treeview
    style = ttk.Style()
    style.theme_use('clam')  # Usar o tema clam
    style.configure("Treeview",
                    background="#2E2E2E",  # Cor de fundo
                    foreground="white",  # Cor do texto
                    rowheight=25,
                    fieldbackground="#2E2E2E")  # Cor de fundo das células
    style.map("Treeview",
              background=[('selected', '#4A4A4A')],  # Cor de fundo quando selecionado
              foreground=[('selected', 'gray')])  # Cor do texto quando selecionado

    tree = ttk.Treeview(agendamentos_window,
                        columns=("Laboratório", "Data", "Hora Início", "Hora Fim", "Status"),
                        show="headings")

    tree.heading("Laboratório", text="Laboratório")
    tree.heading("Data", text="Data")
    tree.heading("Hora Início", text="Hora Início")
    tree.heading("Hora Fim", text="Hora Fim")
    tree.heading("Status", text="Status")
    tree.pack(padx=30, pady=15, fill="x")

    # Definir o tamanho das colunas
    tree.column("Laboratório", width=100)
    tree.column("Data", width=100)
    tree.column("Hora Início", width=80)
    tree.column("Hora Fim", width=80)
    tree.column("Status", width=100)

    def excluir_agendamento():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um agendamento para excluir.")
            return

        id_reserva = tree.item(selected_item)['values'][0]  # Obter ID da reserva selecionada
        confirmar = messagebox.askyesno("Confirmação", f"Deseja realmente excluir o agendamento ID {id_reserva}?")

        if confirmar:
            query = "DELETE FROM Reservas WHERE id_reserva = %s"
            try:
                cursor.execute(query, (id_reserva,))
                conn.commit()
                messagebox.showinfo("Sucesso", "Agendamento excluído com sucesso.")
                tree.delete(selected_item)  # Remover agendamento da árvore
            except mysql.connector.Error as err:
                messagebox.showerror("Erro", f"Erro ao excluir agendamento: {err}")

    # Botão para excluir agendamento
    ctk.CTkButton(agendamentos_window, text="Excluir Agendamento", command=excluir_agendamento).pack(pady=10)

    query = """
    SELECT l.nome, 
           DATE_FORMAT(r.data_reserva, '%d/%m/%Y') AS data_reserva,
           r.hora_inicio, r.hora_fim, r.status
    FROM Reservas r 
    JOIN Laboratorio l ON r.id_laboratorio = l.id_laboratorio
    WHERE r.id_usuario = %s
    """
    try:
        cursor.execute(query, (id_usuario,))
        rows = cursor.fetchall()
        if not rows:
            print("Nenhum agendamento encontrado para o usuário.")
        for row in rows:
            tree.insert("", "end", values=row)
    except mysql.connector.Error as err:
        print(f"Erro ao executar a consulta: {err}")


# Interface principal de login
root = ctk.CTk()
root.title("Login")
root.geometry("500x300")
root.resizable(False, False)

ctk.CTkLabel(root, text="Usuário:").pack(padx=(0, 90), pady=(20, 1))
username_entry = ctk.CTkEntry(root)
username_entry.pack(pady=(0, 10))

ctk.CTkLabel(root, text="Senha:").pack(padx=(0, 100), pady=(0, 1))
password_entry = ctk.CTkEntry(root, show="*")
password_entry.pack(pady=(0, 15))

ctk.CTkButton(root, text="Login", font=("", 13, "bold"), command=login).pack(pady=(0, 10))
ctk.CTkButton(root, text="Cadastrar Usuário", font=("", 13, "bold"), command=tela_cadastro_usuario).pack(pady=(15, 0))

root.mainloop()
