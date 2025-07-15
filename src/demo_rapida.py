"""
🌟 DEMONSTRAÇÃO RÁPIDA - DETECÇÃO DE PULSARES
Executa todos os passos automaticamente para demonstração
"""

import numpy as np
import matplotlib.pyplot as plt
from generate_signal import generate_and_save_random_signal
from process_signal import process_and_analyze_signal

def demo_completa():
    """Demonstração completa do pipeline de detecção"""
    
    print("🌟 DEMONSTRAÇÃO: DETECÇÃO DE PULSARES")
    print("=" * 50)
    
    # Parâmetros
    Fs = 1000  # Hz
    duration = 2  # segundos
    noise_amplitude = 0.5
    
    print(f"📊 Parâmetros:")
    print(f"   • Frequência de amostragem: {Fs} Hz")
    print(f"   • Duração: {duration} s")
    print(f"   • Amplitude do ruído: {noise_amplitude}")
    print()
    
    # Passo 1: Gerar sinal
    print("1️⃣ Gerando sinal sintético...")
    np.random.seed(42)  # Para reprodutibilidade
    noisy_signal, time_vector = generate_and_save_random_signal(Fs, duration, noise_amplitude)
    print(f"   ✅ Sinal gerado com {len(noisy_signal)} amostras")
    
    # Passo 2: Processar sinal
    print("\n2️⃣ Processando e analisando sinal...")
    results = process_and_analyze_signal(noisy_signal, Fs, cutoff_freq=35, filter_order=5)
    
    # Calcular SNR
    noise = noisy_signal - results['filtered_signal']
    signal_power = np.mean(results['filtered_signal']**2)
    noise_power = np.mean(noise**2)
    snr_db = 10 * np.log10(signal_power / noise_power)
    
    print(f"   ✅ Filtro aplicado (corte: {results['cutoff_freq']} Hz)")
    print(f"   ✅ FFT calculada com resolução: {Fs/len(noisy_signal):.2f} Hz")
    print(f"   ✅ SNR estimada: {snr_db:.1f} dB")
    
    # Passo 3: Resultados
    print("\n3️⃣ Resultados da detecção:")
    if results['detected_peak_freq'] > 0:
        print(f"   🎯 Frequência detectada: {results['detected_peak_freq']:.2f} Hz")
        print(f"   ⏰ Período detectado: {results['detected_period']:.3f} s")
        print(f"   ✅ STATUS: PULSAR DETECTADO!")
    else:
        print(f"   ❌ STATUS: PULSAR NÃO DETECTADO")
    
    # Passo 4: Plotar resultados
    print("\n4️⃣ Gerando visualizações...")
    
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('🌟 DEMONSTRAÇÃO: DETECÇÃO DE PULSARES', fontsize=16, fontweight='bold')
    
    # Plot 1: Sinal no tempo
    axes[0,0].plot(time_vector[:1000], noisy_signal[:1000], 'b-', alpha=0.7, label='Sinal Ruidoso')
    axes[0,0].plot(time_vector[:1000], results['filtered_signal'][:1000], 'r-', linewidth=2, label='Sinal Filtrado')
    axes[0,0].set_title('Sinais no Domínio do Tempo')
    axes[0,0].set_xlabel('Tempo (s)')
    axes[0,0].set_ylabel('Amplitude')
    axes[0,0].grid(True, alpha=0.3)
    axes[0,0].legend()
    axes[0,0].set_xlim(0, 1)
    
    # Plot 2: Espectro de potência
    axes[0,1].semilogy(results['frequencies'], results['power_spectrum_original'], 
                       'b-', alpha=0.7, label='Original')
    axes[0,1].semilogy(results['frequencies'], results['power_spectrum_filtered'], 
                       'r-', linewidth=2, label='Filtrado')
    axes[0,1].axvline(x=results['cutoff_freq'], color='g', linestyle='--', 
                      label=f'Corte ({results["cutoff_freq"]} Hz)')
    if results['detected_peak_freq'] > 0:
        axes[0,1].axvline(x=results['detected_peak_freq'], color='purple', 
                          linestyle='--', linewidth=2,
                          label=f'Detectado ({results["detected_peak_freq"]:.1f} Hz)')
    axes[0,1].set_title('Espectro de Potência (Escala Log)')
    axes[0,1].set_xlabel('Frequência (Hz)')
    axes[0,1].set_ylabel('Potência')
    axes[0,1].grid(True, alpha=0.3)
    axes[0,1].legend()
    axes[0,1].set_xlim(0, 100)
    
    # Plot 3: Zoom no espectro
    axes[1,0].plot(results['frequencies'], results['power_spectrum_filtered'], 'r-', linewidth=2)
    if results['detected_peak_freq'] > 0:
        axes[1,0].axvline(x=results['detected_peak_freq'], color='purple', 
                          linestyle='--', linewidth=2,
                          label=f'Pico: {results["detected_peak_freq"]:.1f} Hz')
    axes[1,0].set_title('Zoom: Detecção de Picos')
    axes[1,0].set_xlabel('Frequência (Hz)')
    axes[1,0].set_ylabel('Potência')
    axes[1,0].grid(True, alpha=0.3)
    axes[1,0].legend()
    axes[1,0].set_xlim(0, 50)
    
    # Plot 4: Informações resumidas
    axes[1,1].axis('off')
    info_text = f"""
📊 RESUMO DOS RESULTADOS

🔍 DETECÇÃO:
• Frequência: {results['detected_peak_freq']:.2f} Hz
• Período: {results['detected_period']:.3f} s
• Status: {"✅ DETECTADO" if results['detected_peak_freq'] > 0 else "❌ NÃO DETECTADO"}

⚙️ PROCESSAMENTO:
• Filtro: Butterworth {results['filter_order']}ª ordem
• Corte: {results['cutoff_freq']} Hz  
• SNR: {snr_db:.1f} dB
• Amostras: {len(noisy_signal)}

🎯 CONCEITOS APLICADOS:
• Superposição de senoides
• Filtragem passa-baixa (LTI)
• Análise espectral (FFT)
• Detecção de periodicidade
• Processamento de ruído

🌟 APLICAÇÃO:
Este processo é usado em radiotelescópios
reais para detectar pulsares no universo!
    """
    axes[1,1].text(0.05, 0.95, info_text, fontsize=10, verticalalignment='top',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
    
    plt.tight_layout()
    plt.show()
    
    print("   ✅ Gráficos gerados com sucesso!")
    print("\n🎉 DEMONSTRAÇÃO CONCLUÍDA!")
    print("\n💡 Para aprendizado interativo passo-a-passo, execute: python src/main_app.py")

if __name__ == "__main__":
    demo_completa()
