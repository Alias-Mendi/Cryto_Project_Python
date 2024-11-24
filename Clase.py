# Importamos las librerías necesarias 
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

### Clase Dataset
class Dataset:
    """
    Clase que representa un conjunto de datos de precios de activos financieros.
    Proporciona métodos para calcular indicadores técnicos como la SMA, Bandas de Bollinger y RSI.
    """

    def __init__(self, data):
        """
        Constructor de la clase Dataset.
        Recibe una lista con datos financieros y la convierte en un DataFrame de pandas.
        """
        # Convertimos los datos en un DataFrame
        df = pd.DataFrame(data)
        
        # Asignamos nombres a las columnas
        columns = ["timestamp", "open", "high", "low", "close", "vwap", "volume", "count"]
        df.columns = columns
        
        # Convertimos las columnas numéricas a tipo float
        df.close = df.close.astype(float)
        df.open = df.open.astype(float)
        df.high = df.high.astype(float)
        df.low = df.low.astype(float)
        df.vwap = df.vwap.astype(float)
        df.volume = df.volume.astype(float)
        
        # Convertimos el timestamp a formato de fecha
        df["Date"] = pd.to_datetime(df.timestamp, unit='s')
        
        # Eliminamos la columna timestamp ya que no la necesitamos
        df.drop('timestamp', axis=1, inplace=True)
        
        # Reiniciamos el índice para que sea consecutivo
        df.reset_index(drop=True, inplace=True)
        
        # Guardamos el DataFrame en el atributo 'data'
        self.data = df

    def print_data(self, n=5):
        """
        Imprime los primeros n registros del DataFrame. 
        Por defecto muestra 5 registros.
        """
        print(self.data.head(n))

    def calculate_sma_20(self):
        """
        Calcula la media móvil simple (SMA) de 20 periodos sobre la columna 'close'.
        """
        self.data['SMA'] = self.data['close'].rolling(window=20).mean()
    
    def calculate_volume_sma_20(self):
        """
        Calcula la media móvil simple (SMA) de 20 periodos sobre la columna 'volume'.
        """
        self.data['Volume_SMA'] = self.data['volume'].rolling(window=20).mean()

    def calculate_bollinger_bands(self):
        """
        Calcula las Bandas de Bollinger a partir de la SMA de 20 periodos.
        Las bandas se calculan como 2 desviaciones estándar por encima y por debajo de la SMA.
        """
        # Asegurarse de que se haya calculado la SMA de 20 periodos
        if 'SMA' not in self.data.columns:
            self.calculate_sma_20()
        
        # Inicializamos arrays para las bandas superior e inferior
        n = len(self.data)
        banda_superior = np.zeros(n)
        banda_inferior = np.zeros(n)
        sma_20 = self.data['SMA']
        
        # Cálculo de las bandas de Bollinger
        for i in range(20, n):
            banda_superior[i] = sma_20[i] + 1.8 * np.std(self.data['close'][i-20:i])  # Banda superior
            banda_inferior[i] = sma_20[i] - 1.8 * np.std(self.data['close'][i-20:i])  # Banda inferior   
        
        # Añadimos las bandas al DataFrame
        self.data["Banda_Superior"] = banda_superior
        self.data["Banda_Inferior"] = banda_inferior
        # Establecemos las primeras 19 filas como None (por falta de datos suficientes)
        self.data.loc[0:19, "Banda_Inferior"] = None
        self.data.loc[0:19, "Banda_Superior"] = None

    def calculate_RSI(self):
        """
        Calcula el Índice de Fuerza Relativa (RSI) con un periodo de 14.
        """
        periodo = 14
        # Calculamos la diferencia entre los precios de cierre consecutivos
        delta = self.data["close"].diff()
        
        # Obtenemos las ganancias (diferencias positivas) y pérdidas (diferencias negativas)
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        # Calculamos la media móvil de ganancias y pérdidas
        avg_gain = gain.rolling(window=periodo).mean()
        avg_loss = loss.rolling(window=periodo).mean()
        
        # Calculamos la razón de ganancias/pérdidas
        rs = avg_gain / avg_loss
        
        # Calculamos el RSI basado en la razón
        self.data['rsi'] = 100 - (100 / (1 + rs))

    def get_metrics(self):
        """
        Calcula y devuelve las métricas clave del DataFrame:
        - Media Móvil Simple (SMA 20)
        - Bandas de Bollinger
        - Índice de Fuerza Relativa (RSI)
        """
        self.calculate_RSI()
        self.calculate_sma_20()
        self.calculate_bollinger_bands()
        self.calculate_volume_sma_20()
        estrategia = Estrategia(self.data)
        estrategia.buy_signal()
        estrategia.sell_signal()
                

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

### Clase Grafico
class Grafico:
    """
    Clase que se encarga de generar gráficos para visualizar los datos financieros.
    Ofrece varios tipos de gráficos: gráficos de línea, gráficos de velas, y combinaciones con volumen.
    """

    def __init__(self, df, pair):
        """Constructor de la clase. Recibe un DataFrame con los datos financieros."""
        self.df = df
        self.pair = pair    
    
    def lineplot(self):
        """
        Genera un gráfico de líneas con:
        - Precio de cierre
        - Media Móvil Simple (SMA)
        - Bandas de Bollinger
        """
        # Evita que el gráfico se muestre en la consola (para WSL)
        matplotlib.use('Agg')

        # Estilo visual para el gráfico - modo oscuro ajustado
        plt.style.use("dark_background")

        # Crear figura
        plt.figure(figsize=(24, 12))

        # Añadir líneas al gráfico con colores más brillantes
        sns.lineplot(x=self.df.Date, y=self.df['close'], color='#82CAFA', label='Precio de cierre')  # Azul claro
        sns.lineplot(x=self.df.Date, y=self.df.SMA, label='SMA', color='#FF6F61', linewidth=2)  # Naranja claro
        sns.lineplot(x=self.df.Date, y=self.df.Banda_Superior, label='Bandas de Bollinger superior e inferior', color='#FFD700', linewidth=2)  # Amarillo
        sns.lineplot(x=self.df.Date, y=self.df.Banda_Inferior, color='#FFD700', linewidth=2)  # Amarillo

        # Representar señales de compra y venta con colores más visibles
        sns.scatterplot(x=self.df.Date[self.df['Buy_Signal'] == 1], y=self.df.close[self.df['Buy_Signal'] == 1], color='#00FF7F', s=100, marker='o', label='Compra')  # Verde brillante
        sns.scatterplot(x=self.df.Date[self.df['Sell_Signal'] == 1], y=self.df.close[self.df['Sell_Signal'] == 1], color='#FF6347', s=100, marker='o', label='Venta')  # Rojo tomate

        # Configurar etiquetas y leyenda
        plt.title(f'Evolución del precio de {self.pair} en Kraken', fontsize=20, color='white')
        plt.xlabel('Fecha y Hora', color='white')
        plt.ylabel('Precio', color='white')
        plt.legend(facecolor='black', frameon=True, fontsize=12)
        plt.grid(True, color='grey')
        plt.tight_layout()
        plt.xticks(rotation=45, color='white')
        plt.yticks(color='white')

        # Cambiar el fondo a gris oscuro en lugar de negro puro
        plt.gca().set_facecolor('#2E2E2E')

        # En lugar de guardar, devolvemos la figura
        return plt.gcf()

    def lineplot_with_volume(self):
        """
        Genera un gráfico de líneas con dos subplots:
        - Subplot 1: Precio de cierre, SMA y Bandas de Bollinger
        - Subplot 2: Volumen de transacciones
        """
        # Estilo visual para el gráfico - modo oscuro ajustado
        plt.style.use("dark_background")
        fig, axs = plt.subplots(2, figsize=(24, 12))
        fig.suptitle(f'Evolución del precio y volumen de {self.pair} en Kraken', color='white')

        # Subplot 1: Gráfico de líneas del precio
        sns.lineplot(ax=axs[0], x=self.df.Date, y=self.df['close'], color='#82CAFA', label='Precio de cierre', linewidth=2)
        sns.lineplot(ax=axs[0], x=self.df.Date, y=self.df.SMA, label='SMA_20', color='#FF6F61', linewidth=2)
        sns.lineplot(ax=axs[0], x=self.df.Date, y=self.df.Banda_Superior, label='Bandas de Bollinger superior e inferior', color='#FFD700', linewidth=2)
        sns.lineplot(ax=axs[0], x=self.df.Date, y=self.df.Banda_Inferior, color='#FFD700', linewidth=2)

        # Subplot 2: Gráfico de barras del volumen
        axs[1].set_title('Volumen de operaciones', fontsize=20, color='white')
        axs[1].bar(self.df.Date, self.df.volume, color='#6495ED', label='Volumen', width=0.05)  # Azul
        sns.lineplot(ax=axs[1], x=self.df.Date, y=self.df.Volume_SMA, label='SMA de volumen', color='red', linewidth=2)

        # Representar señales de compra y venta en el subplot 1
        axs[0].scatter(self.df.Date[self.df['Buy_Signal'] == 1], self.df.close[self.df['Buy_Signal'] == 1], color='#00FF7F', marker='o', label='Compra')  # Verde brillante
        axs[0].scatter(self.df.Date[self.df['Sell_Signal'] == 1], self.df.close[self.df['Sell_Signal'] == 1], color='#FF6347', marker='o', label='Venta')  # Rojo tomate

        # Mostrar leyendas con fondo oscuro
        axs[0].legend(loc='upper left', facecolor='black', frameon=True, fontsize=12)
        axs[1].legend(loc='upper right', facecolor='black', frameon=True, fontsize=12)

        # Ajuste final para que el modo oscuro se vea bien
        for ax in axs:
            ax.set_facecolor('#2E2E2E')  # Fondo gris oscuro
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')

        axs[0].grid(True, color='grey')  # Cuadrícula gris en el gráfico de precio
        axs[1].grid(True, color='grey')  # Cuadrícula gris en el gráfico de volumen

        plt.xticks(rotation=45, color='white')
        plt.tight_layout()

        # En lugar de guardar, devolvemos la figura
        return fig


    def candlestick(self):
        """
        Genera un gráfico de velas japonés (candlestick chart), mostrando:
        - Precios de apertura, cierre, máximo y mínimo.
        - Media Móvil Simple (SMA)
        - Bandas de Bollinger
        """
        # Estilo visual para el gráfico - modo oscuro ajustado
        plt.style.use("dark_background")
        plt.figure(figsize=(24, 12))

        # Dibujar cada vela con colores brillantes
        for i in range(len(self.df)):
            color = '#00FF7F' if self.df.close[i] > self.df.open[i] else '#FF6347'  # Verde brillante o rojo tomate
            plt.plot([self.df.Date[i], self.df.Date[i]], [self.df.open[i], self.df.close[i]], color=color, linewidth=0.5)
            plt.plot([self.df.Date[i], self.df.Date[i]], [self.df.low[i], self.df.open[i]], color='white', linewidth=0.1)
            plt.plot([self.df.Date[i], self.df.Date[i]], [self.df.high[i], self.df.close[i]], color='white', linewidth=0.1)

        # Añadir líneas de SMA y Bandas de Bollinger
        sns.lineplot(x=self.df.Date, y=self.df.SMA, label='SMA', color='#FF6F61', linewidth=2)  # Naranja claro
        sns.lineplot(x=self.df.Date, y=self.df.Banda_Superior, label='Bandas de Bollinger superior e inferior', color='#FFD700', linewidth=2)  # Amarillo
        sns.lineplot(x=self.df.Date, y=self.df.Banda_Inferior, color='#FFD700', linewidth=2)  # Amarillo

        # Representar señales de compra y venta
        sns.scatterplot(x=self.df.Date[self.df['Buy_Signal'] == 1], y=self.df.close[self.df['Buy_Signal'] == 1], color='#00FF7F', s=100, marker='o', label='Compra')  # Verde brillante
        sns.scatterplot(x=self.df.Date[self.df['Sell_Signal'] == 1], y=self.df.close[self.df['Sell_Signal'] == 1], color='#FF6347', s=100, marker='o', label='Venta')  # Rojo tomate

        # Configurar etiquetas y leyenda
        plt.title(f'Evolución del precio de {self.pair} en Kraken', fontsize=20, color='white')
        plt.xlabel('Fecha', color='white')
        plt.ylabel('Precio', color='white')
        plt.grid(True, color='grey')  # Cuadrícula gris
        plt.xticks(rotation=45, color='white')
        plt.yticks(color='white')
        plt.legend(facecolor='black', frameon=True)
        plt.tight_layout()

        # Cambiar el fondo a gris oscuro en lugar de negro puro
        plt.gca().set_facecolor('#2E2E2E')

        # En lugar de guardar, devolvemos la figura
        return plt.gcf()

    def candlestick_with_volume(self):
        """
        Genera un gráfico de velas japonés con volumen en dos subplots:
        - Subplot 1: Gráfico de velas, SMA y Bandas de Bollinger
        - Subplot 2: Gráfico de barras con el volumen
        """
        # Estilo visual para el gráfico - modo oscuro ajustado
        plt.style.use("dark_background")
        fig, axs = plt.subplots(2, figsize=(24, 12))

        # Dibujar las velas en el subplot 1
        for i in range(len(self.df)):
            color = '#00FF7F' if self.df.close[i] > self.df.open[i] else '#FF6347'  # Verde brillante o rojo tomate
            axs[0].plot([self.df.Date[i], self.df.Date[i]], [self.df.open[i], self.df.close[i]], color=color, linewidth=0.5)
            axs[0].plot([self.df.Date[i], self.df.Date[i]], [self.df.low[i], self.df.open[i]], color='white', linewidth=0.1)
            axs[0].plot([self.df.Date[i], self.df.Date[i]], [self.df.high[i], self.df.close[i]], color='white', linewidth=0.1)

        # Añadir líneas de SMA y Bandas de Bollinger en el subplot 1
        sns.lineplot(x=self.df.Date, y=self.df.SMA, label='SMA', color='#FF6F61', linewidth=2, ax=axs[0])  # Naranja claro
        sns.lineplot(x=self.df.Date, y=self.df.Banda_Superior, label='Bandas de Bollinger superior e inferior', color='#FFD700', linewidth=2, ax=axs[0])  # Amarillo
        sns.lineplot(x=self.df.Date, y=self.df.Banda_Inferior, color='#FFD700', linewidth=2, ax=axs[0])  # Amarillo

        # Subplot 2: Volumen en gráfico de barras con SMA de volumen
        axs[1].set_title('Volumen de operaciones', fontsize=20, color='white')
        axs[1].bar(self.df.Date, self.df.volume, color='#6495ED', label='Volumen', width=0.05)  # Azul
        sns.lineplot(x=self.df.Date, y=self.df.Volume_SMA, label='SMA de volumen', color='red', linewidth=2, ax=axs[1])

        # Mostrar señales de compra y venta en el subplot 1
        axs[0].scatter(self.df.Date[self.df['Buy_Signal'] == 1], self.df.close[self.df['Buy_Signal'] == 1], color='#00FF7F', marker='o', label='Compra')  # Verde brillante
        axs[0].scatter(self.df.Date[self.df['Sell_Signal'] == 1], self.df.close[self.df['Sell_Signal'] == 1], color='#FF6347', marker='o', label='Venta')  # Rojo tomate

        # Configurar etiquetas y leyendas
        axs[0].set_title(f'Evolución del precio de {self.pair} en Kraken', fontsize=20, color='white')
        axs[0].set_xlabel('Fecha', color='white')
        axs[0].set_ylabel('Precio', color='white')
        axs[0].grid(True, color='grey')  # Cuadrícula gris

        # Ajustar el subplot 2
        axs[1].tick_params(colors='white')
        axs[1].xaxis.label.set_color('white')
        axs[1].yaxis.label.set_color('white')
        axs[1].grid(True, color='grey')  # Cuadrícula gris también en el volumen

        # Ajuste final para que el modo oscuro se vea bien
        for ax in axs:
            ax.set_facecolor('#2E2E2E')  # Fondo gris oscuro en lugar de negro

        plt.xticks(rotation=45, color='white')
        plt.tight_layout()

        # En lugar de guardar, devolvemos la figura
        return fig

### Clase Estrategia (para futuros desarrollos)
class Estrategia:
    """
    ### Clase Estrategia:

    La clase Estrategia implementa dos métodos principales: **buy_signal** y **sell_signal**. 
    Cada uno de estos métodos genera señales de compra o venta basadas en indicadores técnicos clave como las **Bandas de Bollinger** y el **Volumen**.
    """

    def __init__(self, df):
        """Constructor de la clase. Recibe un DataFrame con los datos financieros."""
        self.df = df

    def buy_signal(self):
        """
        Estrategia de Compra: 
        Genera señales de compra basadas en las Bandas de Bollinger y el volumen.
        """
        n = len(self.df)
        self.df['Buy_Signal'] = None

        for i in range(20, n):
            if self.df['close'][i] < self.df['Banda_Inferior'][i] and self.df['volume'][i] > self.df['Volume_SMA'][i] and self.df['close'][i] > self.df['close'][i-1]:
                self.df['Buy_Signal'][i] = 1
            elif self.df['close'][i] <= self.df['Banda_Inferior'][i] and self.df['volume'][i] < self.df['Volume_SMA'][i]:
                self.df['Buy_Signal'][i] = 1

    def sell_signal(self):
        """
        Estrategia de Venta: 
        Genera señales de venta basadas en las Bandas de Bollinger y el volumen.
        """
        n = len(self.df)
        self.df['Sell_Signal'] = None
        for i in range(20, n):
            if self.df['close'][i] > self.df['Banda_Superior'][i] and self.df['volume'][i] > self.df['Volume_SMA'][i] and self.df['close'][i] < self.df['close'][i-1]:
                self.df['Sell_Signal'][i] = 1
            elif self.df['close'][i] >= self.df['Banda_Superior'][i] and self.df['volume'][i] < self.df['Volume_SMA'][i]:
                self.df['Sell_Signal'][i] = 1
