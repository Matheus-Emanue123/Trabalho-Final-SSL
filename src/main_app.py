import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

# Importa as funções dos seus outros scripts
from generate_signal import generate_and_save_random_signal
from process_signal import process_and_analyze_signal

class PulsarDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector de Pulsares Simples")
        self.root.geometry("1000x800") # Define um tamanho inicial para a janela

        self.current_noisy_signal = None
        self.current_time_vector = None
        self.Fs = 1000 # Frequência de amostragem padrão (ajuste se mudar no gerador)
        self.duration = 2 # Duração padrão do sinal

        self._create_widgets()

    def _create_widgets(self):
        # --- Frame de Controles ---
        control_frame = ttk.LabelFrame(self.root, text="Controles do Sinal")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Parâmetros de Geração (para o futuro, se quiser interface para eles)
        # Por enquanto, apenas os botões de ação

        generate_button = ttk.Button(control_frame, text="1. Gerar e Carregar Sinal", command=self._generate_and_load_signal)
        generate_button.pack(side=tk.LEFT, padx=5, pady=5)

        process_button = ttk.Button(control_frame, text="2. Processar e Analisar Sinal", command=self._process_signal)
        process_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Label para exibir o período detectado
        self.period_label = ttk.Label(control_frame, text="Período Detectado: N/A")
        self.period_label.pack(side=tk.RIGHT, padx=10, pady=5)

        # --- Frame de Plots ---
        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Configurar Matplotlib para os plots
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(9, 7)) # 3 subplots
        self.fig.suptitle("Análise de Sinal de Pulsar")
        self.fig.tight_layout(rect=[0, 0.03, 1, 0.95]) # Ajusta layout para título

        # Adicionar o canvas do Matplotlib ao Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Adicionar barra de ferramentas do Matplotlib (zoom, pan, etc.)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        self.toolbar.update()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Inicializa os plots vazios ou com dados placeholder
        self._clear_plots()

    def _clear_plots(self):
        self.ax1.clear()
        self.ax1.set_title("Sinal Original (Tempo)")
        self.ax1.set_xlabel("Tempo (s)")
        self.ax1.set_ylabel("Amplitude")
        self.ax1.grid(True)

        self.ax2.clear()
        self.ax2.set_title("Sinal Filtrado (Tempo)")
        self.ax2.set_xlabel("Tempo (s)")
        self.ax2.set_ylabel("Amplitude")
        self.ax2.grid(True)

        self.ax3.clear()
        self.ax3.set_title("Espectro de Potência (FFT)")
        self.ax3.set_xlabel("Frequência (Hz)")
        self.ax3.set_ylabel("Potência")
        self.ax3.grid(True)
        self.canvas.draw_idle()

    def _generate_and_load_signal(self):
        # Aqui você pode adicionar campos de entrada para Fs, duration, noise_amplitude
        # Por enquanto, usa valores fixos ou o default do generate_signal.py
        
        # Gera o sinal usando a função importada
        # Para um projeto final, você pode adicionar a opção de carregar de arquivo também.
        try:
            self.current_noisy_signal, self.current_time_vector = \
                generate_and_save_random_signal(self.Fs, self.duration, noise_amplitude=0.5)
            
            self._clear_plots()
            self.ax1.plot(self.current_time_vector, self.current_noisy_signal)
            self.ax1.set_title('Sinal Original Gerado com Ruído')
            self.canvas.draw_idle()
            self.period_label.config(text="Período Detectado: N/A") # Reseta o label
            messagebox.showinfo("Sucesso", "Sinal gerado e carregado!")
        except Exception as e:
            messagebox.showerror("Erro na Geração", f"Não foi possível gerar o sinal: {e}")
            self.current_noisy_signal = None
            self.current_time_vector = None


    def _process_signal(self):
        if self.current_noisy_signal is None:
            messagebox.showwarning("Aviso", "Por favor, gere e carregue um sinal primeiro!")
            return

        # Parâmetros para o filtro (pode adicionar controles na GUI para eles depois)
        # Por enquanto, usa valores fixos ou os defaults da função process_and_analyze_signal
        filter_cutoff_freq = 55 # Hz
        filter_order = 5

        try:
            results = process_and_analyze_signal(
                self.current_noisy_signal, self.Fs,
                cutoff_freq=filter_cutoff_freq, filter_order=filter_order
            )

            # Limpa e plota o sinal filtrado
            self.ax2.clear()
            self.ax2.plot(results['time_vector'], results['filtered_signal'], color='orange')
            self.ax2.set_title(f'Sinal Filtrado (Passa-Baixa, Corte: {results["cutoff_freq"]} Hz)')
            self.ax2.set_xlabel("Tempo (s)")
            self.ax2.set_ylabel("Amplitude")
            self.ax2.grid(True)

            # Limpa e plota o espectro de potência
            self.ax3.clear()
            self.ax3.plot(results['frequencies'], results['power_spectrum_original'], label='Espectro Original (Ruidoso)', alpha=0.7)
            self.ax3.plot(results['frequencies'], results['power_spectrum_filtered'], label='Espectro Filtrado', color='orange')
            self.ax3.axvline(x=results['detected_peak_freq'], color='g', linestyle='--', label=f'Pico Detectado: {results["detected_peak_freq"]:.2f} Hz')
            self.ax3.axvline(x=results['cutoff_freq'], color='r', linestyle='--', label=f'Corte do Filtro ({results["cutoff_freq"]} Hz)')
            
            self.ax3.set_title('Espectro de Potência (FFT)')
            self.ax3.set_xlabel('Frequência (Hz)')
            self.ax3.set_ylabel('Potência')
            self.ax3.set_xlim(0, self.Fs / 2) # Garante que o espectro vá até a frequência de Nyquist
            self.ax3.grid(True)
            self.ax3.legend()

            self.canvas.draw_idle() # Redesenha o canvas

            # Atualiza o label do período
            if results['detected_period'] != np.inf:
                self.period_label.config(text=f"Período Detectado: {results['detected_period']:.4f} s ({results['detected_peak_freq']:.4f} Hz)")
            else:
                self.period_label.config(text="Período Detectado: Não detectado ou muito baixo")

            messagebox.showinfo("Sucesso", "Processamento e análise concluídos!")

        except Exception as e:
            messagebox.showerror("Erro no Processamento", f"Ocorreu um erro durante o processamento: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PulsarDetectorApp(root)
    root.mainloop()