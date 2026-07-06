# Simulador EGB-Zeta

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21226269.svg)](https://doi.org/10.5281/zenodo.21226269)

Simulador numérico para el manifiesto *"Stability Analysis of Metric Tensor Perturbations in Einstein-Gauss-Bonnet Gravity via Riemann Zeta Distribution"*.

**Autor:** Francisco J. Zapata García (ZAGGI)  
**Afiliación:** Kinetic Vision Forensic Lab. (K-VISION Lab.), Chile  
**Fecha:** Julio 2026

---

## 📋 Descripción

Este repositorio contiene el código fuente y las figuras generadas para el artículo:

> **"Stability Analysis of Metric Tensor Perturbations in Einstein-Gauss-Bonnet Gravity via Riemann Zeta Distribution"**
>
> El simulador implementa:
> - Cálculo de ceros no triviales de la función zeta de Riemann
> - Corrección logarítmica de entropía: \( S = S_{BH} - \frac{3}{2}\log(S_{BH}) \)
> - Desfase acumulativo para IMBHs detectables por LISA
> - Espectro de Hawking modificado para PBHs (observable por CTA)

---

## 🛠️ Requisitos

- Python 3.12 o superior
- Bibliotecas: numpy, scipy, matplotlib, mpmath, jupyter

---

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/iamzaggi-hub/egb-zeta-simulator.git
cd egb-zeta-simulator

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

🚀 Uso
Generar todas las figuras
bash
python src/visualizer.py
Script interactivo
bash
python interactivo.py
Cuaderno Jupyter (opcional)
bash
jupyter notebook notebooks/demo_simulator.ipynb
📊 Resultados
Las figuras generadas se encuentran en la carpeta figures/:

Figura	Descripción
entropy_correction.png	Corrección logarítmica de entropía
qnm_phase_shift.png	Desfase acumulativo para IMBHs (LISA)
hawking_spectrum.png	Espectro de Hawking modificado
evaporation_peak.png	Pico de evaporación para PBHs
combined_predictions.png	Resumen visual de todas las predicciones
📁 Estructura del Proyecto
text
egb-zeta-simulator/
├── README.md              # Este archivo
├── requirements.txt       # Dependencias
├── .gitignore            # Archivos ignorados por Git
├── interactivo.py        # Script interactivo
├── src/
│   ├── __init__.py
│   ├── zeta_utils.py      # Cálculo de ceros de Riemann
│   ├── entropy_correction.py  # Corrección de entropía
│   ├── qnm_phase_shift.py     # Desfase para LISA
│   ├── hawking_spectrum.py    # Espectro de Hawking
│   └── visualizer.py          # Generación de figuras
├── notebooks/
│   └── demo_simulator.ipynb   # Cuaderno Jupyter (opcional)
└── figures/               # Figuras generadas

📄 Licencia
Este proyecto está bajo la licencia MIT. Ver el archivo LICENSE para más detalles.

📚 Cómo citar este trabajo
Si utilizas este simulador en tu investigación, por favor cítalo como:

Zapata García, F. J. (2026). egb-zeta-simulator: Simulador numérico para el manifiesto "Stability Analysis of Metric Tensor Perturbations in Einstein-Gauss-Bonnet Gravity via Riemann Zeta Distribution" (Version v1.0.1) [Código fuente]. Zenodo. https://doi.org/10.5281/zenodo.21226269

📧 Contacto
Francisco J. Zapata García (ZAGGI)
📧 iamzaggi@gmail.com
🔗 ORCID: 0009-0004-8127-1933
🏛️ Kinetic Vision Forensic Lab. (K-VISION Lab.), Chile

🙏 Agradecimientos
Este trabajo fue inspirado y enriquecido por el Workshop on Foundations of Quantum Mechanics (UC, Santiago, Julio 2026). Agradecimientos especiales a Olimpia Lombardi, Pablo Acuña, Pedro Lamberti, Julio Oliva, Paola Arias, Gonzalo Palma, Aldo Delgado, Pablo Solano, Daniel Castillo, Adrián Rubio, Dardo Goyeneche, Vladimir Juricic, y Anthul Rema por sus valiosos aportes interdisciplinarios.

📚 Referencias
Selberg, A. (1956). J. Indian Math. Soc. 20, 47.
DeWitt, B. S. (1967). Phys. Rev. 160, 1113.
Wald, R. M. (1993). Phys. Rev. D 48, 3427.
Glavan, D. & Lin, C. (2020). Phys. Rev. Lett. 124, 081301.
