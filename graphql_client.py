import httpx

async def query_graphql(query):
    url = 'https://jv-gateway-production.up.railway.app/graphql'  # Reemplaza con la URL de tu API GraphQL
    headers = {
        'Content-Type': 'application/json',
    }
    timeout = None 
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(url, json={'query': query}, headers=headers)

    return response.json()  
