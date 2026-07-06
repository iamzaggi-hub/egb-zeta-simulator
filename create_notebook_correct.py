import json

# Definir el contenido del cuaderno
cells = []

# Celda 0: Markdown de introducción
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# Simulador EGB-Zeta\n",
        "\n",
        "**Autor:** Francisco J. Zapata García (ZAGGI)\n",
        "\n",
        "Este cuaderno permite explorar las predicciones del manifiesto *\"Stability Analysis of Metric Tensor Perturbations in Einstein-Gauss-Bonnet Gravity via Riemann Zeta Distribution\"*.\n",
        "\n",
        "## Instrucciones\n",
        "Ejecuta las celdas en orden con **Shift+Enter**.\n",
        "Ingresa los valores cuando se te solicite."
    ]
})

# Celda 1: Importación de módulos
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "import sys",
        "import os",
        "sys.path.append(os.path.abspath(\"..\"))",
        "",
        "import numpy as np",
        "import matplotlib.pyplot as plt",
        "from src.zeta_utils import compute_zeros, compute_zeta_derivative_ratio",
        "from src.entropy_correction import compute_entropy_correction, compute_entropy_correction_relative",
        "from src.qnm_phase_shift import compute_phase_shift, generate_phase_shift_plot",
        "from src.hawking_spectrum import compute_hawking_temperature, compute_corrected_temperature, compute_spectral_flux",
        "",
        "%matplotlib inline",
        "plt.style.use(\"seaborn-v0_8-darkgrid\")",
        "print(\"✅ Módulos importados correctamente\")"
    ]
})

# Celda 2: Módulo 1 - Entropía corregida
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "print(\"=== CALCULADORA DE ENTROPÍA CORREGIDA ===\")",
        "M = float(input(\"Masa (M⊙): \"))",
        "S_BH = M ** 2",
        "S_corr = compute_entropy_correction(S_BH)",
        "S_rel = compute_entropy_correction_relative(S_BH)",
        "",
        "print(\"Masa:\", M, \"M⊙\")",
        "print(\"S_BH (clásica):\", S_BH)",
        "print(\"S (corregida):\", S_corr)",
        "print(\"Corrección relativa:\", S_rel*100, \"%\")"
    ]
})

# Celda 3: Módulo 2 - Desfase para LISA
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "print(\"=== CALCULADORA DE DESFASE PARA LISA ===\")",
        "M = float(input(\"Masa (M⊙): \"))",
        "N = int(input(\"N (ciclos): \"))",
        "",
        "delta_phi = compute_phase_shift(M, N)",
        "",
        "print(\"Masa:\", M, \"M⊙\")",
        "print(\"Número de ciclos:\", N)",
        "print(\"Desfase acumulativo: Δφ =\", delta_phi, \"rad\")",
        "",
        "if delta_phi >= 0.1:",
        "    print(\"✅ Este desfase es DETECTABLE por LISA (umbral: 0.1 rad)\")",
        "else:",
        "    print(\"⚠️ Este desfase es\", delta_phi/0.1*100, \"% del umbral de LISA (0.1 rad)\")"
    ]
})

# Celda 4: Módulo 3 - Temperatura de Hawking
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "print(\"=== CALCULADORA DE TEMPERATURA DE HAWKING ===\")",
        "M = float(input(\"Masa del PBH (M_P): \"))",
        "S_BH = M ** 2",
        "T_std = compute_hawking_temperature(M)",
        "T_corr = compute_corrected_temperature(M, S_BH)",
        "",
        "print(\"Masa:\", M, \"M_P\")",
        "print(\"T_H (estándar):\", T_std)",
        "print(\"T_H' (corregida):\", T_corr)",
        "print(\"Factor de corrección:\", T_corr/T_std)",
        "",
        "omega = np.logspace(-1, 2, 100)",
        "flux_std = compute_spectral_flux(omega, T_std)",
        "flux_corr = compute_spectral_flux(omega, T_corr)",
        "",
        "plt.figure(figsize=(10, 6))",
        "plt.plot(omega, flux_std, \"b--\", label=\"Hawking Estándar\", linewidth=2)",
        "plt.plot(omega, flux_corr, \"r-\", label=\"EGB-Zeta Modificado\", linewidth=2.5)",
        "plt.axvline(x=10, color=\"green\", linestyle=\":\", label=\"CTA (>100 GeV)\")",
        "plt.xlabel(\"Frecuencia (unidades de T)\", fontsize=12)",
        "plt.ylabel(\"Flujo (normalizado)\", fontsize=12)",
        "plt.title(\"Espectro de Hawking Modificado\", fontsize=14)",
        "plt.legend()",
        "plt.grid(True, alpha=0.3)",
        "plt.xscale(\"log\")",
        "plt.yscale(\"log\")",
        "plt.show()"
    ]
})

# Celda 5: Módulo 4 - Generar gráficas personalizadas
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "print(\"=== GENERACIÓN DE GRÁFICAS PERSONALIZADAS ===\")",
        "print(\"Selecciona una opción:\")",
        "print(\"1. Entropía corregida\")",
        "print(\"2. Desfase para IMBHs\")",
        "print(\"3. Espectro de Hawking\")",
        "print(\"4. Todas las figuras (como en visualizer.py)\")",
        "",
        "opcion = int(input(\"Opción (1-4): \"))",
        "",
        "if opcion == 1:",
        "    from src.entropy_correction import generate_entropy_correction_plot",
        "    generate_entropy_correction_plot(\"figures/entropy_correction.png\")",
        "    print(\"✅ Gráfica de entropía generada\")",
        "elif opcion == 2:",
        "    masses = [1000, 2000, 3000, 5000]",
        "    cycles_range = np.logspace(2, 6, 100)",
        "    generate_phase_shift_plot(masses, cycles_range, \"figures/qnm_phase_shift.png\")",
        "    print(\"✅ Gráfica de desfase generada\")",
        "elif opcion == 3:",
        "    M_range = np.logspace(-2, 2, 50)",
        "    from src.hawking_spectrum import generate_hawking_spectrum_plot",
        "    generate_hawking_spectrum_plot(M_range, \"figures/hawking_spectrum.png\")",
        "    print(\"✅ Gráfica de espectro de Hawking generada\")",
        "elif opcion == 4:",
        "    from src.visualizer import generate_all_figures",
        "    generate_all_figures()",
        "    print(\"✅ Todas las figuras generadas\")",
        "else:",
        "    print(\"❌ Opción no válida\")"
    ]
})

# Celda 6: Créditos e información del sistema
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "print(\"=== INFORMACIÓN DEL SISTEMA ===\")",
        "print(\"Python version:\", sys.version)",
        "print(\"NumPy version:\", np.__version__)",
        "",
        "try:",
        "    import mpmath",
        "    print(\"mpmath version:\", mpmath.__version__)",
        "except:",
        "    print(\"mpmath no instalado\")",
        "",
        "print(\"\")",
        "print(\"=== CRÉDITOS ===\")",
        "print(\"Simulador EGB-Zeta\")",
        "print(\"Autor: Francisco J. Zapata García (ZAGGI)\")",
        "print(\"Afiliación: Kinetic Vision Forensic Lab. (K-VISION Lab.), Chile\")",
        "print(\"Fecha: Julio 2026\")",
        "print(\"Manifiesto: Stability Analysis of Metric Tensor Perturbations in Einstein-Gauss-Bonnet Gravity via Riemann Zeta Distribution\")",
        "print(\"✅ Simulador listo para usar.\")"
    ]
})

# Crear la estructura del notebook
notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.12.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Guardar el archivo
with open('notebooks/demo_simulator.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print("✅ Cuaderno creado correctamente en notebooks/demo_simulator.ipynb")
