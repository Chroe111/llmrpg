import os

import uvicorn

from app.logic import app


if __name__ == "__main__":
    uvicorn.run(app)
