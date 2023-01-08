from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from client import routes as userRouter
from client.order import router_order as orderRouter

app = FastAPI()

app.include_router(userRouter.router)
app.include_router(orderRouter.router)


origins = [
    "http://localhost:3000",
    "https://frontend-pizza-ehrg.vercel.app",
    "*"
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

