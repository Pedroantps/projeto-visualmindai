# teste_pln.py
import json
from src.nlp.text_processor import process_text_to_hierarchy

texto_exemplo = """
A Engenharia de Software é uma disciplina da engenharia dedicada a todos os aspectos da produção de software.
O desenvolvimento de software moderno exige práticas ágeis. A qualidade do software e a engenharia de requisitos
são etapas fundamentais. Muitos profissionais usam Python para criar soluções de inteligência artificial.
O Python possui bibliotecas como spaCy para ajudar na inteligência e na qualidade da engenharia.
"""

print("Processando...")
hierarquia = process_text_to_hierarchy(texto_exemplo)

# Imprimimos de forma bonita (indentada) para visualizar a árvore
print(json.dumps(hierarquia, indent=4, ensure_ascii=False))