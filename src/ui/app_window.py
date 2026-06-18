import customtkinter as ctk
from tkinter import filedialog, messagebox

from src.utils.file_handler import extract_text_from_pdf, extract_text_from_txt
from src.nlp.text_processor import process_text_to_hierarchy
from src.graph.mind_map import draw_mind_map

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("VisualMind AI")
        self.geometry("1100x700") 
        self.minsize(900, 600)
        
        self.current_fig = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._create_sidebar()
        self._create_main_content()

    def _create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="VisualMind AI", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        self.btn_import = ctk.CTkButton(self.sidebar_frame, text="Importar Arquivo", command=self.import_document)
        self.btn_import.grid(row=1, column=0, padx=20, pady=10)

        self.btn_generate = ctk.CTkButton(self.sidebar_frame, text="Gerar Mapa Mental", command=self.generate_mind_map, fg_color="#28a745", hover_color="#218838")
        self.btn_generate.grid(row=2, column=0, padx=20, pady=10)

        # Botão Inteligente: Só aparece quando o mapa está gerado
        self.btn_edit_text = ctk.CTkButton(self.sidebar_frame, text="Editar Texto", command=self.show_text_view, fg_color="#ff9800", hover_color="#e65100")

        self.btn_clear = ctk.CTkButton(self.sidebar_frame, text="Limpar Dados", command=self.clear_data, fg_color="#dc3545", hover_color="#c82333")
        self.btn_clear.grid(row=7, column=0, padx=20, pady=10)

        self.btn_export = ctk.CTkButton(self.sidebar_frame, text="Exportar Mapa", command=self.export_map, state="disabled")
        self.btn_export.grid(row=8, column=0, padx=20, pady=(10, 20))

    def _create_main_content(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        # Uma única coluna e linha para ocupar 100% do espaço
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # --- TELA 1: ÁREA DE TEXTO ---
        self.text_view = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.text_view.grid_columnconfigure(0, weight=1)
        self.text_view.grid_rowconfigure(1, weight=1)

        self.text_label = ctk.CTkLabel(self.text_view, text="Texto de Entrada:", font=ctk.CTkFont(size=14, weight="bold"))
        self.text_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.text_area = ctk.CTkTextbox(self.text_view, wrap="word", corner_radius=8, font=ctk.CTkFont(size=14))
        self.text_area.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # --- TELA 2: ÁREA DO MAPA ---
        self.map_view = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.map_view.grid_columnconfigure(0, weight=1)
        self.map_view.grid_rowconfigure(1, weight=1)

        self.map_label = ctk.CTkLabel(self.map_view, text="Visualização do Mapa Mental:", font=ctk.CTkFont(size=14, weight="bold"))
        self.map_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.map_container = ctk.CTkFrame(self.map_view, corner_radius=8, fg_color="#242424")
        self.map_container.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # Inicia a aplicação na Tela 1
        self.show_text_view()

    # --- Lógica de Alternância de Telas ---
    def show_text_view(self):
        self.map_view.grid_remove() # Esconde o mapa
        self.text_view.grid(row=0, column=0, sticky="nsew") # Mostra o texto
        self.btn_edit_text.grid_remove() # Esconde o botão de editar

    def show_map_view(self):
        self.text_view.grid_remove() # Esconde o texto
        self.map_view.grid(row=0, column=0, sticky="nsew") # Mostra o mapa
        self.btn_edit_text.grid(row=3, column=0, padx=20, pady=10) # Mostra o botão de editar

    # --- Ações ---
    def import_document(self):
        filepath = filedialog.askopenfilename(
            title="Selecione um arquivo",
            filetypes=(("Arquivos PDF e TXT", "*.pdf;*.txt"), ("PDF", "*.pdf"), ("Texto", "*.txt"), ("Todos os Arquivos", "*.*"))
        )
        if not filepath: return 
        try:
            if filepath.lower().endswith(".pdf"): content = extract_text_from_pdf(filepath)
            elif filepath.lower().endswith(".txt"): content = extract_text_from_txt(filepath)
            else:
                messagebox.showwarning("Formato Inválido", "Por favor, selecione um arquivo .pdf ou .txt.")
                return

            self.text_area.delete("1.0", ctk.END)
            self.text_area.insert("1.0", content)
            self.clear_map_container()
            self.show_text_view() # Garante que está na tela de texto após importar
        except Exception as e:
            messagebox.showerror("Erro de Importação", f"Não foi possível ler o arquivo.\nDetalhes: {str(e)}")

    def clear_data(self):
        self.text_area.delete("1.0", ctk.END)
        self.clear_map_container()
        self.show_text_view() # Retorna para a tela original como você pediu

    def clear_map_container(self):
        for widget in self.map_container.winfo_children():
            widget.destroy()
        self.current_fig = None
        self.btn_export.configure(state="disabled")

    def generate_mind_map(self):
        text = self.text_area.get("1.0", ctk.END).strip()
        if not text:
            messagebox.showwarning("Aviso", "A caixa de texto está vazia. Insira ou importe um conteúdo primeiro.")
            return
        try:
            hierarchy = process_text_to_hierarchy(text)
            self.current_fig = draw_mind_map(hierarchy, self.map_container)
            self.btn_export.configure(state="normal")
            
            # Quando a geração dá certo, troca para a tela do mapa
            self.show_map_view()
        except Exception as e:
            messagebox.showerror("Erro de Processamento", f"Ocorreu um erro ao gerar o mapa.\nDetalhes: {str(e)}")

    def export_map(self):
        if self.current_fig is None: return
        filepath = filedialog.asksaveasfilename(
            title="Salvar Mapa Mental", defaultextension=".png",
            filetypes=(("Imagem PNG", "*.png"), ("Documento PDF", "*.pdf"))
        )
        if not filepath: return
        try:
            if filepath.lower().endswith(".pdf"): self.current_fig.savefig(filepath, format="pdf", bbox_inches="tight")
            else: self.current_fig.savefig(filepath, format="png", bbox_inches="tight", dpi=300)
            messagebox.showinfo("Sucesso", f"Mapa exportado com sucesso em:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Erro de Exportação", f"Falha ao salvar o arquivo.\nDetalhes: {str(e)}")