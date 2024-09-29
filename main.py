from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer


from routers import patients_router, doctors_router, auth_router
from dependencies import get_current_user

app = FastAPI(title="Patient Registry API", description="API that allows intercomunication with healthcare centres, "
                                                        "storing patients information in one single database")


app.include_router(patients_router, dependencies=[Depends(get_current_user)])
app.include_router(doctors_router, dependencies=[Depends(get_current_user)])
app.include_router(auth_router)



@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")