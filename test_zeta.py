import mpmath as mp

# La forma correcta de configurar la precisión en mpmath 1.3.0+
mp.mp.dps = 25  # Ahora usamos mp.mp.dps en lugar de mp.dps

# Buscar el primer cero no trivial de la función zeta
primer_cero = mp.zetazero(1)

print(f"Primer cero no trivial: {primer_cero}")
print(f"Parte real: {primer_cero.real}")
print(f"Parte imaginaria: {primer_cero.imag}")
print("¡mpmath funciona correctamente!")
