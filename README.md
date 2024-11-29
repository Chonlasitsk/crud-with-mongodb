# Simple CRUD with mongoDB
### tools stack:
  - Web Framework: [FastAPI](https://fastapi.tiangolo.com/) 🚀
  - Driver: [Motor](https://www.mongodb.com/docs/drivers/motor/) (MongoDB driver for asynchronous Python applications) 🏄 [docs](https://motor.readthedocs.io/en/stable/) 📄
  - ODM: [Beanie](https://beanie-odm.dev/) (asynchronous Python object-document mapper (ODM) for MongoDB) 🌤️

### Run application
```bash
uvicorn simplecrudapi.main:app --port 8000 --reload (for development)
```

### Run mongodb using docker
```bash
docker compose up -d
```
