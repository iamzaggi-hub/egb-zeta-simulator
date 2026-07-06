"""
Módulo entropy_correction.py
Cálculo de la corrección logarítmica de entropía.
S = S_BH - (3/2) * log(S_BH)
"""

import numpy as np
import matplotlib.pyplot as plt

def compute_entropy_correction(S_BH):
    """
    Calcula la entropía corregida.
    
    Args:
        S_BH (float): Entropía de Bekenstein-Hawking.
    
    Returns:
        float: Entropía corregida.
    """
    if S_BH <= 0:
        raise ValueError("S_BH debe ser mayor que 0")
    return S_BH - (3.0 / 2.0) * np.log(S_BH)

def compute_entropy_correction_relative(S_BH):
    """
    Calcula la corrección relativa: (S - S_BH) / S_BH.
    
    Args:
        S_BH (float): Entropía de Bekenstein-Hawking.
    
    Returns:
        float: Corrección relativa.
    """
    if S_BH <= 0:
        raise ValueError("S_BH debe ser mayor que 0")
    return - (3.0 / 2.0) * np.log(S_BH) / S_BH

def generate_entropy_correction_plot(output_file="figures/entropy_correction.png"):
    """
    Genera una gráfica de la corrección logarítmica de entropía.
    
    Args:
        output_file (str): Ruta para guardar la figura.
    """
    # Rango de S_BH para la gráfica (evitando S_BH = 1 donde log=0)
    S_BH_range = np.logspace(0.1, 6, 100)  # desde 1.26 hasta 1,000,000
    
    # Calcular corrección
    S_corr = [compute_entropy_correction(S) for S in S_BH_range]
    S_relative = [compute_entropy_correction_relative(S) for S in S_BH_range]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Gráfica 1: Entropía corregida vs S_BH
    ax1.plot(S_BH_range, S_BH_range, 'b--', label='S_BH (clásica)', alpha=0.5, linewidth=1.5)
    ax1.plot(S_BH_range, S_corr, 'r-', label='S = S_BH - (3/2)log(S_BH)', linewidth=2.5)
    ax1.set_xlabel('S_BH', fontsize=12)
    ax1.set_ylabel('S', fontsize=12)
    ax1.set_title('Entropía Corregida', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    
    # Gráfica 2: Corrección relativa vs S_BH
    ax2.plot(S_BH_range, S_relative, 'g-', linewidth=2.5)
    ax2.axhline(y=-0.01, color='red', linestyle='--', label='-1%', alpha=0.7)
    ax2.axhline(y=-0.001, color='orange', linestyle='--', label='-0.1%', alpha=0.7)
    ax2.set_xlabel('S_BH', fontsize=12)
    ax2.set_ylabel('(S - S_BH) / S_BH', fontsize=12)
    ax2.set_title('Corrección Relativa', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Gráfica guardada en: {output_file}")

def print_entropy_values(masses):
    """
    Imprime valores de entropía para diferentes masas.
    
    Args:
        masses (list): Lista de masas en masas solares.
    """
    print("\n=== Valores de Entropía para Diferentes Masas ===")
    print("M (M⊙)\t\tS_BH\t\tS_corregida\t\tCorrección Relativa")
    print("-" * 70)
    
    for M in masses:
        S_BH = M ** 2
        S_corr = compute_entropy_correction(S_BH)
        S_rel = compute_entropy_correction_relative(S_BH)
        print(f"{M:.0e}\t\t{S_BH:.2e}\t\t{S_corr:.2e}\t\t{S_rel:.4%}")

# Función para probar el módulo
if __name__ == "__main__":
    print("=== Prueba del módulo entropy_correction ===")
    
    # Ejemplos para diferentes masas
    masses = [1, 10, 100, 1000, 10000, 1e6, 1e9]
    print_entropy_values(masses)
    
    print("\nGenerando gráfica de corrección entrópica...")
    generate_entropy_correction_plot()
    
    print("\n¡Módulo entropy_correction.py funcionando correctamente!")
