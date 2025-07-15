import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

# Importa as funções dos seus outros scripts
from generate_signal import generate_and_save_random_signal
from process_signal import process_and_analyze_signal

class PulsarDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌟 Detector de Pulsares Educativo - Sinais e Sistemas Lineares")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')

        # Variáveis de estado
        self.current_noisy_signal = None
        self.current_time_vector = None
        self.individual_components = []
        self.clean_signal = None
        self.Fs = 1000
        self.duration = 2
        self.current_step = 0
        self.total_steps = 5

        # Configurações visuais
        try:
            plt.style.use('seaborn-v0_8')
        except:
            try:
                plt.style.use('seaborn')
            except:
                plt.style.use('default')
        
        self._create_widgets()

    def _create_widgets(self):
        # === PAINEL SUPERIOR: TÍTULO E PROGRESSO ===
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(side=tk.TOP, fill=tk.X)
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, text="🌟 DETECTOR DE PULSARES EDUCATIVO", 
                              font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(pady=15)

        subtitle_label = tk.Label(header_frame, text="Aprendendo Processamento Digital de Sinais na Prática", 
                                 font=('Arial', 10), fg='#ecf0f1', bg='#2c3e50')
        subtitle_label.pack()

        # === PAINEL LATERAL: CONTROLES E EXPLICAÇÕES ===
        self.sidebar = tk.Frame(self.root, bg='#34495e', width=350)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Progresso dos passos
        progress_frame = tk.Frame(self.sidebar, bg='#34495e')
        progress_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(progress_frame, text="📚 PROGRESSO DO APRENDIZADO", 
                font=('Arial', 12, 'bold'), fg='white', bg='#34495e').pack()

        self.progress_var = tk.StringVar(value="Passo 0/5: Início")
        self.progress_label = tk.Label(progress_frame, textvariable=self.progress_var,
                                      font=('Arial', 10), fg='#ecf0f1', bg='#34495e')
        self.progress_label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(progress_frame, length=300, mode='determinate')
        self.progress_bar.pack(pady=5)

        # Botões de controle
        button_frame = tk.Frame(self.sidebar, bg='#34495e')
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        self.step_buttons = []
        steps = [
            ("🎲 1. Gerar Componentes", self._step1_generate_components),
            ("➕ 2. Superposição", self._step2_superposition),
            ("📡 3. Adicionar Ruído", self._step3_add_noise),
            ("🔽 4. Filtrar Sinal", self._step4_filter_signal),
            ("📊 5. Análise FFT", self._step5_fft_analysis)
        ]

        for i, (text, command) in enumerate(steps):
            btn = tk.Button(button_frame, text=text, command=command,
                           font=('Arial', 10, 'bold'), bg='#3498db', fg='white',
                           relief=tk.RAISED, bd=2, padx=10, pady=5)
            btn.pack(fill=tk.X, pady=2)
            btn.configure(state='disabled' if i > 0 else 'normal')
            self.step_buttons.append(btn)

        # Reset button
        reset_btn = tk.Button(button_frame, text="🔄 Recomeçar", command=self._reset_all,
                             font=('Arial', 10, 'bold'), bg='#e74c3c', fg='white',
                             relief=tk.RAISED, bd=2, padx=10, pady=5)
        reset_btn.pack(fill=tk.X, pady=10)

        # Área de explicações
        explanation_frame = tk.LabelFrame(self.sidebar, text="📖 Conceitos Teóricos", 
                                         font=('Arial', 11, 'bold'), fg='white', bg='#34495e')
        explanation_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.explanation_text = scrolledtext.ScrolledText(explanation_frame, 
                                                         wrap=tk.WORD, width=40, height=15,
                                                         font=('Arial', 9), bg='#ecf0f1')
        self.explanation_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # === ÁREA PRINCIPAL: GRÁFICOS ===
        self.plot_frame = tk.Frame(self.root, bg='white')
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configuração inicial do matplotlib
        self.fig, self.ax = plt.subplots(1, 1, figsize=(10, 6))
        self.fig.patch.set_facecolor('white')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        self.toolbar.update()

        # Status bar
        self.status_var = tk.StringVar(value="Pronto para começar! Clique no primeiro passo.")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W, font=('Arial', 9))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self._show_welcome_screen()

    def _show_welcome_screen(self):
        """Tela inicial com explicação sobre pulsares"""
        self.ax.clear()
        self.ax.text(0.5, 0.7, "🌟 BEM-VINDO AO DETECTOR DE PULSARES!", 
                    ha='center', va='center', fontsize=20, fontweight='bold',
                    transform=self.ax.transAxes)
        
        self.ax.text(0.5, 0.5, "Um pulsar é uma estrela de nêutrons rotativa que emite\nfeixes de radiação em intervalos regulares.", 
                    ha='center', va='center', fontsize=12,
                    transform=self.ax.transAxes)
        
        self.ax.text(0.5, 0.3, "Neste simulador, você aprenderá como detectar\nestes sinais usando processamento digital!", 
                    ha='center', va='center', fontsize=11, style='italic',
                    transform=self.ax.transAxes)
        
        self.ax.text(0.5, 0.1, "👆 Clique no primeiro passo para começar!", 
                    ha='center', va='center', fontsize=14, color='blue',
                    transform=self.ax.transAxes)
        
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.axis('off')
        self.canvas.draw()
        
        welcome_text = """
🌟 INTRODUÇÃO AOS PULSARES

Os pulsares são estrelas de nêutrons que rotacionam rapidamente e emitem feixes de radiação eletromagnética. Quando esses feixes apontam para a Terra, detectamos pulsos regulares - como um farol cósmico!

🎯 OBJETIVOS DE APRENDIZADO:
• Compreender superposição de sinais senoidais
• Aplicar conceitos de amostragem e discretização  
• Entender filtragem digital passa-baixa
• Realizar análise espectral com FFT
• Detectar periodicidade em sinais ruidosos

📚 CONCEITOS ABORDADOS:
• Síntese de sinais por superposição
• Teorema de Nyquist
• Sistemas lineares invariantes no tempo (LTI)
• Transformada de Fourier Discreta
• Filtragem Butterworth
• Relação sinal-ruído (SNR)

Clique no primeiro passo para começar a jornada!
        """
        self.explanation_text.delete(1.0, tk.END)
        self.explanation_text.insert(tk.END, welcome_text)

    def _update_progress(self, step, description):
        """Atualiza a barra de progresso e status"""
        self.current_step = step
        self.progress_var.set(f"Passo {step}/{self.total_steps}: {description}")
        self.progress_bar['value'] = (step / self.total_steps) * 100
        self.status_var.set(f"Executando: {description}")
        
        # Habilita o próximo botão
        for i, btn in enumerate(self.step_buttons):
            if i <= step:
                btn.configure(state='normal', bg='#27ae60' if i < step else '#3498db')
            else:
                btn.configure(state='disabled', bg='#95a5a6')

    def _step1_generate_components(self):
        """Passo 1: Gerar e mostrar componentes senoidais individuais"""
        try:
            # Gerar componentes individuais
            T = 1 / self.Fs
            t = np.arange(0, self.duration, T)
            self.current_time_vector = t
            
            # Parâmetros fixos para demonstração educativa
            np.random.seed(42)  # Para resultados reproduzíveis
            num_components = 3
            
            self.individual_components = []
            freqs = [5, 15, 25]  # Frequências bem definidas para visualização
            amps = [1.5, 1.0, 0.8]
            phases = [0, np.pi/4, np.pi/2]
            
            # Gerar cada componente
            for i in range(num_components):
                component = amps[i] * np.sin(2 * np.pi * freqs[i] * t + phases[i])
                self.individual_components.append({
                    'signal': component,
                    'freq': freqs[i],
                    'amp': amps[i],
                    'phase': phases[i]
                })
            
            # Plotar componentes individuais
            self.ax.clear()
            colors = ['red', 'blue', 'green']
            
            for i, comp in enumerate(self.individual_components):
                self.ax.plot(t[:500], comp['signal'][:500], 
                           color=colors[i], linewidth=2,
                           label=f'Comp {i+1}: {comp["freq"]} Hz, A={comp["amp"]:.1f}')
            
            self.ax.set_title('🎲 Passo 1: Componentes Senoidais Individuais', fontsize=14, fontweight='bold')
            self.ax.set_xlabel('Tempo (s)')
            self.ax.set_ylabel('Amplitude')
            self.ax.grid(True, alpha=0.3)
            self.ax.legend()
            self.ax.set_xlim(0, 0.5)  # Mostra apenas os primeiros 0.5s para clareza
            
            self.canvas.draw()
            self._update_progress(1, "Componentes Geradas")
            
            explanation = """
🎲 PASSO 1: COMPONENTES SENOIDAIS

Cada pulsar emite energia em diferentes frequências. Modelamos isso como uma SUPERPOSIÇÃO DE SENOIDES:

📊 COMPONENTES GERADAS:
• Componente 1: 5 Hz (vermelho) - Frequência fundamental
• Componente 2: 15 Hz (azul) - Primeiro harmônico  
• Componente 3: 25 Hz (verde) - Segundo harmônico

🔬 EQUAÇÃO MATEMÁTICA:
x₁(t) = A₁·sin(2πf₁t + φ₁)
x₂(t) = A₂·sin(2πf₂t + φ₂)  
x₃(t) = A₃·sin(2πf₃t + φ₃)

📏 PARÂMETROS:
• Frequência (f): Determina quantos ciclos por segundo
• Amplitude (A): Intensidade do sinal
• Fase (φ): Deslocamento temporal inicial

🎯 CONCEITO CHAVE:
Sinais complexos podem ser decompostos em componentes senoidais simples - base da Análise de Fourier!

Próximo: Vamos somar essas componentes (Princípio da Superposição)
            """
            self.explanation_text.delete(1.0, tk.END)
            self.explanation_text.insert(tk.END, explanation)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no Passo 1: {e}")

    def _step2_superposition(self):
        """Passo 2: Mostrar superposição das componentes"""
        if not self.individual_components:
            messagebox.showwarning("Aviso", "Execute o Passo 1 primeiro!")
            return
            
        try:
            # Criar sinal limpo pela superposição
            t = self.current_time_vector
            self.clean_signal = np.zeros_like(t)
            
            for comp in self.individual_components:
                self.clean_signal += comp['signal']
            
            # Plotar comparação
            self.fig.clear()
            
            # Subplot 1: Componentes individuais
            ax1 = self.fig.add_subplot(2, 1, 1)
            colors = ['red', 'blue', 'green']
            
            for i, comp in enumerate(self.individual_components):
                ax1.plot(t[:500], comp['signal'][:500], 
                        color=colors[i], linewidth=1.5, alpha=0.7,
                        label=f'{comp["freq"]} Hz')
            
            ax1.set_title('Componentes Individuais', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Amplitude')
            ax1.grid(True, alpha=0.3)
            ax1.legend()
            ax1.set_xlim(0, 0.5)
            
            # Subplot 2: Sinal resultante
            ax2 = self.fig.add_subplot(2, 1, 2)
            ax2.plot(t[:500], self.clean_signal[:500], 
                    color='purple', linewidth=2.5,
                    label='Sinal Resultante (Superposição)')
            
            ax2.set_title('➕ Passo 2: Sinal Resultante da Superposição', fontsize=12, fontweight='bold')
            ax2.set_xlabel('Tempo (s)')
            ax2.set_ylabel('Amplitude')
            ax2.grid(True, alpha=0.3)
            ax2.legend()
            ax2.set_xlim(0, 0.5)
            
            self.fig.tight_layout()
            self.canvas.draw()
            self._update_progress(2, "Superposição Aplicada")
            
            explanation = """
➕ PASSO 2: PRINCÍPIO DA SUPERPOSIÇÃO

O sinal final é a SOMA ALGÉBRICA de todas as componentes!

🔬 PRINCÍPIO MATEMÁTICO:
x(t) = x₁(t) + x₂(t) + x₃(t)
x(t) = A₁·sin(2πf₁t + φ₁) + A₂·sin(2πf₂t + φ₂) + A₃·sin(2πf₃t + φ₃)

🎯 CONCEITOS IMPORTANTES:

1️⃣ LINEARIDADE:
A saída é proporcional à entrada - duplicar a amplitude duplica o resultado.

2️⃣ SUPERPOSIÇÃO:
O efeito total é a soma dos efeitos individuais.

3️⃣ INTERFERÊNCIA:
• Construtiva: ondas em fase se somam
• Destrutiva: ondas fora de fase se cancelam

📊 OBSERVE NO GRÁFICO:
• O sinal roxo é complexo mas periódico
• Diferentes frequências criam o padrão único
• A amplitude varia devido à interferência

🌟 APLICAÇÃO REAL:
Pulsares emitem em múltiplas frequências simultaneamente - este é o padrão que detectaríamos no espaço!

Próximo: Adicionar ruído realista
            """
            self.explanation_text.delete(1.0, tk.END)
            self.explanation_text.insert(tk.END, explanation)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no Passo 2: {e}")

    def _step3_add_noise(self):
        """Passo 3: Adicionar ruído e mostrar degradação do sinal"""
        if self.clean_signal is None:
            messagebox.showwarning("Aviso", "Execute os passos anteriores primeiro!")
            return
            
        try:
            # Adicionar ruído
            noise_amplitude = 0.5
            noise = noise_amplitude * np.random.randn(len(self.current_time_vector))
            self.current_noisy_signal = self.clean_signal + noise
            
            # Plotar comparação
            self.fig.clear()
            
            # Subplot 1: Sinal limpo
            ax1 = self.fig.add_subplot(3, 1, 1)
            ax1.plot(self.current_time_vector[:500], self.clean_signal[:500], 
                    color='blue', linewidth=2, label='Sinal Limpo')
            ax1.set_title('Sinal Original (Sem Ruído)', fontsize=11, fontweight='bold')
            ax1.set_ylabel('Amplitude')
            ax1.grid(True, alpha=0.3)
            ax1.legend()
            ax1.set_xlim(0, 0.5)
            
            # Subplot 2: Ruído
            ax2 = self.fig.add_subplot(3, 1, 2)
            ax2.plot(self.current_time_vector[:500], noise[:500], 
                    color='red', linewidth=1, alpha=0.7, label='Ruído Gaussiano')
            ax2.set_title('Ruído Adicionado', fontsize=11, fontweight='bold')
            ax2.set_ylabel('Amplitude')
            ax2.grid(True, alpha=0.3)
            ax2.legend()
            ax2.set_xlim(0, 0.5)
            
            # Subplot 3: Sinal ruidoso
            ax3 = self.fig.add_subplot(3, 1, 3)
            ax3.plot(self.current_time_vector[:500], self.current_noisy_signal[:500], 
                    color='orange', linewidth=1.5, label='Sinal + Ruído')
            ax3.set_title('📡 Passo 3: Sinal Recebido (Com Ruído)', fontsize=11, fontweight='bold')
            ax3.set_xlabel('Tempo (s)')
            ax3.set_ylabel('Amplitude')
            ax3.grid(True, alpha=0.3)
            ax3.legend()
            ax3.set_xlim(0, 0.5)
            
            self.fig.tight_layout()
            self.canvas.draw()
            self._update_progress(3, "Ruído Adicionado")
            
            # Calcular SNR
            signal_power = np.mean(self.clean_signal**2)
            noise_power = np.mean(noise**2)
            snr_db = 10 * np.log10(signal_power / noise_power)
            
            explanation = f"""
📡 PASSO 3: ADIÇÃO DE RUÍDO

Na detecção real de pulsares, o sinal está MUITO fraco e contaminado por ruído!

🔬 TIPOS DE RUÍDO:
• Ruído térmico dos receptores
• Interferência cósmica de fundo  
• Ruído atmosférico
• Interferência de equipamentos

📊 MODELAGEM MATEMÁTICA:
y(t) = x(t) + n(t)

Onde:
• y(t) = sinal recebido
• x(t) = sinal limpo do pulsar
• n(t) = ruído gaussiano branco

📈 CARACTERÍSTICAS DO RUÍDO:
• Distribuição Gaussiana (Normal)
• Média zero: E[n(t)] = 0
• Variância constante: σ² = {noise_amplitude**2:.2f}
• Espectro "branco" (todas as frequências)

📊 SNR CALCULADA: {snr_db:.1f} dB

🎯 DESAFIO:
Como extrair o sinal útil desta "bagunça"?
Resposta: FILTRAGEM DIGITAL!

Próximo: Aplicar filtro passa-baixa
            """
            self.explanation_text.delete(1.0, tk.END)
            self.explanation_text.insert(tk.END, explanation)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no Passo 3: {e}")

    def _step4_filter_signal(self):
        """Passo 4: Aplicar filtro passa-baixa"""
        if self.current_noisy_signal is None:
            messagebox.showwarning("Aviso", "Execute os passos anteriores primeiro!")
            return
            
        try:
            # Aplicar filtro usando a função existente
            from process_signal import process_and_analyze_signal
            results = process_and_analyze_signal(self.current_noisy_signal, self.Fs, 
                                               cutoff_freq=35, filter_order=5)
            
            # Plotar antes e depois da filtragem
            self.fig.clear()
            
            # Subplot 1: Sinal ruidoso
            ax1 = self.fig.add_subplot(2, 1, 1)
            ax1.plot(self.current_time_vector[:500], self.current_noisy_signal[:500], 
                    color='red', linewidth=1, alpha=0.7, label='Sinal Ruidoso')
            ax1.plot(self.current_time_vector[:500], self.clean_signal[:500], 
                    color='blue', linewidth=2, alpha=0.8, label='Sinal Original')
            ax1.set_title('Antes da Filtragem', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Amplitude')
            ax1.grid(True, alpha=0.3)
            ax1.legend()
            ax1.set_xlim(0, 0.5)
            
            # Subplot 2: Sinal filtrado
            ax2 = self.fig.add_subplot(2, 1, 2)
            ax2.plot(results['time_vector'][:500], results['filtered_signal'][:500], 
                    color='green', linewidth=2, label='Sinal Filtrado')
            ax2.plot(self.current_time_vector[:500], self.clean_signal[:500], 
                    color='blue', linewidth=2, alpha=0.5, linestyle='--', label='Original (Referência)')
            ax2.set_title(f'🔽 Passo 4: Após Filtro Passa-Baixa ({results["cutoff_freq"]} Hz)', 
                         fontsize=12, fontweight='bold')
            ax2.set_xlabel('Tempo (s)')
            ax2.set_ylabel('Amplitude')
            ax2.grid(True, alpha=0.3)
            ax2.legend()
            ax2.set_xlim(0, 0.5)
            
            self.fig.tight_layout()
            self.canvas.draw()
            self._update_progress(4, "Filtragem Aplicada")
            
            explanation = f"""
🔽 PASSO 4: FILTRAGEM DIGITAL

O filtro passa-baixa remove frequências altas (ruído) preservando o sinal útil!

🔧 FILTRO BUTTERWORTH:
• Tipo: Passa-baixa
• Ordem: {results["filter_order"]}ª ordem
• Frequência de corte: {results["cutoff_freq"]} Hz
• Resposta: Máximamente plana na banda passante

📊 FUNCIONAMENTO:
• Frequências < 35 Hz: PASSAM (atenuação mínima)
• Frequências > 35 Hz: BLOQUEADAS (atenuação alta)
• Taxa de corte: ~20 dB/década por ordem

🔬 IMPLEMENTAÇÃO:
• Função de transferência H(z)
• Filtragem bidirecional (filtfilt)
• Zero distorção de fase
• Resposta impulsiva finita

⚡ VANTAGENS:
✅ Reduz ruído de alta frequência
✅ Preserva componentes do sinal (5, 15, 25 Hz)
✅ Melhora relação sinal-ruído
✅ Facilita detecção de periodicidade

🎯 TEORIA LTI:
Sistema Linear e Invariante no Tempo
y[n] = Σ h[k] x[n-k] (convolução)

Próximo: Análise espectral com FFT
            """
            self.explanation_text.delete(1.0, tk.END)
            self.explanation_text.insert(tk.END, explanation)
            
            # Salvar resultado para próximo passo
            self.filtered_results = results
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no Passo 4: {e}")

    def _step5_fft_analysis(self):
        """Passo 5: Análise FFT e detecção de periodicidade"""
        if not hasattr(self, 'filtered_results'):
            messagebox.showwarning("Aviso", "Execute os passos anteriores primeiro!")
            return
            
        try:
            results = self.filtered_results
            
            # Plotar análise espectral completa
            self.fig.clear()
            
            # Subplot 1: Sinal no tempo
            ax1 = self.fig.add_subplot(2, 2, 1)
            ax1.plot(results['time_vector'][:500], results['filtered_signal'][:500], 
                    color='green', linewidth=2)
            ax1.set_title('Sinal Filtrado', fontsize=10, fontweight='bold')
            ax1.set_xlabel('Tempo (s)')
            ax1.set_ylabel('Amplitude')
            ax1.grid(True, alpha=0.3)
            ax1.set_xlim(0, 0.5)
            
            # Subplot 2: Espectro original vs filtrado
            ax2 = self.fig.add_subplot(2, 2, 2)
            ax2.semilogy(results['frequencies'], results['power_spectrum_original'], 
                        'r-', alpha=0.7, label='Original')
            ax2.semilogy(results['frequencies'], results['power_spectrum_filtered'], 
                        'g-', linewidth=2, label='Filtrado')
            ax2.axvline(x=results['cutoff_freq'], color='blue', linestyle='--', 
                       label=f'Corte ({results["cutoff_freq"]} Hz)')
            ax2.set_title('Espectros de Potência', fontsize=10, fontweight='bold')
            ax2.set_xlabel('Frequência (Hz)')
            ax2.set_ylabel('Potência (log)')
            ax2.set_xlim(0, 100)
            ax2.grid(True, alpha=0.3)
            ax2.legend(fontsize=8)
            
            # Subplot 3: Zoom nas frequências baixas
            ax3 = self.fig.add_subplot(2, 2, 3)
            ax3.plot(results['frequencies'], results['power_spectrum_filtered'], 
                    'g-', linewidth=2)
            
            # Marcar os picos das componentes originais (5, 15, 25 Hz)
            for comp in self.individual_components:
                freq = comp['freq']
                if freq < len(results['frequencies']):
                    idx = np.argmin(np.abs(results['frequencies'] - freq))
                    ax3.plot(freq, results['power_spectrum_filtered'][idx], 
                            'ro', markersize=8, label=f'{freq} Hz')
            
            # Marcar pico detectado
            if results['detected_peak_freq'] > 0:
                ax3.axvline(x=results['detected_peak_freq'], color='purple', 
                           linestyle='--', linewidth=2,
                           label=f'Detectado: {results["detected_peak_freq"]:.1f} Hz')
            
            ax3.set_title('Detecção de Picos', fontsize=10, fontweight='bold')
            ax3.set_xlabel('Frequência (Hz)')
            ax3.set_ylabel('Potência')
            ax3.set_xlim(0, 50)
            ax3.grid(True, alpha=0.3)
            ax3.legend(fontsize=8)
            
            # Subplot 4: Informações da detecção
            ax4 = self.fig.add_subplot(2, 2, 4)
            ax4.axis('off')
            
            detection_info = f"""📊 RESULTADOS DA DETECÇÃO

🎯 Pico Principal Detectado:
Frequência: {results['detected_peak_freq']:.2f} Hz
Período: {results['detected_period']:.3f} s

🔍 Componentes Originais:
• 5 Hz → Período: 0.200 s
• 15 Hz → Período: 0.067 s  
• 25 Hz → Período: 0.040 s

✅ Status: {"DETECTADO!" if results['detected_peak_freq'] > 0 else "NÃO DETECTADO"}

🌟 Conclusão:
{"O algoritmo identificou com sucesso a periodicidade do pulsar!" if results['detected_peak_freq'] > 0 else "Ajustar parâmetros de detecção."}
            """
            
            ax4.text(0.1, 0.9, detection_info, fontsize=9, 
                    transform=ax4.transAxes, verticalalignment='top',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))
            
            self.fig.suptitle('📊 Passo 5: Análise FFT e Detecção de Periodicidade', 
                             fontsize=14, fontweight='bold')
            self.fig.tight_layout()
            self.canvas.draw()
            self._update_progress(5, "Análise Completa!")
            
            explanation = f"""
📊 PASSO 5: TRANSFORMADA DE FOURIER (FFT)

A FFT revela as frequências presentes no sinal!

🔬 CONCEITOS FUNDAMENTAIS:

1️⃣ TRANSFORMADA DE FOURIER:
X(f) = ∫ x(t) e^(-j2πft) dt
Converte domínio do tempo → frequência

2️⃣ FFT (Fast Fourier Transform):
Algoritmo eficiente: O(N log N)
N = {len(results['frequencies'])} pontos
Resolução: Δf = {self.Fs/len(self.current_noisy_signal):.2f} Hz

3️⃣ ESPECTRO DE POTÊNCIA:
P(f) = |X(f)|²
Mostra energia em cada frequência

🎯 RESULTADOS OBTIDOS:

📈 PICOS DETECTADOS:
• Frequência dominante: {results['detected_peak_freq']:.2f} Hz
• Período correspondente: {results['detected_period']:.3f} s

🔍 INTERPRETAÇÃO:
• Picos em 5, 15, 25 Hz confirmam as componentes originais
• O filtro removeu ruído de alta frequência
• A periodicidade do pulsar foi recuperada!

🌟 APLICAÇÃO REAL:
Em radiotelescópios, este processo detecta pulsares reais no universo, permitindo estudar física extrema e navegação espacial!

🏆 MISSÃO CUMPRIDA!
Você aprendeu todo o pipeline de detecção de pulsares usando processamento digital de sinais!
            """
            self.explanation_text.delete(1.0, tk.END)
            self.explanation_text.insert(tk.END, explanation)
            
            # Mostrar popup de conclusão
            messagebox.showinfo("🎉 Parabéns!", 
                              "Você completou todo o processo de detecção de pulsares!\n\n"
                              f"Período detectado: {results['detected_period']:.3f} segundos\n"
                              f"Frequência: {results['detected_peak_freq']:.2f} Hz\n\n"
                              "Todos os conceitos de Sinais e Sistemas foram aplicados com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no Passo 5: {e}")

    def _reset_all(self):
        """Reset completo da aplicação"""
        self.current_step = 0
        self.current_noisy_signal = None
        self.current_time_vector = None
        self.individual_components = []
        self.clean_signal = None
        
        # Reset botões
        for i, btn in enumerate(self.step_buttons):
            if i == 0:
                btn.configure(state='normal', bg='#3498db')
            else:
                btn.configure(state='disabled', bg='#95a5a6')
        
        # Reset progress
        self.progress_var.set("Passo 0/5: Início")
        self.progress_bar['value'] = 0
        self.status_var.set("Pronto para começar!")
        
        # Reset plot
        self._show_welcome_screen()

    def _clear_plots(self):
        """Método mantido para compatibilidade"""
        pass

    def _generate_and_load_signal(self):
        """Método mantido para compatibilidade"""
        pass

    def _process_signal(self):
        """Método mantido para compatibilidade"""
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = PulsarDetectorApp(root)
    root.mainloop()