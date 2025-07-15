# 🌟 Detector de Pulsares Educativo

Um simulador interativo para aprender **Processamento Digital de Sinais** aplicado à detecção de pulsares astronômicos.

## 📖 Sobre o Projeto

Este projeto é uma ferramenta educativa que demonstra conceitos fundamentais de **Sinais e Sistemas Lineares** através da simulação de detecção de pulsares - estrelas de nêutrons que emitem radiação em intervalos regulares.

## 🎯 Objetivos de Aprendizado

### Conceitos Teóricos Abordados:
- **Síntese de Sinais**: Superposição de componentes senoidais
- **Amostragem**: Teorema de Nyquist e discretização
- **Filtragem Digital**: Filtros passa-baixa Butterworth
- **Análise Espectral**: Transformada de Fourier (FFT)
- **Sistemas LTI**: Linearidade e invariância temporal
- **Processamento de Ruído**: Relação sinal-ruído (SNR)

### Habilidades Práticas:
- Implementação de filtros digitais
- Análise de sinais no domínio da frequência
- Detecção de periodicidade em sinais ruidosos
- Visualização de dados científicos

## 🚀 Como Executar

### Pré-requisitos
```bash
Python 3.8+
```

### Instalação
```bash
# Clone o repositório
git clone [URL_DO_REPO]
cd Trabalho-Final-SSL

# Crie um ambiente virtual (recomendado)
python -m venv .venv

# Ative o ambiente virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### Execução
```bash
# Opção 1: Interface Educativa Completa (Recomendado)
python src/main_app.py

# Opção 2: Demonstração Rápida
python src/demo_rapida.py

# Opção 3: Usar scripts de conveniência (Windows)
# Duplo clique em run.bat
# OU execute run.ps1 no PowerShell
```

## 📚 Estrutura do Projeto

```
src/
├── main_app.py          # Interface principal educativa
├── generate_signal.py   # Geração de sinais sintéticos
├── process_signal.py    # Processamento e análise
└── __pycache__/        # Cache Python
requirements.txt         # Dependências
README.md               # Este arquivo
```

## 🔬 Metodologia Educativa

O aprendizado é estruturado em **5 passos progressivos**:

### 1️⃣ **Geração de Componentes**
- Criação de sinais senoidais individuais
- Conceitos: frequência, amplitude, fase
- Visualização: componentes separadas

### 2️⃣ **Superposição de Sinais**
- Aplicação do princípio da superposição
- Conceitos: linearidade, interferência
- Visualização: antes e depois da soma

### 3️⃣ **Adição de Ruído**
- Simulação de condições reais
- Conceitos: ruído gaussiano, SNR
- Visualização: degradação do sinal

### 4️⃣ **Filtragem Digital**
- Aplicação de filtro passa-baixa
- Conceitos: sistemas LTI, convolução
- Visualização: comparação antes/depois

### 5️⃣ **Análise FFT**
- Transformada de Fourier
- Conceitos: domínio da frequência, detecção de picos
- Visualização: espectro de potência

## 🎨 Interface Educativa

### Características:
- **Design Moderno**: Interface limpa e intuitiva
- **Progressão Guiada**: Passos sequenciais com validação
- **Explicações Contextuais**: Teoria integrada à prática
- **Visualizações Dinâmicas**: Gráficos adaptativos por etapa
- **Feedback Imediato**: Resultados em tempo real

### Painéis:
- **Controle**: Botões de navegação entre passos
- **Progresso**: Barra visual do avanço
- **Teoria**: Explicações detalhadas dos conceitos
- **Visualização**: Gráficos matplotlib integrados

## 📊 Resultados Esperados

Ao final do processo, o estudante terá:
- Detectado a periodicidade do pulsar simulado
- Compreendido cada etapa do processamento
- Visualizado o efeito de cada operação
- Conectado teoria e prática de forma concreta

## 🔧 Parâmetros Configuráveis

```python
# Geração de Sinal
Fs = 1000 Hz           # Frequência de amostragem
duration = 2 s         # Duração do sinal
noise_amplitude = 0.5  # Amplitude do ruído

# Filtragem
cutoff_freq = 35 Hz    # Frequência de corte
filter_order = 5       # Ordem do filtro Butterworth

# Componentes (exemplo)
frequencies = [5, 15, 25] Hz  # Componentes do pulsar
amplitudes = [1.5, 1.0, 0.8] # Amplitudes relativas
```

## 🌟 Aplicações Reais

### Astronomia:
- Detecção de pulsares reais
- Estudo de matéria ultra-densa
- Testes de relatividade geral
- Navegação espacial

### Processamento de Sinais:
- Radar e sonar
- Comunicações digitais
- Análise biomédica
- Controle industrial

## 👥 Equipe

**Curso**: Sinais e Sistemas Lineares  
**Instituição**: CEFET  
**Período**: 5º Período

## 📝 Licença

Este projeto é desenvolvido para fins educacionais.

---

🌟 **"Explorando o cosmos através do processamento digital de sinais!"** 🌟
