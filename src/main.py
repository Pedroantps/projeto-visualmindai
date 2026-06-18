import customtkinter as ctk
import networkx as nx
import spacy
import PyPDF2
from dotenv import load_dotenv
from src.ui.app_window import AppWindow

def main():
    # Instancia e executa o loop principal da aplicação gráfica
    app = AppWindow()
    app.mainloop()

if __name__ == "__main__":
    main()