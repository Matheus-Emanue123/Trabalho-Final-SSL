# 🌟 Detector de Pulsares Educativo v2.0

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green?style=for-the-badge)
![Matplotlib](https://img.shields.io/badge/Plots-Matplotlib-orange?style=for-the-badge)
![NumPy](https://img.shields.io/badge/NumPy-Scipy-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Sistema Interativo de Processamento Digital de Sinais**  
*Aplicado à Detecção de Pulsares Astronômicos*

[🚀 Instalação](#-instalação-e-configuração) •
[📚 Tutorial](#-tutorial-completo) •
[🔬 Teoria](#-fundamentos-teóricos) •
[⚡ Uso](#-como-usar) •
[🛠️ Desenvolvimento](#-desenvolvimento)

</div>

---

## 📖 Sobre o Projeto

Este simulador educativo combina **astrofísica** e **processamento digital de sinais** para criar uma experiência de aprendizado única. Os usuários exploram desde conceitos básicos de superposição de ondas até técnicas avançadas de análise espectral, tudo no contexto da detecção de pulsares - estrelas de nêutrons que são alguns dos objetos mais extremos do universo.

### 🌟 O que são Pulsares?

Pulsares são estrelas de nêutrons altamente magnetizadas que rotacionam rapidamente (até 700 vezes por segundo!). Elas emitem feixes de radiação eletromagnética que, quando apontados para a Terra, são detectados como pulsos regulares - funcionando como "faróis cósmicos" com precisão comparable a relógios atômicos.

**Características importantes:**
- ⭐ **Massa**: 1.4 massas solares comprimidas em ~20 km de diâmetro
- 🌀 **Rotação**: De milissegundos a segundos por rotação
- 📡 **Emissão**: Radiação em múltiplas frequências simultaneamente
- 🎯 **Precisão**: Alguns são mais precisos que relógios atômicos

---

## 🎯 Objetivos Educacionais

### 📊 Conceitos de Sinais e Sistemas
- **Síntese de Sinais**: Superposição de componentes senoidais
- **Amostragem Digital**: Teorema de Nyquist e discretização
- **Sistemas LTI**: Linearidade e invariância temporal
- **Filtragem Digital**: Filtros passa-baixa Butterworth
- **Análise Espectral**: Transformada de Fourier (FFT)
- **Processamento de Ruído**: Relação sinal-ruído (SNR)

### 🧠 Habilidades Práticas
- Implementação de algoritmos de processamento digital
- Análise de sinais no domínio tempo-frequência
- Detecção de periodicidade em sinais ruidosos
- Interpretação de espectros de potência
- Configuração de parâmetros de filtragem

---

## 🚀 Instalação e Configuração

### 📋 Pré-requisitos
```bash
Python 3.8 ou superior
Git (para clonagem do repositório)
```

### 🔧 Instalação Automática

#### Windows
```batch
# Execute o script de instalação
run.bat
```

#### PowerShell
```powershell
# Execute o script PowerShell
.\run.ps1
```

#### Linux/Mac
```bash
# Clone o repositório
git clone https://github.com/Matheus-Emanue123/Trabalho-Final-SSL.git
cd Trabalho-Final-SSL

# Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt

# Execute a aplicação
python src/main_app.py
```

### 📦 Instalação Manual

1. **Clone o repositório:**
```bash
git clone https://github.com/Matheus-Emanue123/Trabalho-Final-SSL.git
cd Trabalho-Final-SSL
```

2. **Crie um ambiente virtual:**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação:**
```bash
python src/main_app.py
```

### 📚 Dependências
- **numpy**: Computação numérica e arrays
- **matplotlib**: Visualização de gráficos e plots
- **scipy**: Algoritmos científicos (filtros, FFT)
- **tkinter**: Interface gráfica (incluído no Python)

---

## 📚 Tutorial Completo

### 🎮 Modos de Operação

#### 🎓 Modo Educativo
- **Características**: Parâmetros fixos e reproduzíveis
- **Componentes**: 3 senoides bem definidas (5, 15, 25 Hz)
- **Objetivo**: Demonstração clara dos conceitos
- **Ideal para**: Primeira experiência e aprendizado

#### 🎲 Modo Aleatório
- **Características**: Simulação realística
- **Variações**: Pulsar típico, sinal irregular, apenas ruído
- **Desafio**: Nem sempre há pulsar detectável!
- **Ideal para**: Teste de conhecimento e casos reais

### 📖 Passo a Passo Detalhado

#### 🔬 Passo 1: Geração de Componentes
**O que acontece:**
- Criação de 2-5 componentes senoidais independentes
- Cada componente tem frequência, amplitude e fase específicas
- Visualização individual de cada onda

**Conceitos aplicados:**
```mathematical
x_i(t) = A_i · sin(2πf_i·t + φ_i)
```
- **A_i**: Amplitude da componente i
- **f_i**: Frequência em Hz
- **φ_i**: Fase inicial em radianos

**Observações importantes:**
- Frequências determinam a periodicidade
- Amplitudes afetam a intensidade do sinal
- Fases criam padrões de interferência

#### ⚡ Passo 2: Superposição Linear
**O que acontece:**
- Soma algébrica de todas as componentes
- Demonstração do princípio da superposição
- Comparação entre componentes e resultado final

**Conceitos aplicados:**
```mathematical
x(t) = Σ x_i(t) = Σ A_i · sin(2πf_i·t + φ_i)
```

**Fenômenos observados:**
- **Interferência construtiva**: Ondas em fase se somam
- **Interferência destrutiva**: Ondas fora de fase se cancelam
- **Batimento**: Frequências próximas criam modulação

#### 📡 Passo 3: Adição de Ruído
**O que acontece:**
- Adição de ruído gaussiano branco
- Simulação de condições reais de detecção
- Cálculo da relação sinal-ruído (SNR)

**Conceitos aplicados:**
```mathematical
y(t) = x(t) + n(t)
```
- **n(t)**: Ruído gaussiano com média zero
- **SNR**: 10·log₁₀(P_sinal/P_ruído) [dB]

**Tipos de ruído simulados:**
- Ruído térmico de receptores
- Interferência cósmica de fundo
- Ruído atmosférico
- Interferência de equipamentos

#### 🔧 Passo 4: Filtragem Digital
**O que acontece:**
- Aplicação de filtro Butterworth passa-baixa
- Remoção de componentes de alta frequência (ruído)
- Preservação do sinal útil

**Conceitos aplicados:**
- **Função de transferência**: H(z) do filtro digital
- **Frequência de corte**: Limite entre passagem e rejeição
- **Ordem do filtro**: Determina a inclinação da resposta
- **Filtragem bidirecional**: Zero distorção de fase

**Parâmetros configuráveis:**
- Frequência de corte: 35 Hz (ajustável)
- Ordem: 5ª ordem (suavidade vs. seletividade)
- Tipo: Butterworth (resposta maximalmente plana)

#### 🚀 Passo 5: Análise FFT
**O que acontece:**
- Transformada de Fourier do sinal filtrado
- Cálculo do espectro de potência
- Detecção automática de picos de frequência
- Determinação do período de pulsação

**Conceitos aplicados:**
```mathematical
X(f) = ∫ x(t) · e^(-j2πft) dt
P(f) = |X(f)|²
```

**Algoritmo de detecção:**
1. Calcular FFT do sinal filtrado
2. Encontrar picos no espectro de potência
3. Identificar frequência dominante
4. Calcular período: T = 1/f

---

## 🔬 Fundamentos Teóricos

### 📐 Matemática dos Sinais

#### Síntese por Superposição
A base matemática dos pulsares reside na síntese de Fourier:

```mathematical
x(t) = A₀ + Σ[n=1 to ∞] Aₙcos(nω₀t + φₙ)
```

Para nosso simulador, usamos uma aproximação finita:
```mathematical
x(t) = Σ[i=1 to N] Aᵢsin(2πfᵢt + φᵢ)
```

#### Amostragem e Discretização
O teorema de Nyquist garante que:
```mathematical
fs ≥ 2 · fmax
```
- **fs**: Frequência de amostragem (1000 Hz)
- **fmax**: Maior frequência do sinal (50 Hz)
- **Margem de segurança**: 10x oversampling

#### Filtragem Digital
O filtro Butterworth de ordem N tem resposta:
```mathematical
|H(jω)|² = 1 / (1 + (ω/ωc)^(2N))
```
- **ωc**: Frequência de corte angular
- **N**: Ordem do filtro
- **Atenuação**: -20N dB/década

#### Transformada de Fourier Discreta
A DFT é calculada eficientemente pela FFT:
```mathematical
X[k] = Σ[n=0 to N-1] x[n] · e^(-j2πkn/N)
```
- **Resolução**: Δf = fs/N
- **Complexidade**: O(N log N)

### 🌌 Física dos Pulsares

#### Formação e Estrutura
- **Colapso gravitacional**: Estrela massiva → estrela de nêutrons
- **Conservação do momento angular**: Rotação extremamente rápida
- **Campo magnético**: 10⁸-10¹⁵ Gauss (Terra: ~0.5 Gauss)

#### Mecanismo de Emissão
- **Aceleração de partículas**: Campo magnético rotativo
- **Radiação síncrotron**: Elétrons relativísticos
- **Cone de emissão**: Alinhado com eixo magnético
- **Efeito farol**: Detecção periódica na Terra

#### Características Observacionais
- **Período**: 1.337 ms (mais rápido) a 11.76 s (mais lento)
- **Deriva**: P aumenta devido à perda de energia
- **Glitches**: Mudanças súbitas no período
- **Pulso duplo**: Alguns pulsares têm dois feixes

---

## ⚡ Como Usar

### 🎯 Interface do Usuário

#### Painel Lateral
- **Progresso da Missão**: Barra visual do progresso
- **Botões de Controle**: Execução sequencial dos passos
- **Modo de Operação**: Toggle educativo/aleatório
- **Banco de Conhecimento**: Explicações detalhadas

#### Área Principal
- **Visualização Gráfica**: Plots em tempo real
- **Toolbar de Navegação**: Zoom, pan, salvar figuras
- **Status do Sistema**: Indicadores de operação

#### Barra de Status
- **Estado Atual**: Operação em andamento
- **Indicador Visual**: LED colorido de status

### 🔄 Fluxo de Trabalho

1. **Inicialização**
   - Escolha o modo (educativo/aleatório)
   - Leia as informações teóricas
   - Clique em "Gerar Componentes"

2. **Execução Sequencial**
   - Execute os passos em ordem
   - Observe as visualizações
   - Leia as explicações de cada etapa

3. **Análise de Resultados**
   - Interprete os espectros de potência
   - Identifique frequências detectadas
   - Compare com valores teóricos

4. **Experimentação**
   - Use "Reinicializar Sistema" para novas tentativas
   - Alterne entre modos
   - Explore diferentes cenários

### 🎛️ Controles Avançados

#### Modificação de Parâmetros
Para usuários avançados, os parâmetros podem ser modificados editando:
```python
# Em main_app.py
self.Fs = 1000          # Frequência de amostragem
self.duration = 2       # Duração do sinal
cutoff_freq = 35        # Frequência de corte do filtro
filter_order = 5        # Ordem do filtro
```

#### Extensões Possíveis
- Diferentes tipos de filtros (Chebyshev, Elliptic)
- Análise de múltiplos pulsares simultâneos
- Simulação de efeitos Doppler
- Processamento em tempo real

---

## 🛠️ Desenvolvimento

### 📁 Estrutura do Projeto
```
Trabalho-Final-SSL/
├── src/
│   ├── main_app.py         # Interface principal e lógica
│   ├── generate_signal.py  # Geração de sinais sintéticos
│   ├── process_signal.py   # Processamento e filtragem
│   └── __pycache__/        # Cache Python
├── requirements.txt        # Dependências Python
├── run.bat                # Script Windows
├── run.ps1                # Script PowerShell
├── README.md              # Esta documentação
└── LICENSE                # Licença MIT
```

### 🔧 Arquitetura do Sistema

#### Classe Principal: `PulsarDetectorApp`
- **Responsabilidade**: Interface gráfica e coordenação
- **Padrão**: MVC (Model-View-Controller)
- **Threading**: Single-thread com processamento assíncrono

#### Módulo de Geração: `generate_signal.py`
- **Função principal**: `generate_and_save_random_signal()`
- **Modos**: Educativo, aleatório, apenas ruído
- **Saída**: Sinal temporal + metadados

#### Módulo de Processamento: `process_signal.py`
- **Função principal**: `process_and_analyze_signal()`
- **Algoritmos**: Butterworth + FFT + detecção de picos
- **Saída**: Sinal filtrado + análise espectral

### 🎨 Customização

#### Esquema de Cores
O sistema usa um esquema futurístico modificável:
```python
self.colors = {
    'bg_dark': '#1a1a2e',       # Fundo principal
    'accent_cyan': '#00d4ff',   # Destaques
    'text_primary': '#ffffff',  # Texto principal
    # ... outros valores
}
```

#### Fontes Tecnológicas
```python
self.fonts = {
    'title': ('Consolas', 18, 'bold'),
    'subtitle': ('Segoe UI', 12, 'normal'),
    # ... outras definições
}
```

### 📊 Métricas de Performance

#### Complexidade Computacional
- **Geração de sinal**: O(N) onde N = fs × duration
- **Filtragem**: O(N) (implementação FIR/IIR)
- **FFT**: O(N log N)
- **Total**: O(N log N) dominante

#### Uso de Memória
- **Sinal base**: ~16 KB (2000 amostras × 8 bytes)
- **Espectros**: ~8 KB cada
- **Interface**: ~5-10 MB
- **Total**: <20 MB típico

### 🧪 Testes e Validação

#### Casos de Teste
1. **Sinal conhecido**: Verificação com parâmetros fixos
2. **Apenas ruído**: Comportamento sem sinal
3. **SNR baixa**: Robustez em condições adversas
4. **Frequências limite**: Teste dos filtros

#### Validação Científica
- Comparação com dados reais do pulsar B1919+21
- Verificação das equações de Fourier
- Teste de conservação de energia

---

## 📈 Casos de Uso Educacionais

### 🎓 Para Estudantes

#### Disciplinas Aplicáveis
- **Sinais e Sistemas Lineares**
- **Processamento Digital de Sinais**
- **Métodos Matemáticos para Engenharia**
- **Física Moderna**
- **Astronomia e Astrofísica**

#### Atividades Sugeridas
1. **Laboratório Guiado**: Seguir todos os passos comentando
2. **Projeto Livre**: Modificar parâmetros e observar efeitos
3. **Pesquisa**: Conectar com dados reais de pulsares
4. **Programação**: Estender funcionalidades

### 👨‍🏫 Para Professores

#### Planos de Aula
- **Aula 1**: Introdução aos pulsares e síntese de sinais
- **Aula 2**: Amostragem e teorema de Nyquist
- **Aula 3**: Filtragem digital e sistemas LTI
- **Aula 4**: Análise espectral e FFT
- **Aula 5**: Projeto final e discussão

#### Recursos Complementares
- Slides de apoio (podem ser gerados)
- Exercícios com diferentes parâmetros
- Conexão com dados astronômicos reais
- Extensões para pesquisa

---

## 🌟 Resultados e Interpretação

### 📊 Análise de Espectros

#### Espectro Típico (Modo Educativo)
- **Picos esperados**: 5, 15, 25 Hz
- **Relação harmônica**: f₂ = 3f₁, f₃ = 5f₁
- **Largura dos picos**: Determinada pela janela temporal

#### Variações no Modo Aleatório
- **Pulsar típico**: Fundamental + harmônicos
- **Sinal irregular**: Picos próximos (batimento)
- **Apenas ruído**: Espectro plano sem picos

### 🎯 Critérios de Detecção

#### Algoritmo Automático
1. Busca em faixa de interesse (0.5-50 Hz)
2. Identificação do pico máximo
3. Verificação de SNR local
4. Cálculo do período correspondente

#### Interpretação Manual
- **Picos nítidos**: Pulsar bem definido
- **Múltiplos picos**: Sistema binário ou harmônicos
- **Ausência de picos**: Sem sinal detectável

### 🔍 Troubleshooting

#### Problemas Comuns
- **Não detecta pulsar**: Verificar modo aleatório (pode ser normal)
- **Frequências incorretas**: Ajustar filtro de corte
- **Interface lenta**: Reduzir duração do sinal
- **Gráficos não aparecem**: Verificar instalação matplotlib

---

## 🤝 Contribuições

### 💡 Como Contribuir
1. **Fork** do repositório
2. **Clone** sua versão local
3. **Crie** branch para feature
4. **Desenvolva** e teste
5. **Submeta** pull request

### 🐛 Relatório de Bugs
- Use as **Issues** do GitHub
- Inclua **passos para reproduzir**
- Forneça **informações do sistema**
- Adicione **capturas de tela** se relevante

### ✨ Ideias de Melhorias
- **Novos algoritmos**: Wavelets, filtros adaptativos
- **Visualizações**: Espectrogramas, mapas 3D
- **Dados reais**: Integração com catálogos astronômicos
- **Performance**: Otimizações para sinais longos

---

## 📞 Suporte e Contato

### 🔗 Links Úteis
- **Repositório**: [GitHub](https://github.com/Matheus-Emanue123/Trabalho-Final-SSL)
- **Issues**: [Reportar Problemas](https://github.com/Matheus-Emanue123/Trabalho-Final-SSL/issues)
- **Wiki**: [Documentação Estendida](https://github.com/Matheus-Emanue123/Trabalho-Final-SSL/wiki)

### 📚 Recursos Adicionais
- **Catálogo de Pulsares**: [ATNF Pulsar Catalogue](https://www.atnf.csiro.au/research/pulsar/psrcat/)
- **Teoria DSP**: [Smith - Digital Signal Processing](https://www.dspguide.com/)
- **Astronomia**: [Handbook of Pulsar Astronomy](https://ui.adsabs.harvard.edu/abs/2004hpa..book.....L/abstract)

### 👥 Equipe de Desenvolvimento
- **Desenvolvedor Principal**: Matheus Emanuel e João Paulo
- **Orientação Acadêmica**: Thabatta Araújo
- **Disciplina**: Sinais e Sistemas Lineares

---

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

### ⚖️ Termos de Uso
- **Uso educacional**: Livre e incentivado
- **Uso comercial**: Permitido com atribuição
- **Modificações**: Livres, mantendo a licença
- **Distribuição**: Livre, incluindo o código fonte

---

<div align="center">

**🌟 Feito com ❤️ para a comunidade científica e educacional**

*"Os pulsares são como faróis cósmicos que nos ensinam sobre física extrema e nos guiam através do universo."*

---

![Pulsar Animation](https://upload.wikimedia.org/wikipedia/commons/c/c0/Pulsar_schematic.svg)

</div>
