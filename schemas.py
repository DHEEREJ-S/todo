from pydantic import BaseModel

class TodoBase(BaseModel):
    title:str
    description:str | None = None
    completed: bool = False


class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    class Config:
        from_attributes = True #tells Pydantic: You are allowed to create this Pydantic model by reading attributes from an object, not only from a dictionary.