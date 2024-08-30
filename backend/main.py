from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update this with the correct frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a Note model
class Note(BaseModel):
    id: int
    title: str
    content: str

# In-memory database for demonstration purposes
notes_db = []

@app.get("/notes", response_model=List[Note])
def get_notes():
    return notes_db

@app.post("/notes", response_model=Note)
def create_note(note: Note):
    notes_db.append(note)
    return note

@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, note: Note):
    for n in notes_db:
        if n.id == note_id:
            n.title = note.title
            n.content = note.content
            return n
    return {"error": "Note not found"}

@app.delete("/notes/{note_id}", response_model=dict)
def delete_note(note_id: int):
    global notes_db
    notes_db = [note for note in notes_db if note.id != note_id]
    return {"message": "Note deleted successfully"}



# python -m venv venv
# venv\Scripts\activate