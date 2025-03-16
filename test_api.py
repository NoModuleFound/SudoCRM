from backend.api.routers import all_routers
from fastapi import FastAPI
import uvicorn

app = FastAPI()

for router in all_routers:
  app.include_router(router)

if __name__ == '__main__':
  uvicorn.run('test_api:app', host='127.0.0.1', port=8080, reload=True)