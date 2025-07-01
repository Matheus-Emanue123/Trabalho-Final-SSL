import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from scipy.fft import fft, fftfreq

def process_and_analyze_signal(input_signal, Fs, cutoff_freq=55, filter_order=5):
    """
    Aplica filtro passa-baixa, realiza FFT e tenta detectar um pico de frequência.
    Retorna o sinal filtrado, frequências, espectros e o período detectado.
    """
    N = len(input_signal)
    T = 1 / Fs
    t = np.arange(0, N * T, T) # Vetor de tempo para plotagem

    # --- 1. Filtragem Passa-Baixa ---
    Wn = cutoff_freq / (Fs / 2) # Frequência de corte normalizada
    b, a = butter(filter_order, Wn, btype='low', analog=False)
    filtered_signal = filtfilt(b, a, input_signal)

    # --- 2. Análise Espectral (FFT) ---
    yf_original = fft(input_signal)
    power_spectrum_original = np.abs(yf_original[0:N//2])**2

    yf_filtered = fft(filtered_signal)
    xf = fftfreq(N, T)[:N//2] # Frequências correspondentes
    power_spectrum_filtered = np.abs(yf_filtered[0:N//2])**2

    # --- 3. Detecção do Pulsar (Pico na FFT) ---
    min_freq_for_pulsar = 0.5 # Hz (ajuste se souber a faixa do seu pulsar sintético)
    max_freq_for_pulsar = Fs/2 - 5 # Hz (ajuste)

    idx_min_freq = np.argmin(np.abs(xf - min_freq_for_pulsar))
    idx_max_freq = np.argmin(np.abs(xf - max_freq_for_pulsar))

    # Garante que a faixa seja válida
    if idx_min_freq >= idx_max_freq:
        peak_freq = 0.0
        detected_period = np.inf
        print("Aviso: Faixa de frequência para detecção de pulsar inválida ou muito estreita.")
    else:
        peak_index_in_range = np.argmax(power_spectrum_filtered[idx_min_freq : idx_max_freq])
        peak_freq = xf[idx_min_freq + peak_index_in_range]
        detected_period = 1 / peak_freq if peak_freq > 0 else np.inf
    
    return {
        'time_vector': t,
        'noisy_signal': input_signal,
        'filtered_signal': filtered_signal,
        'frequencies': xf,
        'power_spectrum_original': power_spectrum_original,
        'power_spectrum_filtered': power_spectrum_filtered,
        'detected_peak_freq': peak_freq,
        'detected_period': detected_period,
        'cutoff_freq': cutoff_freq,
        'filter_order': filter_order
    }

if __name__ == '__main__':
    # Este bloco só executa se o script for rodado diretamente, não quando importado
    # Exemplo de uso direto (para testar a função):
    from generate_signal import generate_and_save_random_signal

    Fs_test = 1000
    duration_test = 2
    noise_amp_test = 0.5
    
    test_noisy_signal, test_time_vec = generate_and_save_random_signal(Fs_test, duration_test, noise_amp_test)
    
    results = process_and_analyze_signal(test_noisy_signal, Fs_test)
    
    # Plotar os resultados (similar ao seu script original, mas usando 'results')
    plt.figure(figsize=(12, 10))

    plt.subplot(3, 1, 1)
    plt.plot(results['time_vector'], results['noisy_signal'])
    plt.title('Sinal Original Sintético com Ruído')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(results['time_vector'], results['filtered_signal'], color='orange')
    plt.title(f'Sinal Filtrado (Passa-Baixa, Corte: {results["cutoff_freq"]} Hz)')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(results['frequencies'], results['power_spectrum_original'], label='Espectro Original (Ruidoso)', alpha=0.7)
    plt.plot(results['frequencies'], results['power_spectrum_filtered'], label='Espectro Filtrado', color='orange')
    plt.axvline(x=results['detected_peak_freq'], color='g', linestyle='--', label=f'Pico Detectado: {results["detected_peak_freq"]:.2f} Hz')
    plt.axvline(x=results['cutoff_freq'], color='r', linestyle='--', label=f'Corte do Filtro ({results["cutoff_freq"]} Hz)')
    plt.title('Espectro de Potência (FFT)')
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Potência')
    plt.xlim(0, Fs_test/2)
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

    print(f"\n--- Detecção de Pulsar ---")
    print(f"Frequência do Pico Detectado: {results['detected_peak_freq']:.4f} Hz")
    print(f"Período de Pulsação Detectado: {results['detected_period']:.4f} segundos")