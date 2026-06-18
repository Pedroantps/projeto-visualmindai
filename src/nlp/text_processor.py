import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

# Carrega as chaves do .env para manter a segurança do repositório no GitHub
load_dotenv()

def clean_text_for_llm(raw_text: str) -> str:
    """
    Higieniza o texto bruto antes de enviar para a IA.
    Isso economiza milhares de tokens de input removendo espaços e caracteres inúteis.
    """
    text = re.sub(r'\n+', '\n', raw_text) # Remove quebras de linha múltiplas
    text = re.sub(r'\s+', ' ', text)      # Remove espaços múltiplos
    text = re.sub(r'[^\w\s\.,;:!?\-\(\)\[\]"\'•/]', '', text) # Mantém apenas texto e pontuação básica
    return text[:15000] # Limite de segurança de caracteres para não estourar a API

def process_text_to_hierarchy(text: str) -> dict:
    if not text.strip():
        raise ValueError("O texto fornecido está vazio.")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Chave GROQ_API_KEY não encontrada no arquivo .env.")

    client = Groq(api_key=api_key)

    # Prompt ultracomprimido para economizar tokens
    system_prompt = """Retorne APENAS um JSON válido e minificado. Sem markdown ou explicações.
Regras de hierarquia:
1. "name" (Tema central).
2. "children" (Títulos/Categorias).
3. "children" Nível 2 (Tópicos/Listas).
4. "children" Nível 3 (Detalhes/Sub-listas, crie APENAS se o texto exigir profundidade).
Formato: {"name":"Raiz","children":[{"name":"Cat","children":[{"name":"Top","children":[{"name":"Det"}]}]}]}"""

    clean_input = clean_text_for_llm(text)

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": clean_input}
            ],
            model="llama-3.3-70b-versatile", 
            temperature=0.1,
            max_tokens=2048
        )
        
        raw_output = response.choices[0].message.content.strip()
        
        # Limpa possíveis formatações residuais de Markdown
        if raw_output.startswith("```json"):
            raw_output = raw_output[7:-3].strip()
        elif raw_output.startswith("```"):
            raw_output = raw_output[3:-3].strip()

        hierarchy = json.loads(raw_output)
        
        if "name" not in hierarchy:
            raise ValueError("O JSON retornado não contém o nó raiz.")
            
        return hierarchy
        
    except json.JSONDecodeError:
        raise Exception("A IA não retornou um formato de dados JSON válido.")
    except Exception as e:
        raise Exception(f"Erro na comunicação com a API: {str(e)}")