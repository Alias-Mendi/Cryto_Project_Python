# Visualización y Análisis Técnico de Precios de Activos en Kraken

Este proyecto es una aplicación para analizar y visualizar datos financieros obtenidos de Kraken, utilizando indicadores técnicos como la Media Móvil Simple (SMA), Bandas de Bollinger y el Índice de Fuerza Relativa (RSI). La aplicación está desarrollada en Python y ofrece dos modos de uso: mediante una interfaz gráfica web desarrollada con `Streamlit` o desde la línea de comandos. La aplicación se conecta a la API pública de Kraken para obtener datos de mercado en tiempo real y generar gráficos interactivos o estáticos.

## Características

- **Cálculo de indicadores técnicos**:
  - Media Móvil Simple (SMA) de 20 periodos.
  - Bandas de Bollinger.
  - Índice de Fuerza Relativa (RSI).
  - SMA de volumen.

- **Generación de señales de compra/venta**:
  - Basado en Bandas de Bollinger, volumen y el comportamiento del precio.

- **Visualización gráfica**:
  - Gráficos de líneas y velas japonesas.
  - Visualización de volumen junto con precios.
  - Gráficos interactivos (en la aplicación web) o estáticos (en la línea de comandos).

- **Integración con la API de Kraken**:
  - Obtención de datos en tiempo real para varios pares de criptomonedas.

## Requisitos

Para ejecutar este proyecto, necesitarás instalar las siguientes dependencias:

- `pandas`
- `numpy`
- `seaborn`
- `matplotlib`
- `mplfinance`
- `krakenex`
- `streamlit`

Puedes instalar las dependencias usando `pip` a través del archivo `requirements.txt`.

## Instalación

Sigue estos pasos para configurar el proyecto en tu entorno local:

1. **Clonar el repositorio**:

    ```bash
    git clone https://github.com/Alias-Mendi/Crypto_Project.git
    cd Crypto_Project
    ```

2. **Crear un entorno virtual (opcional pero recomendado)**:

    ```bash
    conda create -n nombre_entorno
    conda activate nombre_entorno
    ```

3. **Instalar las dependencias**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configurar las credenciales de Kraken**:

    Crea un archivo llamado `kraken.key` en el directorio raíz del proyecto y agrega tus credenciales de API de Kraken en el siguiente formato:

    ```
    key=TU_API_KEY
    secret=TU_API_SECRET
    ```

## Ejecución

### Opción 1: Ejecutar el script desde la terminal

Puedes ejecutar el archivo principal (`main.py`) para obtener datos y generar gráficos directamente desde la línea de comandos.

1. **Ejecutar el script principal**:

    ```bash
    python main.py
    ```

2. **Seleccionar el par de criptomonedas**:

    Elige entre los siguientes pares al ejecutar el script:
    - BTC / USD
    - ETH / USD
    - ETH / BTC
    - ADA / USD
    - DOT / USD
    - SOL / USD
    - XRP / USD
    - LTC / USD

El script descargará los datos del par seleccionado, calculará los indicadores técnicos, generará gráficos y guardará los resultados en archivos PNG. Los gráficos incluyen:

- **Gráfico de líneas con SMA y Bandas de Bollinger**.
- **Gráfico de líneas con volumen**.
- **Gráfico de velas japonesas**.
- **Gráfico de velas japonesas con volumen**.

### Opción 2: Ejecutar la aplicación con Streamlit

Puedes ejecutar una interfaz gráfica interactiva utilizando `Streamlit` para visualizar los gráficos en tiempo real.

1. **Ejecutar la aplicación de Streamlit**:

    ```bash
    streamlit run app.py
    ```

2. **Interacción en la interfaz**:

   - Selecciona el par de criptomonedas desde el menú desplegable en la barra lateral.
   - Genera gráficos de líneas, velas japonesas y volumen directamente desde la aplicación.
   - Los gráficos interactivos permiten ampliar y analizar diferentes puntos de datos de forma dinámica.

## Uso

Una vez que la aplicación esté en funcionamiento (tanto en la interfaz web como desde la terminal), puedes seleccionar diferentes pares de criptomonedas (BTC/USD, ETH/USD, ADA/USD, etc.) y visualizar los siguientes gráficos con indicadores técnicos:

- **Gráfico de líneas**: Muestra la evolución del precio de cierre junto con la SMA y las Bandas de Bollinger.
- **Gráfico de velas japonesas**: Visualiza los precios de apertura, cierre, máximo y mínimo en forma de velas japonesas.
- **Gráfico con volumen**: Añade información sobre el volumen de operaciones al gráfico de precios.

En la interfaz de `Streamlit`, además de visualizar los gráficos, puedes interactuar con los datos mediante expansores que muestran los datos en bruto.

## Estructura del Proyecto

├── Clase.py # Contiene las clases Dataset, Estrategia y Grafico.

├── main.py # Script principal para ejecutar desde la terminal. 
 
├── app.py # Aplicación Streamlit para la interfaz web.

├── requirements.txt # Archivo con las dependencias del proyecto.

├── kraken.key # Archivo que almacena las credenciales de la API de Kraken (no incluido).

└── README.md # Documentación del proyecto.


## Futuras Mejoras

- Añadir más indicadores técnicos (MACD, RSI más personalizados, etc.).
- Implementar estrategias de trading más avanzadas y automatizadas.
- Permitir la descarga de gráficos generados directamente desde la interfaz web.
- Soporte para más intervalos de tiempo en los datos de Kraken.

## Créditos

Este proyecto fue desarrollado por **Carlos Mendizabal**. Si tienes alguna pregunta o sugerencia, no dudes en ponerte en contacto.

