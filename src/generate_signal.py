import numpy as np
import matplotlib.pyplot as plt

def generate_and_save_random_signal(Fs, duration, noise_amplitude, force_random=False):
    """
    Gera um sinal sintético com componentes senoidais aleatórias e ruído.
    Retorna o sinal ruidoso e o vetor de tempo.
    
    Args:
        force_random: Se True, força geração totalmente aleatória (pode não ter pulsar)
    """
    T = 1 / Fs
    t = np.arange(0, duration, T)

    # Verificar se deve usar modo educativo ou aleatório
    use_educational_mode = not force_random and hasattr(np.random, 'get_state') and np.random.get_state()[1][0] == 42
    
    if use_educational_mode:
        # Modo educativo: usar frequências específicas para demonstração
        frequencies = [5, 15, 25]  # Hz - bem separadas para visualização
        amplitudes = [1.5, 1.0, 0.8]
        phases = [0, np.pi/4, np.pi/2]
        num_components = 3
    else:
        # Modo aleatório: pode gerar diferentes tipos de sinais
        signal_type = np.random.choice(['pulsar', 'noise_only', 'irregular'], p=[0.6, 0.2, 0.2])
        
        if signal_type == 'noise_only':
            # Apenas ruído - simula não detecção de pulsar
            num_components = 0
            frequencies = []
            amplitudes = []
            phases = []
        elif signal_type == 'irregular':
            # Componentes com frequências muito próximas ou muito fracas
            num_components = np.random.randint(1, 4)
            frequencies = []
            amplitudes = []
            phases = []
            
            base_freq = np.random.uniform(1, 10)
            for i in range(num_components):
                # Frequências próximas que podem causar batimento
                frequencies.append(base_freq + i * np.random.uniform(0.1, 2))
                amplitudes.append(np.random.uniform(0.2, 0.6))  # Amplitudes menores
                phases.append(np.random.uniform(0, 2 * np.pi))
        else:
            # Pulsar típico com componentes bem definidas
            num_components = np.random.randint(2, 5)
            frequencies = []
            amplitudes = []
            phases = []
            
            # Frequência fundamental
            fundamental = np.random.uniform(2, 20)
            frequencies.append(fundamental)
            amplitudes.append(np.random.uniform(1.0, 2.5))
            phases.append(np.random.uniform(0, 2 * np.pi))
            
            # Harmônicos ou frequências relacionadas
            for i in range(1, num_components):
                if np.random.random() < 0.7:  # 70% chance de ser harmônico
                    freq = fundamental * (i + 1) + np.random.uniform(-1, 1)
                else:  # Frequência independente
                    freq = np.random.uniform(5, 50)
                
                frequencies.append(freq)
                amplitudes.append(np.random.uniform(0.3, 1.5))
                phases.append(np.random.uniform(0, 2 * np.pi))

    # Gerar sinal como superposição
    signal = np.zeros_like(t)
    for i in range(num_components):
        component = amplitudes[i] * np.sin(2 * np.pi * frequencies[i] * t + phases[i])
        signal += component

    # Adicionar ruído gaussiano
    noise = noise_amplitude * np.random.randn(len(t))
    noisy_signal = signal + noise

    # Salvar informações para debugging
    signal_info = {
        'frequencies': frequencies,
        'amplitudes': amplitudes,
        'phases': phases,
        'num_components': num_components,
        'noise_amplitude': noise_amplitude,
        'fs': Fs,
        'duration': duration,
        'signal_type': 'educational' if use_educational_mode else signal_type if 'signal_type' in locals() else 'pulsar'
    }
    
    return noisy_signal, t, signal_info

def generate_educational_components(Fs, duration):
    """
    Gera componentes individuais para demonstração educativa.
    Retorna lista de componentes e parâmetros.
    """
    T = 1 / Fs
    t = np.arange(0, duration, T)
    
    # Componentes bem definidas para educação
    components_data = [
        {'freq': 5, 'amp': 1.5, 'phase': 0, 'name': 'Fundamental'},
        {'freq': 15, 'amp': 1.0, 'phase': np.pi/4, 'name': '1º Harmônico'},
        {'freq': 25, 'amp': 0.8, 'phase': np.pi/2, 'name': '2º Harmônico'}
    ]
    
    components = []
    for comp_data in components_data:
        signal = comp_data['amp'] * np.sin(2 * np.pi * comp_data['freq'] * t + comp_data['phase'])
        components.append({
            'signal': signal,
            'time': t,
            'freq': comp_data['freq'],
            'amp': comp_data['amp'],
            'phase': comp_data['phase'],
            'name': comp_data['name']
        })
    
    return components, components_data

if __name__ == '__main__':
    # Este bloco só executa se o script for rodado diretamente, não quando importado
    Fs_default = 1000
    duration_default = 2
    noise_amp_default = 0.5

    print("🎲 GERADOR DE SINAIS SINTÉTICOS")
    print("=" * 40)
    
    # Demonstração das componentes individuais
    print("\n1️⃣ Gerando componentes educativas...")
    components, comp_data = generate_educational_components(Fs_default, duration_default)
    
    # Plotar componentes individuais
    plt.figure(figsize=(12, 8))
    
    # Subplot das componentes
    plt.subplot(2, 2, 1)
    colors = ['red', 'blue', 'green']
    for i, comp in enumerate(components):
        plt.plot(comp['time'][:500], comp['signal'][:500], 
                color=colors[i], linewidth=2, 
                label=f"{comp['name']}: {comp['freq']} Hz")
    plt.title('Componentes Senoidais Individuais')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 0.5)
    
    # Sinal somado (limpo)
    plt.subplot(2, 2, 2)
    clean_signal = sum(comp['signal'] for comp in components)
    plt.plot(components[0]['time'][:500], clean_signal[:500], 
            'purple', linewidth=2, label='Sinal Limpo (Soma)')
    plt.title('Superposição das Componentes')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 0.5)
    
    # Gerar sinal ruidoso
    print("\n2️⃣ Adicionando ruído...")
    np.random.seed(42)  # Para reprodutibilidade
    noisy_sig, time_vec = generate_and_save_random_signal(Fs_default, duration_default, noise_amp_default)
    
    # Sinal com ruído
    plt.subplot(2, 2, 3)
    plt.plot(time_vec[:500], noisy_sig[:500], 
            'orange', alpha=0.8, label='Sinal + Ruído')
    plt.plot(time_vec[:500], clean_signal[:500], 
            'purple', alpha=0.5, linestyle='--', label='Original')
    plt.title('Sinal com Ruído Adicionado')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 0.5)
    
    # Informações
    plt.subplot(2, 2, 4)
    plt.axis('off')
    info_text = f"""
📊 PARÂMETROS DO SINAL:

🎯 Componentes:
"""
    for comp_data in comp_data:
        info_text += f"• {comp_data['name']}: {comp_data['freq']} Hz, A={comp_data['amp']:.1f}\n"
    
    info_text += f"""
⚙️ Configurações:
• Freq. amostragem: {Fs_default} Hz
• Duração: {duration_default} s
• Amostras: {len(noisy_sig)}
• Ruído: σ = {noise_amp_default}

🔬 Conceitos:
• Superposição linear
• Amostragem digital
• Ruído gaussiano
• Periodicidade
"""
    
    plt.text(0.1, 0.9, info_text, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))
    
    plt.suptitle('🎲 Demonstração: Geração de Sinais Educativos', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

    # Salvar arquivo
    np.savetxt('random_signal_noisy.txt', noisy_sig)
    print(f"\n✅ Sinal salvo em 'random_signal_noisy.txt'")
    print(f"📊 {len(noisy_sig)} amostras geradas")
    print("🎯 Para interface educativa completa, execute: python main_app.py")