"""
Módulo visualizer.py
Funciones de visualización unificadas para todas las predicciones.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os
import sys

# Añadir el directorio padre al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.zeta_utils import compute_zeros
from src.entropy_correction import compute_entropy_correction, compute_entropy_correction_relative
from src.qnm_phase_shift import compute_phase_shift, generate_phase_shift_plot
from src.hawking_spectrum import generate_hawking_spectrum_plot, generate_evaporation_spectrum

def generate_all_figures():
    """
    Genera todas las figuras del manifiesto.
    """
    print("=== Generando todas las figuras del manifiesto ===\n")
    
    # Crear carpeta de figuras si no existe
    os.makedirs("figures", exist_ok=True)
    
    # 1. Entropía corregida
    print("1. Generando gráfica de entropía corregida...")
    from src.entropy_correction import generate_entropy_correction_plot
    generate_entropy_correction_plot("figures/entropy_correction.png")
    
    # 2. Desfase para IMBHs
    print("\n2. Generando gráfica de desfase para IMBHs...")
    masses = [1000, 2000, 3000, 5000, 10000]
    cycles_range = np.logspace(2, 6, 100)  # 100 a 1,000,000 ciclos
    generate_phase_shift_plot(masses, cycles_range, "figures/qnm_phase_shift.png")
    
    # 3. Espectro de Hawking
    print("\n3. Generando gráficas del espectro de Hawking...")
    M_range = np.logspace(-2, 2, 50)
    generate_hawking_spectrum_plot(M_range, "figures/hawking_spectrum.png")
    generate_evaporation_spectrum("figures/evaporation_peak.png")
    
    print("\n✓ Todas las figuras se han generado correctamente.")
    print("  - figures/entropy_correction.png")
    print("  - figures/qnm_phase_shift.png")
    print("  - figures/hawking_spectrum.png")
    print("  - figures/evaporation_peak.png")

def generate_combined_figure(output_file="figures/combined_predictions.png"):
    """
    Genera una figura combinada con las tres predicciones principales.
    """
    print("\nGenerando figura combinada...")
    
    fig = plt.figure(figsize=(15, 10))
    gs = GridSpec(2, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    # 1. Entropía corregida (superior izquierda)
    ax1 = fig.add_subplot(gs[0, 0])
    S_BH_range = np.logspace(0, 6, 100)
    S_corr = [compute_entropy_correction(S) for S in S_BH_range]
    ax1.plot(S_BH_range, S_BH_range, 'b--', label='S_BH (clasica)', alpha=0.5, linewidth=1.5)
    ax1.plot(S_BH_range, S_corr, 'r-', label='Corregida', linewidth=2.5)
    ax1.set_xlabel('S_BH', fontsize=11)
    ax1.set_ylabel('S', fontsize=11)
    ax1.set_title('Entropia Corregida', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    
    # 2. Desfase QNM (superior central)
    ax2 = fig.add_subplot(gs[0, 1])
    masses = [1000, 3000, 5000]
    cycles_range = np.logspace(2, 6, 100)
    for M in masses:
        delta_phis = [compute_phase_shift(M, N) for N in cycles_range]
        ax2.plot(cycles_range, delta_phis, label=f'{M} M_sol', linewidth=2)
    ax2.axhline(y=0.1, color='red', linestyle='--', label='Umbral LISA', alpha=0.7)
    ax2.set_xlabel('N (ciclos)', fontsize=11)
    ax2.set_ylabel('Delta phi (rad)', fontsize=11)
    ax2.set_title('Desfase para IMBHs', fontsize=12)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    
    # 3. Espectro Hawking (superior derecho)
    ax3 = fig.add_subplot(gs[0, 2])
    M = 1.0
    S_BH = M ** 2
    T_standard = 1.0 / M
    T_corrected = T_standard / (1.0 - 3.0 / (2.0 * S_BH))
    omega = np.logspace(-2, 2, 100)
    flux_standard = (omega / T_standard)**3 / (np.exp(omega / T_standard) - 1)
    flux_corrected = (omega / T_corrected)**3 / (np.exp(omega / T_corrected) - 1)
    flux_standard = flux_standard / np.max(flux_standard)
    flux_corrected = flux_corrected / np.max(flux_corrected)
    ax3.plot(omega, flux_standard, 'b--', label='Estandar', alpha=0.7, linewidth=2)
    ax3.plot(omega, flux_corrected, 'r-', label='EGB-Zeta', linewidth=2.5)
    ax3.axvline(x=10, color='green', linestyle=':', alpha=0.7, label='CTA >100 GeV')
    ax3.set_xlabel('Frecuencia', fontsize=11)
    ax3.set_ylabel('Flujo', fontsize=11)
    ax3.set_title('Espectro de Hawking', fontsize=12)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    
    # 4. Corrección relativa (inferior izquierda)
    ax4 = fig.add_subplot(gs[1, 0])
    S_rel = [compute_entropy_correction_relative(S) for S in S_BH_range]
    ax4.plot(S_BH_range, S_rel, 'g-', linewidth=2.5)
    ax4.axhline(y=-0.01, color='red', linestyle='--', label='-1%', alpha=0.7)
    ax4.set_xlabel('S_BH', fontsize=11)
    ax4.set_ylabel('Correccion relativa', fontsize=11)
    ax4.set_title('Correccion Relativa de Entropia', fontsize=12)
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_xscale('log')
    ax4.set_yscale('log')
    
    # 5. Evaporación final (inferior central)
    ax5 = fig.add_subplot(gs[1, 1])
    masses_pbh = np.logspace(0, 3, 50)
    S_pbh = masses_pbh ** 2
    temps = [1.0 / (M * (1.0 - 3.0 / (2.0 * S))) for M, S in zip(masses_pbh, S_pbh)]
    ax5.plot(masses_pbh, temps, 'b-', linewidth=2.5)
    ax5.axvline(x=1, color='green', linestyle=':', label='PBH (10^15 g)', alpha=0.7)
    ax5.set_xlabel('Masa (M_P)', fontsize=11)
    ax5.set_ylabel('Temperatura', fontsize=11)
    ax5.set_title('Evaporacion Final', fontsize=12)
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    ax5.set_xscale('log')
    ax5.set_yscale('log')
    
    # 6. Espacio para texto o esquema (inferior derecho)
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.text(0.1, 0.8, "Predicciones Clave:", fontsize=14, fontweight='bold')
    ax6.text(0.1, 0.6, "• IMBHs (LISA): Delta phi ≈ 0.1 - 0.15 rad", fontsize=12)
    ax6.text(0.1, 0.45, "• PBHs (CTA): Espectro log-periodico", fontsize=12)
    ax6.text(0.1, 0.3, "• Entropia: S = S_BH - 3/2 log(S_BH)", fontsize=12)
    ax6.text(0.1, 0.15, "• Estabilidad: Re(s) > 1/4", fontsize=12)
    ax6.axis('off')
    ax6.set_title('Resumen de Predicciones', fontsize=12)
    
    plt.suptitle('Predicciones del Modelo EGB-Zeta', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Figura combinada guardada en: {output_file}")

def print_summary():
    """
    Imprime un resumen de las predicciones numéricas.
    """
    print("\n" + "="*60)
    print("RESUMEN DE PREDICCIONES NUMERICAS")
    print("="*60)
    
    # Entropía para diferentes masas
    masses = [1, 10, 100, 1000, 10000, 1e6, 1e9]
    print("\n1. CORRECCION DE ENTROPIA:")
    print("   M (M⊙)\tS_BH\t\tS_corregida")
    for M in masses[:5]:
        S_BH = M ** 2
        S_corr = S_BH - 1.5 * np.log(S_BH)
        print(f"   {M:.0e}\t\t{S_BH:.2e}\t\t{S_corr:.2e}")
    
    # Desfase para IMBHs
    print("\n2. DESFASE PARA IMBHs (LISA):")
    masses_imbh = [1000, 2000, 3000, 5000, 10000]
    N = 100000  # 10^5 ciclos
    for M in masses_imbh:
        S_BH = M ** 2
        delta_phi = 1.5 * N / S_BH
        print(f"   M = {M} M⊙: Delta phi = {delta_phi:.6f} rad")
    
    # Espectro de Hawking
    print("\n3. ESPECTRO DE HAWKING (PBHs):")
    M_PBH = 1.0  # Masa de Planck (~10^15 g)
    S_BH = M_PBH ** 2
    T_std = 1.0 / M_PBH
    T_corr = T_std / (1.0 - 1.5 / S_BH)
    print(f"   PBH (M = 10^15 g):")
    print(f"   T_H (estandar) = {T_std:.6f}")
    print(f"   T_H' (corregida) = {T_corr:.6f}")
    print(f"   Razon = {T_corr/T_std:.6f}")
    
    print("\n" + "="*60)

# Función para probar el módulo
if __name__ == "__main__":
    print("=== Prueba del módulo visualizer ===")
    
    # Generar todas las figuras
    generate_all_figures()
    
    # Generar figura combinada
    generate_combined_figure()
    
    # Imprimir resumen
    print_summary()
    
    print("\n¡Módulo visualizer.py funcionando correctamente!")
