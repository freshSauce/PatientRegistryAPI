from fastapi import FastAPI
from routers import patients_router

app = FastAPI(title="Patient Registry API", description="API that allows intercomunication with health centres, "
                                                        "storing patients information in one single database")
app.include_router(patients_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
