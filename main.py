import json
from fastapi import FastAPI

from models import Composer, Pieces


app = FastAPI()

with open("composers.json", "r") as f:
    composers_list: list[dict] = json.load(f)

with open("pieces.json", "r") as f:
    piece_list: list[dict] = json.load(f)

composers: list[Composer] = []
pieces: list[Pieces] = []

for composer in composers_list:
    composers.append(Composer(**composer))

for piece in piece_list:
    pieces.append(Pieces(**piece))

@app.get("/composers")
async def list_composers() -> list[Composer]:
    return composers

@app.get("/pieces")
async def list_pieces() -> list[Pieces]:
    return pieces

@app.post("/composers")
async def create_composer(new_composer: Composer):
    composers.append(new_composer)

@app.post("/pieces")
async def create_piece(new_piece: Pieces):
    pieces.append(new_piece)

@app.put("/composer/{composer_id}")
async def update_composer(composer_id: int, updated_composer: Composer):
    for i, composer in enumerate(composers):
        if composer.composer_id == composer_id:
            composers[i] = updated_composer
            return "Composer updated sucssefully"
    return "Composer created sucssefully"

@app.put("/pieces/{piece_name}")
async def update_piece(piece_name: str, updated_piece: Pieces):
    for i, piece in enumerate(pieces):
        if piece.name == piece_name:
            pieces[i] = updated_piece
            return "Composer updated sucssefully"
    return "Composer created sucssefully"

@app.delete("/composer/{composer_id}")
async def delete_composer(composer_id: int):
    for i, composer in enumerate(composers):
        if composer.composer_id == composer_id:
            composers.pop(i)
            return "Composer deleted"
        
@app.delete("/pieces/{piece_name}")
async def delete_piece(piece_name: str):
    for i, piece in enumerate(pieces):
        if piece.name == piece_name:
            pieces.pop(i)
            return "Piece deleted"


