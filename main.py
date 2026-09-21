from fastapi import FastAPI, Depends, HTTPException   # Used to create your application, Used for dependency injection, Used when you want to return an HTTP error.
from schemas import Todo as TodoSchema, TodoCreate
from sqlalchemy.orm import Session  #Session represents a connection/session through which SQLAlchemy communicates with your database.
from database import SessionLocal, Base, engine
from models import Todo
import httpx
import time
import asyncio

app = FastAPI()
Base.metadata.create_all(bind=engine)  #Create database tables

app = FastAPI()  #creates your FastAPI application.

#dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db  #giving the database session to the API endpoint.
    finally:
        db.close()  #After the request finishes, FastAPI closes the database session.

# POST - Create TODO
@app.post("/todos", response_model=TodoSchema)
def create(todo: TodoCreate, db: Session= Depends(get_db)):  #FastAPI expects the request body to follow the TodoCreate schema.
    db_todo = Todo(**todo.dict())  #Convert Pydantic data into SQLAlchemy model, The ** operator unpacks the dictionary.
    db.add(db_todo)  #Add the Todo to database session
    db.commit() #This commits the transaction.
    db.refresh(db_todo)  #This reloads the object from the database. This is particularly useful because the database generates the ID.
    return db_todo  #FastAPI converts the SQLAlchemy object into the response schema

#GET = All TODOS
@app.get("/todos", response_model=list[TodoSchema])
def read_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()


#GET = Single TODOS
@app.get("/todo/{todo_id}", response_model=TodoSchema)
def read_todo(todo_id: int,db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found") 
    return todo

#PUT - Update Todo
@app.put("/todos/{todo_id}",response_model=TodoSchema)
def update_todo(todo_id:int, updated: TodoCreate, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in updated.dict().items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo

#DELETE - Delete todo
@app.delete("/todo/{todo_id}")
def delete_todo(todo_id:int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo Deleted Successfully"}




JOKE_URL = "https://official-joke-api.appspot.com/random_joke"

@app.get("/jokes-sync")
def get_jokes_sync():
    start = time.time()
    jokes = []
    with httpx.Client() as client:
        for _ in range(10):
            resp = client.get(JOKE_URL)
            data = resp.json()
            jokes.append(f"{data['setup']} - {data['punchline']}")
    elapsed = time.time() - start

    return {
        "mode": "sync",
        "elapsed_time_sec": round(elapsed, 3),
        "jokes": jokes,
    }

@app.get("/jokes-async")
async def get_jokes_async():
    start = time.time()
    jokes = []
    async with httpx.AsyncClient() as client:
        tasks = [client.get(JOKE_URL) for _ in range(10)]
        responses = await asyncio.gather(*tasks)

        for resp in responses:
            data = resp.json()
            jokes.append(f"{data['setup']} - {data['punchline']}")
    
    elapsed = time.time() - start

    return {
        "mode": "async",
        "elapsed_time_sec": round(elapsed, 3),
        "jokes": jokes,
    }