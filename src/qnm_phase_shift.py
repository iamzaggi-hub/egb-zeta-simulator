"""
Módulo qnm_phase_shift.py
Cálculo del desfase acumulativo para IMBHs detectables por LISA.
"""

import numpy as np
import matplotlib.pyplot as plt
from src.zeta_utils import compute_zeros, compute_zeta_derivative_ratio

def compute_entropy(mass_solar):
    """
    Calcula la entropía de Bekenstein-Hawking para una masa dada.
    S_BH ∝ M^2 (en unidades donde M_P = 1).
    
    Args:
        mass_solar (float): Masa en masas solares.
    
    Returns:
        float: Entropía S_BH.
    """
    # Relación simplificada: S_BH ≈ M^2 (en unidades de Planck)
    return mass_solar ** 2

def compute_phase_shift(mass_solar, n_cycles):
    """
    Calcula el desfase acumulativo para un IMBH.
    Δφ = (3/2) * (N / S_BH)
    
    Args:
        mass_solar (float): Masa en masas solares.
        n_cycles (int): Número de ciclos en banda.
    
    Returns:
        float: Desfase acumulativo en radianes.
    """
    S_BH = compute_entropy(mass_solar)
    delta_phi = (3.0 / 2.0) * (n_cycles / S_BH)
    return delta_phi

def generate_phase_shift_plot(masses, cycles_range, output_file="figures/qnm_phase_shift.png"):
    """
    Genera una gráfica de Δφ vs N para diferentes masas.
    
    Args:
        masses (list): Lista de masas en masas solares.
        cycles_range (array): Rango de valores para N.
        output_file (str): Ruta para guardar la figura.
    """
    plt.figure(figsize=(10, 6))
    colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(masses)))
    
    for i, M in enumerate(masses):
        delta_phis = [compute_phase_shift(M, N) for N in cycles_range]
        plt.plot(cycles_range, delta_phis, 
                 label=f'M = {M} M_sol',  # Quitamos el \o
                 color=colors[i], linewidth=2)
    
    # Umbral de sensibilidad de LISA (Δφ ≈ 0.1 rad)
    plt.axhline(y=0.1, color='red', linestyle='--', 
                label='Umbral LISA (0.1 rad)', linewidth=1.5)
    
    # Umbral óptimo para IMBHs (Δφ ≈ 0.15 rad)
    plt.axhline(y=0.15, color='green', linestyle=':', 
                label='Optimo IMBH (0.15 rad)', linewidth=1.5)
    
    plt.xlabel('Numero de ciclos en banda (N)', fontsize=12)  # Sin \D
    plt.ylabel('Desfase acumulativo (Delta phi)', fontsize=12)  # Sin \D
    plt.title('Desfase Acumulativo para IMBHs', fontsize=14)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    
    # Usar escala logarítmica si los valores abarcan varios órdenes de magnitud
    if max(cycles_range) / min(cycles_range) > 10:
        plt.xscale('log')
        plt.yscale('log')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Grafica guardada en: {output_file}")

def compute_qnm_correction(zeros_list, mass_solar, l=2, m=0):
    """
    Calcula la corrección a los QNMs usando la suma sobre los ceros.
    F = (1/S_BH) * Σ (ζ'(s_k)/ζ(s_k)) * Y_lm
    
    Args:
        zeros_list (list): Lista de ceros no triviales.
        mass_solar (float): Masa en masas solares.
        l (int): Número cuántico azimutal.
        m (int): Número cuántico magnético.
    
    Returns:
        complex: Corrección F.
    """
    S_BH = compute_entropy(mass_solar)
    F = 0.0j
    
    # Aproximación: Y_lm ≈ 1 para modos fundamentales
    for cero in zeros_list:
        ratio = compute_zeta_derivative_ratio(cero)
        F += ratio / S_BH
    
    return F

# Función para probar el módulo
if __name__ == "__main__":
    print("=== Prueba del módulo qnm_phase_shift ===")
    print("\nCalculando desfase para IMBH de 1000 M_sol con N = 10^5 ciclos:")
    delta_phi = compute_phase_shift(1000, 100000)
    print(f"Delta phi = {delta_phi:.6f} rad")
    
    print("\nGenerando gráfica de desfase...")
    masses = [1000, 2000, 3000, 5000]
    cycles_range = np.logspace(1, 6, 100)  # de 10 a 1,000,000 ciclos
    generate_phase_shift_plot(masses, cycles_range)
    
    print("\nCalculando corrección QNM para IMBH de 1000 M_sol:")
    zeros = compute_zeros(10, verbose=False)
    F = compute_qnm_correction(zeros, 1000)
    print(f"F = {F:.6f}")
    
    print("\n¡Módulo qnm_phase_shift.py funcionando correctamente!")
