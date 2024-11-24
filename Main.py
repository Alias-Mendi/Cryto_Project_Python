import pandas as pd
import krakenex
import matplotlib.pyplot as plt
from Clase import Dataset, Grafico
import os
import dotenv

# Conectar a la API de Kraken
dotenv.load_dotenv()
k = krakenex.API(os.getenv('KRAKEN_KEY'))
i = True

# Función para guardar gráficos
def guardar_grafico(figura, nombre):
    """Guarda una figura en un archivo con el nombre dado."""
    figura.savefig(f"{nombre}.png", dpi=300)
    plt.close(figura)  # Cerramos la figura para evitar acumulación de memoria

while i == True:
    print("Selecciona la moneda que quiere representar:\n"
          "1. BTC / USD\n"
          "2. ETH / USD\n"
          "3. ETH / BTC\n"
          "4. ADA / USD\n"
          "5. DOT / USD\n"
          "6. SOL / USD\n"
          "7. XRP / USD\n"
          "8. LTC / USD\n")
    
    opcion = int(input("Introduce el número de la moneda que quieres representar: "))

    if opcion == 1:
        data = k.query_public('OHLC', {'pair': 'XXBTZUSD', 'interval': 60})
        datos = data['result']['XXBTZUSD']  
        pair = 'BTC/USD'
        df = Dataset(datos)
        df.get_metrics()
        df.print_data(200)
        
        # Generar gráficos
        grafico = Grafico(df.data, pair)
        fig = grafico.lineplot()
        guardar_grafico(fig, 'BTCUSD_Lineplot')
        fig = grafico.lineplot_with_volume()
        guardar_grafico(fig, 'BTCUSD_Lineplot_Volumen')
        fig = grafico.candlestick()
        guardar_grafico(fig, 'BTCUSD_Candlestick')
        fig = grafico.candlestick_with_volume()
        guardar_grafico(fig, 'BTCUSD_Candlestick_Volumen')
        break

    elif opcion == 2:
        data = k.query_public('OHLC', {'pair': 'XETHZUSD', 'interval': 60})
        datos = data['result']['XETHZUSD']
        pair = 'ETH/USD'
        df = Dataset(datos)
        df.get_metrics()
        df.print_data(200)
        
        # Generar gráficos
        grafico = Grafico(df.data, pair)
        fig = grafico.lineplot()
        guardar_grafico(fig, 'ETHUSD_Lineplot')
        fig = grafico.lineplot_with_volume()
        guardar_grafico(fig, 'ETHUSD_Lineplot_Volumen')
        fig = grafico.candlestick()
        guardar_grafico(fig, 'ETHUSD_Candlestick')
        fig = grafico.candlestick_with_volume()
        guardar_grafico(fig, 'ETHUSD_Candlestick_Volumen')
        break

    elif opcion == 3:
        data = k.query_public('OHLC', {'pair': 'XETHXXBT', 'interval': 60})
        datos = data['result']['XETHXXBT']
        pair = 'ETH/BTC'
        df = Dataset(datos)
        df.get_metrics()
        df.print_data(200)
        
        # Generar gráficos
        grafico = Grafico(df.data, pair)
        fig = grafico.lineplot()
        guardar_grafico(fig, 'ETHBTC_Lineplot')
        fig = grafico.lineplot_with_volume()
        guardar_grafico(fig, 'ETHBTC_Lineplot_Volumen')
        fig = grafico.candlestick()
        guardar_grafico(fig, 'ETHBTC_Candlestick')
        fig = grafico.candlestick_with_volume()
        guardar_grafico(fig, 'ETHBTC_Candlestick_Volumen')
        break

    elif opcion == 4:
        data = k.query_public('OHLC', {'pair': 'ADAUSD', 'interval': 60})
        datos = data['result']['ADAUSD']
        pair = 'ADA/USD'
        df = Dataset(datos)
        df.get_metrics()
        df.print_data(200)
        
        # Generar gráficos
        grafico = Grafico(df.data, pair)
        fig = grafico.lineplot()
        guardar_grafico(fig, 'ADAUSD_Lineplot')
        fig = grafico.lineplot_with_volume()
        guardar_grafico(fig, 'ADAUSD_Lineplot_Volumen')
        fig = grafico.candlestick()
        guardar_grafico(fig, 'ADAUSD_Candlestick')
        fig = grafico.candlestick_with_volume()
        guardar_grafico(fig, 'ADAUSD_Candlestick_Volumen')
        break

    elif opcion == 5:
        data = k.query_public('OHLC', {'pair': 'DOTUSD', 'interval': 60})
        datos = data['result']['DOTUSD']
        pair = 'DOT/USD'
        df = Dataset(datos)
        df.get_metrics()
        df.print_data(200)
        
        # Generar gráficos
        grafico = Grafico(df.data, pair)
        fig = grafico.lineplot()
        guardar_grafico(fig, 'DOTUSD_Lineplot')
        fig = grafico.lineplot_with_volume()
        guardar_grafico(fig, 'DOTUSD_Lineplot_Volumen')
        fig = grafico.candlestick()
        guardar_grafico(fig, 'DOTUSD_Candlestick')
        fig = grafico.candlestick_with_volume()
        guardar_grafico(fig, 'DOTUSD_Candlestick_Volumen')
        break

    elif opcion == 6:
        data = k.query_public('OHLC', {'pair': 'SOLUSD', 'interval': 60})
        datos = data['result']['SOLUSD']
        pair = 'SOL/USD'
        df = Dataset(datos)
        df.get_metrics()
        df.print_data(200)
        
        # Generar gráficos
        grafico = Grafico(df.data, pair)
        fig = grafico.lineplot()
        guardar_grafico(fig, 'SOLUSD_Lineplot')
        fig = grafico.lineplot_with_volume()
        guardar_grafico(fig, 'SOLUSD_Lineplot_Volumen')
        fig = grafico.candlestick()
        guardar_grafico(fig, 'SOLUSD_Candlestick')
        fig = grafico.candlestick_with_volume()
        guardar_grafico(fig, 'SOLUSD_Candlestick_Volumen')
        break

    elif opcion == 7:
        data = k.query_public('OHLC', {'pair': 'XXRPZUSD', 'interval': 60})
        datos = data['result']['XXRPZUSD']
        pair = 'XRP/USD'
        df = Dataset(datos)
        df.get_metrics()
        df.print_data(200)
        
        # Generar gráficos
        grafico = Grafico(df.data, pair)
        fig = grafico.lineplot()
        guardar_grafico(fig, 'XRPUSD_Lineplot')
        fig = grafico.lineplot_with_volume()
        guardar_grafico(fig, 'XRPUSD_Lineplot_Volumen')
        fig = grafico.candlestick()
        guardar_grafico(fig, 'XRPUSD_Candlestick')
        fig = grafico.candlestick_with_volume()
        guardar_grafico(fig, 'XRPUSD_Candlestick_Volumen')
        break

    elif opcion == 8:
        data = k.query_public('OHLC', {'pair': 'XLTCZUSD', 'interval': 60})
        datos = data['result']['XLTCZUSD']
        pair = 'LTC/USD'
        df = Dataset(datos)
        df.get_metrics()
        df.print_data(200)
        
        # Generar gráficos
        grafico = Grafico(df.data, pair)
        fig = grafico.lineplot()
        guardar_grafico(fig, 'LTCUSD_Lineplot')
        fig = grafico.lineplot_with_volume()
        guardar_grafico(fig, 'LTCUSD_Lineplot_Volumen')
        fig = grafico.candlestick()
        guardar_grafico(fig, 'LTCUSD_Candlestick')
        fig = grafico.candlestick_with_volume()
        guardar_grafico(fig, 'LTCUSD_Candlestick_Volumen')
        break

    else:
        print("Opción no válida")
