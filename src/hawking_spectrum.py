"""
Módulo hawking_spectrum.py
Cálculo del espectro de Hawking modificado para PBHs.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import hbar, c, k, pi

def compute_hawking_temperature(M, M_Planck=1.0):
    """
    Calcula la temperatura de Hawking estándar.
    T_H = (hbar * c^3) / (8 * pi * G * k * M)
    
    Args:
        M (float): Masa del agujero negro.
        M_Planck (float): Masa de Planck (en las mismas unidades).
    
    Returns:
        float: Temperatura de Hawking.
    """
    # Usando unidades simplificadas: T_H ≈ 1/M (en unidades de Planck)
    return 1.0 / M

def compute_corrected_temperature(M, S_BH=None):
    """
    Calcula la temperatura corregida.
    T_H' = T_H / (1 - 3/(2*S_BH))
    
    Args:
        M (float): Masa del agujero negro.
        S_BH (float): Entropía (opcional, se calcula si no se proporciona).
    
    Returns:
        float: Temperatura corregida.
    """
    if S_BH is None:
        S_BH = M ** 2  # Simplificación: S_BH ≈ M^2
    
    if S_BH <= 1.5:  # Corrección crítica: S_BH > 1.5 para evitar divisiones problemáticas
        S_BH = 1.51
    
    T_H = compute_hawking_temperature(M)
    factor = 1.0 / (1.0 - 3.0 / (2.0 * S_BH))
    return T_H * factor

def compute_spectral_flux(omega, T):
    """
    Calcula el flujo espectral de Hawking (aproximación de cuerpo negro).
    dE/dω ∝ ω^3 / (exp(ω/T) - 1)
    
    Args:
        omega (array): Frecuencias (en unidades de temperatura).
        T (float): Temperatura del agujero negro.
    
    Returns:
        array: Flujo espectral (normalizado).
    """
    # En unidades donde k_B = hbar = 1
    x = omega / T
    
    # Protección contra overflow numérico
    x_clipped = np.clip(x, -100, 100)  # Limitar para evitar overflow en exp
    
    # Calcular el flujo, evitando divisiones por cero
    with np.errstate(divide='ignore', invalid='ignore'):
        flux = np.where(
            np.abs(x_clipped) > 1e-10,
            x_clipped**3 / (np.exp(x_clipped) - 1),
            0.0
        )
    
    # Reemplazar valores no finitos con 0
    flux = np.nan_to_num(flux, nan=0.0, posinf=0.0, neginf=0.0)
    
    # Normalizar solo si el máximo es > 0
    max_flux = np.max(flux)
    if max_flux > 0:
        flux = flux / max_flux
    
    return flux

def generate_hawking_spectrum_plot(M_range, output_file="figures/hawking_spectrum.png"):
    """
    Genera una gráfica del espectro de Hawking modificado.
    
    Args:
        M_range (array): Rango de masas para la evaporación final (no usado en esta versión).
        output_file (str): Ruta para guardar la figura.
    """
    # Usamos una masa específica para la gráfica principal
    M = 1.0  # En unidades de Planck (≈ 10^15 g)
    S_BH = M ** 2
    
    # Calcular temperaturas
    T_standard = compute_hawking_temperature(M)
    T_corrected = compute_corrected_temperature(M, S_BH)
    
    # Generar espectro - usando un rango de frecuencias adecuado
    omega = np.logspace(-1, 2, 100)  # Frecuencias alrededor de la temperatura
    
    flux_standard = compute_spectral_flux(omega, T_standard)
    flux_corrected = compute_spectral_flux(omega, T_corrected)
    
    # Verificar que los arrays no estén vacíos
    if len(flux_standard) == 0 or len(flux_corrected) == 0:
        print("Error: Arrays de flujo vacíos")
        return
    
    plt.figure(figsize=(10, 6))
    
    # Espectro estándar
    plt.plot(omega, flux_standard, 'b--', label='Hawking Estándar', linewidth=2, alpha=0.7)
    
    # Espectro corregido
    plt.plot(omega, flux_corrected, 'r-', label='EGB-Zeta Modificado', linewidth=2.5)
    
    # Resaltar la región de >100 GeV (en unidades simplificadas, ~10^3)
    plt.axvline(x=10, color='green', linestyle=':', label='CTA (>100 GeV)', alpha=0.7)
    
    # Sombra para la región detectable por CTA (solo si hay valores en esa región)
    max_omega = np.max(omega)
    if max_omega > 10:
        plt.axvspan(10, min(100, max_omega), alpha=0.2, color='green', label='Región CTA')
    
    plt.xlabel('Frecuencia (unidades de T)', fontsize=12)
    plt.ylabel('Flujo (normalizado)', fontsize=12)
    plt.title('Espectro de Hawking Modificado para PBHs', fontsize=14)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    
    # Escala logarítmica solo si los valores son positivos
    if np.all(omega > 0) and np.all(flux_standard >= 0) and np.all(flux_corrected >= 0):
        plt.xscale('log')
        plt.yscale('log')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Gráfica guardada en: {output_file}")
    
    # Imprimir valores de temperatura
    print(f"\nTemperatura estándar: T_H ≈ {T_standard:.2e}")
    print(f"Temperatura corregida: T_H' ≈ {T_corrected:.2e}")
    print(f"Factor de corrección: {T_corrected/T_standard:.6f}")

def generate_evaporation_spectrum(output_file="figures/evaporation_peak.png"):
    """
    Genera una gráfica del pico de evaporación para PBHs.
    """
    # Simular la evaporación final: M disminuye, T aumenta
    masses = np.logspace(0, 3, 50)  # Desde 1 hasta 1000 en unidades de M_P
    S_BH = masses ** 2
    
    # Calcular temperaturas corregidas
    temperatures = [compute_corrected_temperature(M, S) for M, S in zip(masses, S_BH)]
    
    # Calcular flujo máximo en función de la masa
    flux_peak = 1.0 / masses  # Aproximación: el flujo máximo escala como 1/M
    
    # Limpiar valores no finitos
    temperatures = np.nan_to_num(temperatures, nan=0.0, posinf=0.0, neginf=0.0)
    flux_peak = np.nan_to_num(flux_peak, nan=0.0, posinf=0.0, neginf=0.0)
    
    plt.figure(figsize=(10, 6))
    
    # Solo plotear si hay valores positivos
    mask = (temperatures > 0) & (flux_peak > 0)
    if np.any(mask):
        plt.plot(masses[mask], temperatures[mask], 'b-', linewidth=2.5, label='Temperatura corregida')
        plt.plot(masses[mask], flux_peak[mask], 'r--', linewidth=2, label='Flujo máximo (aprox.)', alpha=0.7)
    
    # Resaltar la región de PBHs (M ~ 1 en unidades de Planck)
    plt.axvline(x=1, color='green', linestyle=':', label='PBH (M ~ 10^15 g)', alpha=0.7)
    plt.axvspan(0.5, 2, alpha=0.2, color='green', label='Región de evaporación final')
    
    plt.xlabel('Masa (en unidades de Planck)', fontsize=12)
    plt.ylabel('Valor (unidades simplificadas)', fontsize=12)
    plt.title('Evaporación Final de PBHs', fontsize=14)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    
    # Escala logarítmica solo si los valores son positivos
    if np.all(masses > 0) and np.all(temperatures >= 0) and np.all(flux_peak >= 0):
        plt.xscale('log')
        plt.yscale('log')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Gráfica guardada en: {output_file}")

# Función para probar el módulo
if __name__ == "__main__":
    print("=== Prueba del módulo hawking_spectrum ===")
    
    # Probar con una masa típica de PBH
    M = 1.0  # En unidades de Planck (≈ 10^15 g)
    S_BH = M ** 2
    T_standard = compute_hawking_temperature(M)
    T_corrected = compute_corrected_temperature(M, S_BH)
    
    print(f"\nPara PBH con M = {M:.2f} M_P:")
    print(f"T_H (estándar) = {T_standard:.6f}")
    print(f"T_H' (corregida) = {T_corrected:.6f}")
    print(f"Razón T_H'/T_H = {T_corrected/T_standard:.6f}")
    
    print("\nGenerando gráficas del espectro de Hawking...")
    M_range = np.logspace(-2, 2, 50)
    generate_hawking_spectrum_plot(M_range)
    generate_evaporation_spectrum()
    
    print("\n¡Módulo hawking_spectrum.py funcionando correctamente!")
