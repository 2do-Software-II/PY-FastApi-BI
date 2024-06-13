from fastapi import FastAPI, HTTPException
from graphql_client import query_graphql
from typing import List
from pydantic import BaseModel
import pandas as pd

# Path: main.py
app = FastAPI()

# class
class Room(BaseModel):
    nroRoom: str
    id: str

class Booking(BaseModel):
    checkIn: str
    checkOut: str
    date: str
    endDate: str
    fullPayment: float
    id: str
    paymentMethod: str
    prePaid: float
    startDate: str
    status: str
    time: str
    room: Room

# Controllers
@app.get("/api/op")
async def get_data():
    graphql_query = """
    query {
        getAllRoles {
            description
            id
            name
        }
    }
    """

    try:
        graphql_response = await query_graphql(graphql_query)
        data = graphql_response.get('data', {}).get('getAllRoles')
        if not data:
            raise HTTPException(status_code=404, detail="Data not found")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/one")
async def calculate_payments():
    graphql_query = """
            query {
                 getAllBookings {
                    checkIn
                    checkOut
                    date
                    endDate
                    fullPayment
                    id
                    paymentMethod
                    prePaid
                    startDate
                    status
                    time
                    room {
                    nroRoom
                    id
                    }
                }
            }
    """
    try:
        graphql_response = await query_graphql(graphql_query)
        data = graphql_response.get('data', {}).get('getAllBookings')
        # Convertir los datos a un DataFrame de pandas
        df = pd.DataFrame(data)

        # Convertir la columna 'date' a tipo datetime
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

        # Agrupar por fecha y calcular el monto acumulado de 'fullPayment'
        grouped = df.groupby('date')['fullPayment'].sum().reset_index()

        # Convertir el resultado a formato JSON compatible con FastAPI
        result = grouped.to_dict(orient='records')

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/two")
async def calculate_payments():
    graphql_query = """
            query {
                 getAllBookings {
                    checkIn
                    checkOut
                    date
                    endDate
                    fullPayment
                    id
                    paymentMethod
                    prePaid
                    startDate
                    status
                    time
                    room {
                    nroRoom
                    id
                    }
                }
            }
    """
    try:
        graphql_response = await query_graphql(graphql_query)
        data = graphql_response.get('data', {}).get('getAllBookings')
        df = pd.DataFrame(data)
         # Convertir la columna 'date' a tipo datetime
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
        
        # Agregar una columna para el mes
        df['month'] = df['date'].dt.to_period('M')  # Agrupa por mes
        
        # Obtener el número del mes como entero
        df['monthNumber'] = df['month'].dt.month

        grouped = df.groupby(['month', 'monthNumber'])['fullPayment'].sum().reset_index()
        
        # Convertir el resultado a formato JSON compatible con FastAPI
        result = grouped.to_dict(orient='records')
        
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/three")
async def count_bookings_per_room():
    graphql_query = """
            query {
                 getAllBookings {
                    checkIn
                    checkOut
                    date
                    endDate
                    fullPayment
                    id
                    paymentMethod
                    prePaid
                    startDate
                    status
                    time
                    room {
                        nroRoom
                        id
                    }
                }
            }
    """
    try:
        # Simulamos la llamada a la función query_graphql para obtener los datos
        graphql_response = await query_graphql(graphql_query)
        data = graphql_response.get('data', {}).get('getAllBookings', [])

        # Convertir los datos a un DataFrame de pandas
        df = pd.DataFrame(data)

        # Convertir la columna 'date' a tipo datetime
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

        # Agregar una columna para el mes
        df['month'] = df['date'].dt.to_period('M')  # Agrupa por mes

        df['monthNumber'] = df['month'].dt.month

        # Contar la cantidad de reservas por mes
        grouped = df.groupby(['month', 'monthNumber']).size().reset_index(name='reservationCount')

        # Convertir el resultado a formato JSON compatible con FastAPI
        result = grouped.to_dict(orient='records')

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Services


# Path: main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
