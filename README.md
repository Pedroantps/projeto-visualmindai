# 🧠 VisualMind AI

O **VisualMind AI** é uma aplicação desktop desenvolvida em Python que transforma textos extensos e ficheiros PDF em mapas mentais interativos de forma automática. O software utiliza Inteligência Artificial (via API Groq/Llama 3) para compreender a semântica do texto, estruturando títulos, subtópicos e detalhes numa árvore de nós visuais perfeitamente alinhada.

Projeto desenvolvido para a disciplina de **Tópicos Avançados da Computação I** (Associação Educacional Dom Bosco - AEDB).

### 👥 Membros do Grupo
* Arthur Henrique Silva da Costa
* Davi Garutti Diniz
* Iago de Oliveira Andrade
* Pedro Antônio Pereira da Silva
* Victor Hugo dos Santos

---

## ⚙️ Pré-requisitos

Para executar a aplicação, certifique-se de que tem o **Python 3.8+** instalado na sua máquina.

## 🚀 Guia de Instalação e Execução

Siga os passos abaixo para clonar, configurar e executar a aplicação em qualquer máquina.

### 1. Clonar o Repositório
Abra o terminal e clone este repositório para a sua máquina local:
```bash
git clone [https://github.com/Pedroantps/projeto-visualmindai.git]
cd visualmind-ai
```

### 2. Criar e Ativar o Ambiente Virtual
É altamente recomendado o uso de um ambiente virtual para evitar conflitos de dependências.
* **No Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
* **No Linux/macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar as Dependências
Com o ambiente ativado, instale todas as bibliotecas necessárias utilizando o ficheiro de requisitos:
```bash
pip install -r requirements.txt
```

### 4. Configuração de Segurança (Chave da API)
O projeto utiliza a API da Groq para o processamento de linguagem natural. Para segurança do código-fonte, a chave não está no repositório.

**Como obter a sua chave da Groq (Gratuito):**
1. Aceda ao [Groq Console](https://console.groq.com/keys).
2. Crie uma conta ou inicie sessão.
3. No menu lateral esquerdo, clique em **API Keys**.
4. Clique no botão **Create API Key**, dê um nome (ex: `VisualMind`) e copie a chave gerada (ela começa com `gsk_`).

**Como configurar no projeto:**
1. Crie um ficheiro chamado `.env` na raiz do projeto (na mesma pasta deste README).
2. Cole a chave que acabou de copiar dentro do ficheiro `.env` no seguinte formato:
   ```env
   GROQ_API_KEY=gsk_sua_chave_copiada_aqui

### 5. Executar a Aplicação
Com tudo configurado, inicie a interface gráfica executando o módulo principal:
```bash
python -m src.main
```

---

## 🛠️ Principais Funcionalidades
* **Importação de Documentos:** Suporte nativo para extração de texto a partir de ficheiros `.pdf` e `.txt`.
* **Geração Inteligente:** O algoritmo Bottom-Up calcula dinamicamente o espaçamento das caixas e diminui o tamanho da fonte para textos longos, evitando sobreposição visual.
* **Layout Bilateral:** O mapa mental divide-se simetricamente (esquerda/direita) para facilitar a leitura.
* **Exportação HD:** Exporte o mapa gerado para imagem `.png` em alta resolução ou ficheiro `.pdf` vetorizado.