"""
Módulo zeta_utils.py
Cálculo de la función zeta de Riemann, sus ceros y derivadas.
"""

import mpmath as mp
import numpy as np

# Configurar precisión global para mpmath
mp.mp.dps = 50  # 50 dígitos de precisión para cálculos numéricos

def compute_zeros(n_zeros=10, verbose=True):
    """
    Calcula los primeros n_zeros ceros no triviales de la función zeta.
    
    Args:
        n_zeros (int): Número de ceros a calcular.
        verbose (bool): Si es True, imprime progreso.
    
    Returns:
        list: Lista de ceros como números complejos (s_k = 1/2 + i*tau_k).
    """
    zeros = []
    for k in range(1, n_zeros + 1):
        cero = mp.zetazero(k)
        zeros.append(cero)
        if verbose:
            print(f"Cero {k}: s = {cero:.6f} (tau = {cero.imag:.6f})")
    return zeros

def compute_zeta_derivative_ratio(s):
    """
    Calcula el cociente ζ'(s)/ζ(s) para un punto s dado.
    
    Args:
        s (complex): Punto en el plano complejo.
    
    Returns:
        complex: Valor de ζ'(s)/ζ(s).
    """
    # Usamos la función zeta de mpmath y su derivada numérica
    # Nota: mpmath tiene ζ(s) y ζ'(s) como funciones nativas
    zeta_val = mp.zeta(s)
    zeta_deriv = mp.zeta(s, derivative=1)
    return zeta_deriv / zeta_val

def compute_partition_function_zeta(beta, zeros_list, verbose=True):
    """
    Calcula la función de partición usando la representación integral con ceros.
    Z(β) = ∮ (ζ'(s)/ζ(s)) e^{-β s} ds
    
    Aproximación numérica: sumamos sobre los ceros en la línea crítica.
    
    Args:
        beta (float): Parámetro de temperatura inversa.
        zeros_list (list): Lista de ceros no triviales.
        verbose (bool): Si es True, imprime progreso.
    
    Returns:
        complex: Valor aproximado de Z(β).
    """
    Z = 0.0j
    for cero in zeros_list:
        # Contribución del polo en s = cero
        residuo = 1.0  # El residuo de ζ'(s)/ζ(s) en un cero simple es 1
        contribucion = residuo * mp.exp(-beta * cero)
        Z += contribucion
        if verbose:
            print(f"Contribución del cero {cero:.6f}: {contribucion:.6f}")
    return Z

def compute_spectral_density(tau_values, eta=0.01):
    """
    Calcula la densidad espectral usando la función de distribución de ceros.
    Esta es una aproximación para la suma sobre los ceros: Σ ζ'(s_k)/ζ(s_k) * Y_lm
    
    Args:
        tau_values (array): Valores de tau (parte imaginaria de los ceros).
        eta (float): Parámetro de suavizado.
    
    Returns:
        array: Densidad espectral normalizada.
    """
    density = np.zeros_like(tau_values, dtype=complex)
    for i, tau in enumerate(tau_values):
        s = 0.5 + 1j * tau
        # La derivada logarítmica es aproximadamente -Σ 1/(s - s_k)
        # Aquí usamos una aproximación con los ceros cercanos
        # Para un cálculo exacto, necesitaríamos la función zeta
        density[i] = compute_zeta_derivative_ratio(s)
    return density

# Función para probar el módulo
if __name__ == "__main__":
    print("=== Prueba del módulo zeta_utils ===")
    print("Calculando los primeros 5 ceros no triviales de Riemann:")
    zeros = compute_zeros(5)
    print(f"\nCeros calculados: {zeros}")
    
    print("\nCalculando la derivada logarítmica en s = 1/2 + i*14.13...")
    s = 0.5 + 1j * 14.1347
    ratio = compute_zeta_derivative_ratio(s)
    print(f"ζ'(s)/ζ(s) = {ratio:.6f}")
    
    print("\nCalculando la función de partición Z(β) con β = 1.0:")
    Z = compute_partition_function_zeta(1.0, zeros, verbose=False)
    print(f"Z(1.0) ≈ {Z:.6f}")
    
    print("\n¡Módulo zeta_utils.py funcionando correctamente!")
