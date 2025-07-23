import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

from generate_signal import generate_and_save_random_signal
from process_signal import process_and_analyze_signal

class PulsarDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌟 Detector de Pulsares Educativo - Sinais e Sistemas Lineares")
        self.root.geometry("1500x950")
        
        # Esquema de cores moderno e tecnológico
        self.colors = {
            'bg_dark': '#1a1a2e',      # Azul escuro espacial
            'bg_medium': '#16213e',     # Azul médio
            'bg_light': '#0f3460',      # Azul claro
            'accent_cyan': '#00d4ff',   # Ciano brilhante
            'accent_purple': '#9d4edd', # Roxo tecnológico
            'accent_green': '#00f5ff',  # Verde neon
            'text_primary': '#ffffff',  # Branco puro
            'text_secondary': '#b0bec5', # Cinza claro
            'success': '#4caf50',       # Verde sucesso
            'warning': '#ff9800',       # Laranja aviso
            'error': '#f44336',         # Vermelho erro
            'button_primary': '#0088cc', # Azul botão
            'button_hover': '#00a6e6'   # Azul hover
        }
        
        self.root.configure(bg=self.colors['bg_dark'])
        
        # Fontes modernas e tecnológicas
        self.fonts = {
            'title': ('Consolas', 18, 'bold'),        # Fonte monospace tecnológica
            'subtitle': ('Segoe UI', 12, 'normal'),   # Fonte moderna
            'button': ('Segoe UI', 10, 'bold'),       # Botões
            'text': ('Segoe UI', 9, 'normal'),        # Texto geral
            'code': ('Consolas', 9, 'normal'),        # Código/dados
            'header': ('Segoe UI', 14, 'bold')        # Cabeçalhos
        }

        # Variáveis de estado
        self.current_noisy_signal = None
        self.current_time_vector = None
        self.individual_components = []
        self.clean_signal = None
        self.Fs = 1000
        self.duration = 2
        self.current_step = 0
        self.total_steps = 5
        self.random_mode = False  # Novo: controla modo aleatório vs educativo
        self.signal_info = {}  # Novo: armazena informações do sinal gerado

        # Configurações visuais
        try:
            plt.style.use('dark_background')  # Tema escuro para gráficos
        except:
            try:
                plt.style.use('seaborn-v0_8-dark')
            except:
                try:
                    plt.style.use('seaborn-dark')
                except:
                    plt.style.use('default')
        
        # Configurar matplotlib para tema escuro
        plt.rcParams.update({
            'figure.facecolor': self.colors['bg_dark'],
            'axes.facecolor': self.colors['bg_medium'],
            'axes.edgecolor': self.colors['accent_cyan'],
            'axes.labelcolor': self.colors['text_primary'],
            'xtick.color': self.colors['text_secondary'],
            'ytick.color': self.colors['text_secondary'],
            'text.color': self.colors['text_primary'],
            'grid.color': self.colors['text_secondary'],
            'grid.alpha': 0.3
        })
        
        self._create_widgets()

    def _create_widgets(self):
        # === PAINEL SUPERIOR: TÍTULO E PROGRESSO ===
        header_frame = tk.Frame(self.root, bg=self.colors['bg_medium'], height=100)
        header_frame.pack(side=tk.TOP, fill=tk.X)
        header_frame.pack_propagate(False)

        # Gradiente visual com canvas
        header_canvas = tk.Canvas(header_frame, bg=self.colors['bg_medium'], height=100, highlightthickness=0)
        header_canvas.pack(fill=tk.BOTH)
        
        # Criar gradiente simulado
        for i in range(100):
            color_intensity = int(26 + i * 0.3)  # Gradiente sutil
            color = f"#{color_intensity:02x}{color_intensity+10:02x}{color_intensity+30:02x}"
            header_canvas.create_line(0, i, 2000, i, fill=color, width=1)

        title_label = tk.Label(header_frame, text="🌟 DETECTOR DE PULSARES EDUCATIVO", 
                              font=self.fonts['title'], fg=self.colors['accent_cyan'], 
                              bg=self.colors['bg_medium'])
        title_label.place(relx=0.5, rely=0.35, anchor='center')

        subtitle_label = tk.Label(header_frame, text="⚡ Processamento Digital de Sinais Aplicado à Astrofísica ⚡", 
                                 font=self.fonts['subtitle'], fg=self.colors['text_secondary'], 
                                 bg=self.colors['bg_medium'])
        subtitle_label.place(relx=0.5, rely=0.65, anchor='center')

        # === PAINEL LATERAL: CONTROLES E EXPLICAÇÕES ===
        self.sidebar = tk.Frame(self.root, bg=self.colors['bg_light'], width=380)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Progresso dos passos
        progress_frame = tk.Frame(self.sidebar, bg=self.colors['bg_light'])
        progress_frame.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(progress_frame, text="� PROGRESSO DA MISSÃO", 
                font=self.fonts['header'], fg=self.colors['accent_green'], 
                bg=self.colors['bg_light']).pack()

        self.progress_var = tk.StringVar(value="Passo 0/5: Inicializando Sistema")
        self.progress_label = tk.Label(progress_frame, textvariable=self.progress_var,
                                      font=self.fonts['text'], fg=self.colors['text_primary'], 
                                      bg=self.colors['bg_light'])
        self.progress_label.pack(pady=8)

        # Barra de progresso customizada
        self.progress_bar = ttk.Progressbar(progress_frame, length=320, mode='determinate',
                                           style='TProgressbar')
        self.progress_bar.pack(pady=5)

        # Botões de controle com estilo tecnológico
        button_frame = tk.Frame(self.sidebar, bg=self.colors['bg_light'])
        button_frame.pack(fill=tk.X, padx=15, pady=10)

        self.step_buttons = []
        steps = [
            ("🔬 1. Gerar Componentes", self._step1_generate_components),
            ("⚡ 2. Superposição", self._step2_superposition),
            ("📡 3. Adicionar Ruído", self._step3_add_noise),
            ("� 4. Filtrar Sinal", self._step4_filter_signal),
            ("� 5. Análise FFT", self._step5_fft_analysis)
        ]

        for i, (text, command) in enumerate(steps):
            btn = tk.Button(button_frame, text=text, command=command,
                           font=self.fonts['button'], bg=self.colors['button_primary'], 
                           fg=self.colors['text_primary'], relief=tk.FLAT, bd=0, 
                           padx=15, pady=8, cursor='hand2')
            btn.pack(fill=tk.X, pady=3)
            
            # Efeitos hover
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.colors['button_hover']))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.colors['button_primary'] if b['state'] == 'normal' else '#555'))
            
            btn.configure(state='disabled' if i > 0 else 'normal')
            if i > 0:
                btn.configure(bg='#555')
            self.step_buttons.append(btn)

        # Reset button com destaque
        reset_btn = tk.Button(button_frame, text="🔄 REINICIALIZAR SISTEMA", command=self._reset_all,
                             font=self.fonts['button'], bg=self.colors['error'], 
                             fg=self.colors['text_primary'], relief=tk.FLAT, bd=0, 
                             padx=15, pady=8, cursor='hand2')
        reset_btn.pack(fill=tk.X, pady=8)
        
        # Hover effect para reset
        reset_btn.bind("<Enter>", lambda e: reset_btn.configure(bg='#d32f2f'))
        reset_btn.bind("<Leave>", lambda e: reset_btn.configure(bg=self.colors['error']))

        # Modo de operação com estilo futurístico
        mode_frame = tk.LabelFrame(self.sidebar, text="� MODO DE OPERAÇÃO", 
                                  font=self.fonts['button'], fg=self.colors['accent_purple'],
                                  bg=self.colors['bg_light'], labelanchor='n')
        mode_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.mode_var = tk.StringVar(value="educativo")
        
        mode_edu = tk.Radiobutton(mode_frame, text="🎓 Educativo (Demonstração)", 
                                 variable=self.mode_var, value="educativo", 
                                 bg=self.colors['bg_light'], fg=self.colors['text_primary'], 
                                 selectcolor=self.colors['accent_cyan'], 
                                 font=self.fonts['text'], command=self._on_mode_change)
        mode_edu.pack(anchor='w', padx=10, pady=5)
        
        mode_random = tk.Radiobutton(mode_frame, text="🎲 Aleatório (Casos Reais)", 
                                    variable=self.mode_var, value="aleatorio",
                                    bg=self.colors['bg_light'], fg=self.colors['text_primary'],
                                    selectcolor=self.colors['accent_cyan'], 
                                    font=self.fonts['text'], command=self._on_mode_change)
        mode_random.pack(anchor='w', padx=10, pady=5)

        # Área de explicações com estilo high-tech
        explanation_frame = tk.LabelFrame(self.sidebar, text="🧠 BANCO DE CONHECIMENTO", 
                                         font=self.fonts['button'], fg=self.colors['accent_green'], 
                                         bg=self.colors['bg_light'], labelanchor='n')
        explanation_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.explanation_text = scrolledtext.ScrolledText(explanation_frame, 
                                                         wrap=tk.WORD, width=45, height=18,
                                                         font=self.fonts['text'], 
                                                         bg=self.colors['bg_dark'], 
                                                         fg=self.colors['text_primary'],
                                                         insertbackground=self.colors['accent_cyan'],
                                                         selectbackground=self.colors['accent_purple'])
        self.explanation_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # === ÁREA PRINCIPAL: GRÁFICOS ===
        self.plot_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Configuração matplotlib com tema escuro
        self.fig, self.ax = plt.subplots(1, 1, figsize=(12, 7), 
                                        facecolor=self.colors['bg_dark'])
        self.ax.set_facecolor(self.colors['bg_medium'])
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas_widget.configure(bg=self.colors['bg_dark'])

        # Toolbar com fundo escuro
        toolbar_frame = tk.Frame(self.plot_frame, bg=self.colors['bg_dark'])
        toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()
        self.toolbar.configure(bg=self.colors['bg_dark'])

        # Status bar com estilo futurístico
        status_frame = tk.Frame(self.root, bg=self.colors['bg_medium'], height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar(value="🚀 Sistema Inicializado | Pronto para Detecção de Pulsares")
        status_bar = tk.Label(status_frame, textvariable=self.status_var, 
                             relief=tk.FLAT, anchor=tk.W, font=self.fonts['text'],
                             bg=self.colors['bg_medium'], fg=self.colors['text_secondary'])
        status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=5)
        
        # Indicador de status
        self.status_indicator = tk.Label(status_frame, text="●", font=('Arial', 16),
                                        fg=self.colors['success'], bg=self.colors['bg_medium'])
        self.status_indicator.pack(side=tk.RIGHT, padx=10)

        self._show_welcome_screen()

    def _on_mode_change(self):
        """Callback para mudança de modo"""
        self.random_mode = (self.mode_var.get() == "aleatorio")
        if self.current_step > 0:
            self._reset_all()  # Reset se já começou

    def _show_welcome_screen(self):
        """Tela inicial com explicação sobre pulsares"""
        self.ax.clear()
        self.ax.set_facecolor(self.colors['bg_dark'])
        
        # Criar um "display" futurístico
        self.ax.text(0.5, 0.85, "🌟 DETECTOR DE PULSARES v2.0", 
                    ha='center', va='center', fontsize=24, fontweight='bold',
                    color=self.colors['accent_cyan'], transform=self.ax.transAxes)
        
        self.ax.text(0.5, 0.75, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 
                    ha='center', va='center', fontsize=12,
                    color=self.colors['accent_purple'], transform=self.ax.transAxes)
        
        self.ax.text(0.5, 0.65, "Sistema de Processamento Digital de Sinais", 
                    ha='center', va='center', fontsize=16, style='italic',
                    color=self.colors['text_secondary'], transform=self.ax.transAxes)
        
        self.ax.text(0.5, 0.55, "Aplicado à Detecção de Estrelas de Nêutrons", 
                    ha='center', va='center', fontsize=16, style='italic',
                    color=self.colors['text_secondary'], transform=self.ax.transAxes)
        
        # Informações técnicas
        self.ax.text(0.5, 0.4, "⚡ ESPECIFICAÇÕES TÉCNICAS ⚡", 
                    ha='center', va='center', fontsize=14, fontweight='bold',
                    color=self.colors['accent_green'], transform=self.ax.transAxes)
        
        specs_text = """🔬 Processamento: FFT de alta resolução
📡 Filtragem: Butterworth digital adaptativo
🎯 Detecção: Análise espectral automática
🚀 Interface: Modo educativo + casos reais"""
        
        self.ax.text(0.5, 0.25, specs_text, 
                    ha='center', va='center', fontsize=12,
                    color=self.colors['text_primary'], transform=self.ax.transAxes,
                    bbox=dict(boxstyle="round,pad=0.5", facecolor=self.colors['bg_medium'], 
                             edgecolor=self.colors['accent_cyan'], alpha=0.8))
        
        self.ax.text(0.5, 0.08, "► INICIAR SEQUÊNCIA DE DETECÇÃO ◄", 
                    ha='center', va='center', fontsize=16, fontweight='bold',
                    color=self.colors['warning'], transform=self.ax.transAxes,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor=self.colors['bg_light'], 
                             edgecolor=self.colors['warning'], alpha=0.9))
        
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.axis('off')
        
        # Adicionar grade sutil de fundo
        for i in range(20):
            alpha = 0.05
            self.ax.axhline(y=i/20, color=self.colors['accent_cyan'], alpha=alpha, linewidth=0.5)
            self.ax.axvline(x=i/20, color=self.colors['accent_cyan'], alpha=alpha, linewidth=0.5)
        
        self.canvas.draw()
        
        welcome_text = f"""
🌟 DETECTOR DE PULSARES v2.0

INICIALIZANDO SISTEMA...
████████████████████████ 100%

🎯 MISSÃO: Detectar periodicidade em sinais cósmicos
📊 MÉTODO: Processamento Digital de Sinais
🔬 ALGORITMOS: FFT, Filtragem Butterworth, Análise Espectral

═══════════════════════════════════════════════════

🧠 OBJETIVOS DE APRENDIZADO:
• Síntese e superposição de sinais
• Teorema de amostragem de Nyquist  
• Filtragem digital passa-baixa
• Análise espectral com FFT
• Detecção de periodicidade em ruído

📚 CONCEITOS FUNDAMENTAIS:
• Sistemas Lineares Invariantes no Tempo (LTI)
• Transformada de Fourier Discreta (DFT)
• Processamento digital de ruído
• Relação sinal-ruído (SNR)

🎮 MODOS DE OPERAÇÃO:
• EDUCATIVO: Demonstração com parâmetros fixos
• ALEATÓRIO: Casos reais (pode não haver pulsar!)

⚠️  NOTA IMPORTANTE:
No modo aleatório, nem sempre há pulsar detectável!
Isso simula condições reais de observação astronômica.

🚀 READY FOR LAUNCH! Clique no primeiro passo...
        """
        self.explanation_text.delete(1.0, tk.END)
        self.explanation_text.insert(tk.END, welcome_text)

    def _update_progress(self, step, description):
        """Atualiza a barra de progresso e status"""
        self.current_step = step
        self.progress_var.set(f"Passo {step}/{self.total_steps}: {description}")
        self.progress_bar['value'] = (step / self.total_steps) * 100
        self.status_var.set(f"🔄 Processando: {description} | Sistema Operacional")
        
        # Atualizar indicador de status
        if step < self.total_steps:
            self.status_indicator.configure(fg=self.colors['warning'])  # Amarelo durante processamento
        else:
            self.status_indicator.configure(fg=self.colors['success'])  # Verde quando completo
        
        # Habilita o próximo botão com cores tecnológicas
        for i, btn in enumerate(self.step_buttons):
            if i <= step:
                if i < step:
                    btn.configure(state='normal', bg=self.colors['success'])  # Verde para concluído
                else:
                    btn.configure(state='normal', bg=self.colors['button_primary'])  # Azul para atual
            else:
                btn.configure(state='disabled', bg='#555')  # Cinza para desabilitado

    def _step1_generate_components(self):
        """Passo 1: Gerar e mostrar componentes senoidais individuais"""
        try:
            # Gerar componentes individuais
            T = 1 / self.Fs
            t = np.arange(0, self.duration, T)
            self.current_time_vector = t
            
            if self.random_mode:
                # Modo aleatório: usar geração aleatória
                from generate_signal import generate_and_save_random_signal
                _, _, self.signal_info = generate_and_save_random_signal(
                    self.Fs, self.duration, 0.5, force_random=True)
                
                # Construir componentes baseados no sinal_info
                self.individual_components = []
                if self.signal_info['num_components'] > 0:
                    for i in range(self.signal_info['num_components']):
                        component = self.signal_info['amplitudes'][i] * np.sin(
                            2 * np.pi * self.signal_info['frequencies'][i] * t + 
                            self.signal_info['phases'][i])
                        self.individual_components.append({
                            'signal': component,
                            'freq': self.signal_info['frequencies'][i],
                            'amp': self.signal_info['amplitudes'][i],
                            'phase': self.signal_info['phases'][i]
                        })
            else:
                # Modo educativo: parâmetros fixos
                np.random.seed(42)  # Para resultados reproduzíveis
                self.individual_components = []
                freqs = [5, 15, 25]  # Frequências bem definidas para visualização
                amps = [1.5, 1.0, 0.8]
                phases = [0, np.pi/4, np.pi/2]
                
                self.signal_info = {
                    'frequencies': freqs,
                    'amplitudes': amps,
                    'phases': phases,
                    'num_components': 3,
                    'signal_type': 'educational'
                }
                
                # Gerar cada componente
                for i in range(3):
                    component = amps[i] * np.sin(2 * np.pi * freqs[i] * t + phases[i])
                    self.individual_components.append({
                        'signal': component,
                        'freq': freqs[i],
                        'amp': amps[i],
                        'phase': phases[i]
                    })
            
            # Plotar componentes individuais
            self.ax.clear()
            
            if len(self.individual_components) == 0:
                # Caso especial: apenas ruído
                self.ax.text(0.5, 0.5, "🔍 SINAL DETECTADO: APENAS RUÍDO\n\n"
                           "Este é um caso realista onde não há\npulsar detectável no sinal!\n\n"
                           "Prossiga para ver como o sistema\nlida com a ausência de periodicidade.",
                           ha='center', va='center', fontsize=14,
                           transform=self.ax.transAxes,
                           bbox=dict(boxstyle="round,pad=0.3", facecolor="orange", alpha=0.8))
                self.ax.set_xlim(0, 1)
                self.ax.set_ylim(0, 1)
                self.ax.axis('off')
            else:
                colors = ['red', 'blue', 'green', 'purple', 'orange']
                for i, comp in enumerate(self.individual_components):
                    color = colors[i % len(colors)]
                    self.ax.plot(t[:500], comp['signal'][:500], 
                               color=color, linewidth=2,
                               label=f'Comp {i+1}: {comp["freq"]:.1f} Hz, A={comp["amp"]:.1f}')
                
                self.ax.set_title('🎲 Passo 1: Componentes Senoidais Individuais', 
                                fontsize=14, fontweight='bold')
                self.ax.set_xlabel('Tempo (s)')
                self.ax.set_ylabel('Amplitude')
                self.ax.grid(True, alpha=0.3)
                self.ax.legend()
                self.ax.set_xlim(0, 0.5)  # Mostra apenas os primeiros 0.5s para clareza
            
            self.canvas.draw()
            self._update_progress(1, "Componentes Geradas")
            
            # Gerar texto explicativo baseado no tipo de sinal
            if len(self.individual_components) == 0:
                explanation = """
🎲 PASSO 1: SINAL SEM COMPONENTES PERIÓDICAS

⚠️ CASO REALISTA DETECTADO!
Este sinal representa uma situação comum na astronomia onde apenas RUÍDO é captado.

📊 CARACTERÍSTICAS:
• Número de componentes: 0
• Tipo de sinal: Apenas ruído
• Periodicidade: Ausente

🔬 CENÁRIOS REAIS:
• Pulsar muito distante (sinal fraco)
• Direcionamento incorreto da antena
• Interferência dominante
• Pulsar "jovem" ainda instável

🎯 APRENDIZADO:
Nem sempre detectamos pulsares! O processamento deve ser robusto para identificar quando NÃO há sinal útil.

Próximo: Vamos ver como isso afeta a análise...
                """
            else:
                signal_type = self.signal_info.get('signal_type', 'unknown')
                mode_text = "EDUCATIVO" if not self.random_mode else "ALEATÓRIO"
                
                explanation = f"""
🎲 PASSO 1: COMPONENTES SENOIDAIS ({mode_text})

Cada pulsar emite energia em diferentes frequências. Modelamos isso como uma SUPERPOSIÇÃO DE SENOIDES:

📊 COMPONENTES GERADAS: {len(self.individual_components)}
"""
                for i, comp in enumerate(self.individual_components):
                    explanation += f"• Componente {i+1}: {comp['freq']:.1f} Hz (Amplitude: {comp['amp']:.1f})\n"

                if signal_type == 'irregular':
                    explanation += "\n⚠️ SINAL IRREGULAR DETECTADO!"
                    explanation += "\nEste sinal tem frequências próximas que podem causar interferência (batimento)."
                
                explanation += """

🔬 EQUAÇÃO MATEMÁTICA:
x(t) = Σ Aᵢ·sin(2πfᵢt + φᵢ)

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
            ax1.set_facecolor(self.colors['bg_medium'])
            
            if len(self.individual_components) > 0:
                colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57']
                
                for i, comp in enumerate(self.individual_components):
                    color = colors[i % len(colors)]
                    ax1.plot(t[:500], comp['signal'][:500], 
                            color=color, linewidth=2, alpha=0.8,
                            label=f'{comp["freq"]:.1f} Hz')
                
                ax1.set_title('Componentes Individuais', fontsize=12, fontweight='bold',
                             color=self.colors['text_primary'])
                ax1.set_ylabel('Amplitude', color=self.colors['text_primary'])
                ax1.grid(True, alpha=0.3, color=self.colors['text_secondary'])
                ax1.legend()
                ax1.set_xlim(0, 0.5)
                ax1.tick_params(colors=self.colors['text_secondary'])
            
            # Subplot 2: Sinal resultante
            ax2 = self.fig.add_subplot(2, 1, 2)
            ax2.set_facecolor(self.colors['bg_medium'])
            
            if len(self.individual_components) > 0:
                ax2.plot(t[:500], self.clean_signal[:500], 
                        color=self.colors['accent_purple'], linewidth=3,
                        label='Sinal Resultante (Superposição)')
                
                ax2.set_title('⚡ Passo 2: Sinal Resultante da Superposição', 
                             fontsize=12, fontweight='bold', color=self.colors['text_primary'])
                ax2.set_xlabel('Tempo (s)', color=self.colors['text_primary'])
                ax2.set_ylabel('Amplitude', color=self.colors['text_primary'])
                ax2.grid(True, alpha=0.3, color=self.colors['text_secondary'])
                ax2.legend()
                ax2.set_xlim(0, 0.5)
                ax2.tick_params(colors=self.colors['text_secondary'])
            else:
                # Caso de apenas ruído
                ax2.text(0.5, 0.5, "⚠️ SINAL NULO\n\nNenhuma componente detectada.\nApenas ruído será adicionado no próximo passo.",
                        ha='center', va='center', fontsize=14,
                        color=self.colors['warning'], transform=ax2.transAxes,
                        bbox=dict(boxstyle="round,pad=0.3", facecolor=self.colors['bg_light'], alpha=0.8))
                ax2.set_xlim(0, 1)
                ax2.set_ylim(0, 1)
                ax2.axis('off')
                # Criar sinal zero para próximos passos
                self.clean_signal = np.zeros_like(t)
            
            self.fig.tight_layout()
            self.canvas.draw()
            self._update_progress(2, "Superposição Aplicada")
            
            # Explanation baseada no número de componentes
            if len(self.individual_components) == 0:
                explanation = """
⚡ PASSO 2: SUPERPOSIÇÃO (CASO ESPECIAL)

⚠️ SINAL SEM COMPONENTES PERIÓDICAS

Como não há componentes para somar, o sinal resultante é ZERO (apenas ruído será adicionado posteriormente).

🔬 IMPLICAÇÕES MATEMÁTICAS:
x(t) = 0  (sinal nulo)

🎯 CENÁRIO REALISTA:
• Pulsar fora do campo de visão
• Sinal abaixo do limiar de detecção
• Apenas ruído de fundo presente
• Falso alarme ou observação negativa

📊 PRÓXIMOS PASSOS:
O sistema continuará o processamento apenas com ruído, demonstrando como algoritmos lidam com ausência de sinal.

Próximo: Adicionar ruído ao sinal nulo
                """
            else:
                explanation = f"""
⚡ PASSO 2: PRINCÍPIO DA SUPERPOSIÇÃO

O sinal final é a SOMA ALGÉBRICA de todas as componentes!

🔬 PRINCÍPIO MATEMÁTICO:
x(t) = Σ xᵢ(t) = {' + '.join([f'x{i+1}(t)' for i in range(len(self.individual_components))])}

onde cada xᵢ(t) = Aᵢ·sin(2πfᵢt + φᵢ)

🎯 CONCEITOS FUNDAMENTAIS:

1️⃣ LINEARIDADE:
A saída é proporcional à entrada - duplicar a amplitude duplica o resultado.

2️⃣ SUPERPOSIÇÃO:
O efeito total é a soma dos efeitos individuais. Esta é a base dos sistemas LTI!

3️⃣ INTERFERÊNCIA:
• Construtiva: ondas em fase se somam (amplitude aumenta)
• Destrutiva: ondas fora de fase se cancelam (amplitude diminui)

📊 OBSERVE NO GRÁFICO:
• O sinal resultante (roxo) é complexo mas determinístico
• Diferentes frequências criam padrões únicos
• A amplitude varia devido à interferência entre componentes

🌟 APLICAÇÃO REAL:
Pulsares emitem em múltiplas frequências simultaneamente - este é o padrão característico que detectaríamos no espaço!

🔍 ANÁLISE MATEMÁTICA:
Com {len(self.individual_components)} componentes, o sinal tem periodicidade complexa determinada pela combinação das frequências fundamentais.

Próximo: Adicionar ruído realista para simular condições de observação
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
        self.signal_info = {}
        
        # Limpar resultados filtrados se existirem
        if hasattr(self, 'filtered_results'):
            delattr(self, 'filtered_results')
        
        # Reset botões - APENAS o primeiro deve estar habilitado
        for i, btn in enumerate(self.step_buttons):
            if i == 0:
                btn.configure(state='normal', bg=self.colors['button_primary'])
            else:
                btn.configure(state='disabled', bg='#555')
        
        # Reset progress
        self.progress_var.set("Passo 0/5: Sistema Reinicializado")
        self.progress_bar['value'] = 0
        self.status_var.set("🚀 Sistema Reinicializado | Pronto para Nova Detecção")
        self.status_indicator.configure(fg=self.colors['success'])
        
        # Reset plot - limpar completamente e mostrar tela inicial
        self.fig.clear()
        self.ax = self.fig.add_subplot(1, 1, 1)
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