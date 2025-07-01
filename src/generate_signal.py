import numpy as np
import matplotlib.pyplot as plt

def generate_and_save_random_signal(Fs, duration, noise_amplitude):
    """
    Gera um sinal sintético com componentes senoidais aleatórias e ruído.
    Retorna o sinal ruidoso e o vetor de tempo.
    """
    T = 1 / Fs
    t = np.arange(0, duration, T)

    num_components = np.random.randint(2, 6) # Número aleatório de componentes senoidais
    signal = np.zeros_like(t)
    for _ in range(num_components):
        freq = np.random.uniform(1, 50) # Frequência entre 1 e 50 Hz
        amp = np.random.uniform(0.5, 2.0) # Amplitude entre 0.5 e 2.0
        phase = np.random.uniform(0, 2 * np.pi) # Fase aleatória
        signal += amp * np.sin(2 * np.pi * freq * t + phase)

    noise = noise_amplitude * np.random.randn(len(t))
    noisy_signal = signal + noise

    # Opcional: Salvar o sinal. Para a GUI, podemos retornar diretamente.
    # np.savetxt('random_signal_noisy.txt', noisy_signal)
    
    return noisy_signal, t

if __name__ == '__main__':
    # Este bloco só executa se o script for rodado diretamente, não quando importado
    Fs_default = 1000
    duration_default = 2
    noise_amp_default = 0.5

    noisy_sig, time_vec = generate_and_save_random_signal(Fs_default, duration_default, noise_amp_default)

    plt.figure(figsize=(10, 4))
    plt.plot(time_vec, noisy_sig)
    plt.title('Sinal Aleatório Sintético com Ruído (Gerador Direto)')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()

    np.savetxt('random_signal_noisy.txt', noisy_sig) # Ainda salvamos para o caso de querer carregar de arquivo