# Análisis del Impacto de la Música en el Rendimiento Competitivo de Jugadores de Dota 2

Este proyecto forma parte del trabajo de titulación de la carrera de Ciencias de la Computación en la Universidad San Francisco de Quito. El objetivo principal es evaluar el efecto de la música en el desempeño de los jugadores de Dota 2 mediante el análisis de métricas clave de rendimiento utilizando técnicas de ciencia de datos y machine learning.

## Objetivos

### Objetivo general
Analizar si la música tiene impacto en el desempeño competitivo de los jugadores de Dota 2, evaluando su influencia en métricas clave de rendimiento en un entorno competitivo.

### Objetivos específicos
- Examinar cómo diferentes géneros musicales afectan los tiempos de reacción de los jugadores durante el juego.
- Evaluar la influencia de la música en la calidad de la toma de decisiones estratégicas en situaciones de alta presión.
- Comparar el desempeño entre jugadores que escuchan música y aquellos que no, considerando métricas de rendimiento específicas.
- Identificar correlaciones entre géneros musicales y parámetros de rendimiento, tales como acciones por minuto (APM) y tasas de victoria.

## Estructura del Proyecto

├── Data/
│ ├── Raw/ # Datos crudos extraídos de la API de OpenDota
│ ├── Processed/ # Datos limpios y listos para análisis
│ └── Surveys/ # Resultados de encuestas sobre hábitos musicales
│
├── Notebooks/
│ ├── 1_EDA.ipynb # Análisis exploratorio de datos
│ ├── 2_DataWrangling.ipynb # Limpieza y transformación de datos
│ ├── 3_FeatureEngineering.ipynb# Creación de nuevas métricas
│ └── 4_Modeling.ipynb # Entrenamiento y evaluación de modelos
│
├── Src/
│ ├── DataCollect.py # Extracción de datos desde la API
│ ├── DataWrangling.py # Limpieza y transformación de datos
│ └── FeatureEngineering.py # Creación de métricas personalizadas

## Cómo Ejecutar

1. Clona este repositorio:

   git clone https://github.com/N3pthys/Dota2-Performance-Music.git

2. Crea un entorno virtual y activa:

	python -m venv env
	source env/bin/activate 

3. Instala las dependencias:

	pip install -r requirements.txt

4. Ejecuta los scripts en scripts/ o explora los análisis en notebooks/.



## Herramientas Utilizadas

- Python 3.11

- pandas, numpy, matplotlib, seaborn

- scikit-learn, statsmodels, xgboost

- Google Colab Notebooks

