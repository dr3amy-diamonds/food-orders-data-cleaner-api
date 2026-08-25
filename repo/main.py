from fastapi import FastAPI

app = FastAPI(title='API Pedidos')

@app.get('/salud')
def salud():
    return {'estado': 'OK'}
