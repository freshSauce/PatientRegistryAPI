from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer


from routers import patients_router, doctors_router, auth_router

app = FastAPI(title="Patient Registry API", description="API that allows intercomunication with healthcare centres, "
                                                        "storing patients information in one single database")
app.include_router(patients_router)
app.include_router(doctors_router)
app.include_router(auth_router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")