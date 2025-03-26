from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

class MyWrapper(EWrapper):
    def __init__(self):
        self.datos_list = []
        self.datos = None
        
    def nextValidId(self, orderId:int):
        print("Comienza la petición con Id:", orderId)
        self.start()
    
    def historicalData(self, reqId, bar):
        # Por cada linea vamos sacando las variables y
        # añadiéndola a la lista
        self.datos_list.append(vars(bar));
        
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        # Al finalizar ponemos los datos en formato dataframe,
        # la fecha en formato datetime y la ponemos como indice
        print("Final. ReqId:", reqId, "(", start, "/", end,")")
        self.datos = pd.DataFrame(self.datos_list)
        self.datos['date'] = pd.to_datetime(self.datos['date'])
        self.datos.set_index('date', inplace=True)
        app.disconnect()
        
    def error(self, reqId, errorCode, errorString):
        # Mostramos los mensajes que devuelve el IB Gateway
        print(errorString," (Id:", reqId, " Code:", errorCode,")")

    def start(self):        
        # Creamos en contrato
        contrato = Contract()
        contrato.symbol = "SPY"
        contrato.secType = "STK" 
        contrato.currency = "USD"
        contrato.exchange = "ARCA"
        
        # Hacemos la petición de los datos
        app.reqHistoricalData(1, contrato, "", "30 Y", "4 hours", "MIDPOINT", 0, 1, False, [])

wrap = MyWrapper()
app = EClient(wrap)
app.connect("127.0.0.1", 4002, clientId=1)
app.run()

wrap.datos

plt.show()  # <- Esto abre la ventana con el gráfico
