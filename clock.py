import tkinter as tk
import os
import json


# Relógio digital personalizável para Windows
# Requer as bibliotecas: tkinter, win32gui, win32con
# Este script cria um relógio digital que pode ser movido, personalizado e configurado
# para exibir hora, data e dia da semana. Ele também permite alterar a fonte, tamanho, cor e opacidade.
# Importante: Instale as bibliotecas necessárias com:

# Nota: me senti frustado apos terminar o projeto, pois ele não funcionou como esperado, python não é capaz de sobrepor full screen real de aplicativos sem
#colocar o app em windowed borderless, o que não é o que eu queria, então decidi deixar o projeto aqui para quem quiser tentar melhorar ou usar como base para algo mais.

#variáveis globais
current_bg_color = "black"
current_fg_color = "white"

CONFIG_FILE = "clock_config.json"

root = None
label = None

current_font_family = "Segoe UI"
current_font_size = 12
current_font_weight = "normal" 

current_display_format = "time_date"
current_24h_format = True  

current_opacity = 0.9  # padrão

# Função para definir a fonte do relógio
def apply_font():
    global current_font_family, current_font_size, current_font_weight
    label.config(font=(current_font_family, current_font_size, current_font_weight))

# Funções para alterar a fonte
def set_font_family(family):
    global current_font_family
    current_font_family = family
    apply_font()
    save_config()

# Função para alterar o tamanho da fonte
def set_font_size(size):
    global current_font_size
    current_font_size = size
    apply_font()
    save_config()

# Função para alternar entre negrito e normal
def toggle_bold():
    global current_font_weight
    current_font_weight = "bold" if current_font_weight == "normal" else "normal"
    apply_font()
    save_config()

# Função para atualizar o relógio
def update_time():
    import datetime
    now = datetime.datetime.now()

    if current_24h_format:
        hour_format = "%H:%M:%S"
    else:
        hour_format = "%I:%M:%S %p"

    if current_display_format == "time_only":
        display_text = now.strftime(hour_format)
    elif current_display_format == "time_date":
        display_text = now.strftime(f"{hour_format}\n%d/%m/%Y")
    elif current_display_format == "time_date_weekday":
        display_text = now.strftime(f"{hour_format}\n%A, %d/%m/%Y")
    else:
        display_text = now.strftime(hour_format)

    label.config(text=display_text)
    root.after(1000, update_time)

# Função para definir a posição do relógio na tela
def set_position(pos):
    global current_position
    current_position = pos

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width, height = 150, 60

    if pos == "top_left":
        x, y = 10, 10
    elif pos == "top_right":
        x, y = screen_width - width - 10, 10
    elif pos == "bottom_right":
        x, y = screen_width - width - 10, screen_height - height - 40
    elif pos == "bottom_left":
        x, y = 10, screen_height - height - 40
    else:
        x, y = 10, 10

    # Verificação para garantir que a janela não fique fora da tela
    if x + width > screen_width:
        x = screen_width - width - 10
    if y + height > screen_height:
        y = screen_height - height - 40

    root.geometry(f"{width}x{height}+{x}+{y}")
    save_config()


# Função para iniciar o movimento do relógio
def start_move(event):
    root.x = event.x
    root.y = event.y

# Função para mover o relógio
def do_move(event):
    x = event.x_root - root.x
    y = event.y_root - root.y

    # Animação suave para mover a janela
    def move_window():
        root.geometry(f"+{x}+{y}")
    
    root.after(10, move_window)

# Função para definir a cor do relógio
def set_color(bg, fg):
    global current_bg_color, current_fg_color
    current_bg_color = bg
    current_fg_color = fg
    root.configure(bg=bg)
    label.configure(bg=bg, fg=fg)
    save_config()

# Função para definir a opacidade do relógio
def set_opacity(value):
    global current_opacity
    current_opacity = value
    root.attributes("-alpha", current_opacity)
    save_config()

# Função para sair do aplicativo
def quit_app():
    if root:
        root.destroy()
    os._exit(0)

# Função para salvar a configuração do relógio
def save_config():
    config = {
        "bg_color": current_bg_color,
        "fg_color": current_fg_color,
        "font_family": current_font_family,
        "font_size": current_font_size,
        "font_weight": current_font_weight,
        "position": current_position,
        "display_format": current_display_format,
        "opacity": current_opacity,
        "use_24h": current_24h_format
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

# Função para carregar a configuração do relógio
def load_config():
    global current_bg_color, current_fg_color
    global current_font_family, current_font_size, current_font_weight
    global current_position
    global current_display_format, current_24h_format
    global current_opacity

    if not os.path.exists(CONFIG_FILE):
        # Defaults
        current_bg_color = "black"
        current_fg_color = "white"
        current_font_family = "Segoe UI"
        current_font_size = 12
        current_font_weight = "normal"
        current_position = "top_left"
        return

    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
        current_bg_color = config.get("bg_color", "black")
        current_fg_color = config.get("fg_color", "white")
        current_font_family = config.get("font_family", "Segoe UI")
        current_font_size = config.get("font_size", 12)
        current_font_weight = config.get("font_weight", "normal")
        current_position = config.get("position", "top_left")
        current_display_format = config.get("display_format", "time_date")
        current_24h_format = config.get("use_24h")
        current_opacity = config.get("opacity")

# Funções para alterar a posição, formato de exibição e 24h/12h
def set_display_format(fmt):
    global current_display_format
    current_display_format = fmt
    save_config()

# Função para alternar entre formato 24h e 12h
def toggle_24h_format():
    global current_24h_format
    current_24h_format = not current_24h_format
    save_config()

# Função para realçar a opção do menu selecionada
def highlight_menu_option(menu, label):
    menu.entryconfig(label, background="lightblue")

# Função para exibir o menu de contexto
def show_context_menu(event):
    menu = tk.Menu(root, tearoff=0)

    # Posições
    menu.add_command(label="Canto superior esquerdo", command=lambda: set_position("top_left"))
    menu.add_command(label="Canto superior direito", command=lambda: set_position("top_right"))
    menu.add_command(label="Canto inferior esquerdo", command=lambda: set_position("bottom_left"))
    menu.add_command(label="Canto inferior direito", command=lambda: set_position("bottom_right"))

    menu.add_separator()

    # Formato de exibição
    format_menu = tk.Menu(menu, tearoff=0)
    format_menu.add_command(label="Hora", command=lambda: set_display_format("time_only"))
    format_menu.add_command(label="Hora e data", command=lambda: set_display_format("time_date"))
    format_menu.add_command(label="Hora, data e dia da semana", command=lambda: set_display_format("time_date_weekday"))
    menu.add_cascade(label="Formato de exibição", menu=format_menu)

    # Alternar 24h / 12h
    menu.add_command(label="Alternar 24h / 12h", command=toggle_24h_format)

    menu.add_separator()

    # Cores
    color_menu = tk.Menu(menu, tearoff=0)
    color_menu.add_command(label="Preto (padrão)", command=lambda: set_color("black", "white"))
    color_menu.add_command(label="Branco", command=lambda: set_color("white", "black"))
    color_menu.add_command(label="Azul escuro", command=lambda: set_color("#001f3f", "white"))
    color_menu.add_command(label="Verde escuro", command=lambda: set_color("#004d00", "white"))
    menu.add_cascade(label="Cor do relógio", menu=color_menu)

    opacity_menu = tk.Menu(menu, tearoff=0)
    for val in [1.0, 0.9, 0.8, 0.7, 0.6, 0.5]:
        label_text = f"{int(val * 100)}%"
        opacity_menu.add_command(label=label_text, command=lambda v=val: set_opacity(v))
    menu.add_cascade(label="Transparência", menu=opacity_menu)

    menu.add_separator()

    # Fonte
    font_menu = tk.Menu(menu, tearoff=0)
    font_menu.add_command(label="Segoe UI", command=lambda: set_font_family("Segoe UI"))
    font_menu.add_command(label="Arial", command=lambda: set_font_family("Arial"))
    font_menu.add_command(label="Courier New", command=lambda: set_font_family("Courier New"))
    font_menu.add_command(label="Times New Roman", command=lambda: set_font_family("Times New Roman"))
    menu.add_cascade(label="Fonte", menu=font_menu)

    # Tamanho da fonte
    size_menu = tk.Menu(menu, tearoff=0)
    for size in [10, 12, 14, 16, 18, 20]:
        size_menu.add_command(label=str(size), command=lambda s=size: set_font_size(s))
    menu.add_cascade(label="Tamanho da fonte", menu=size_menu)

    # Negrito
    menu.add_command(label="Alternar Negrito", command=toggle_bold)

    menu.add_separator()

    # Sair
    menu.add_command(label="Sair", command=quit_app)

    menu.post(event.x_root, event.y_root)

    # Realce da opção selecionada
    highlight_menu_option(menu, "Alternar Negrito")

# Função para criar a janela do relógio
def create_clock_window():
    global root, label
    load_config()

    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.9)

    root.configure(bg=current_bg_color)

    root.attributes("-alpha", current_opacity)

    root.update_idletasks()  # Garante que a janela existe

    hwnd = root.winfo_id()

    # Traz para o topo, mesmo sobre jogos e apps fullscreen
   
    label = tk.Label(root, justify="center", bg=current_bg_color, fg=current_fg_color)
    label.pack(fill="both", expand=True)

    label.bind("<Button-1>", start_move)
    label.bind("<B1-Motion>", do_move)

    apply_font()
    set_position(current_position)
    update_time()

    label.bind("<Button-3>", show_context_menu)

    # Bloqueia o fechamento padrão (incluindo Alt+F4)
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    # Intercepta Alt+F4 e ignora
    def block_alt_f4(event):
        return "break"

    root.bind("<Alt-F4>", block_alt_f4)

    root.mainloop()

if __name__ == "__main__":
    create_clock_window()
