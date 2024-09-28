from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routers import patients_router

app = FastAPI(title="Patient Registry API", description="API that allows intercomunication with healthcare centres, "
                                                        "storing patients information in one single database")
app.include_router(patients_router)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")