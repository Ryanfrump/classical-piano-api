import json
from fastapi import FastAPI, Query, HTTPException, status
from typing import List, Optional

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
async def list_pieces(composer_id: Optional[int] = Query(None)) -> list[Pieces]:
    if composer_id is not None:
        filtered_pieces = [piece for piece in pieces if piece.composer_id == composer_id]
    else:
        filtered_pieces = pieces
    return filtered_pieces

@app.post("/composers")
async def create_composer(new_composer: Composer):
    for composer in composers:
        if composer.composer_id == new_composer.composer_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Composer with this ID already exists")
    composers.append(new_composer)

@app.post("/pieces")
async def create_piece(new_piece: Pieces):
    composer_exists = any(composer.composer_id == new_piece.composer_id for composer in composers)
    if not composer_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No composer with this ID")
    pieces.append(new_piece)

@app.put("/composer/{composer_id}")
async def update_composer(composer_id: int, updated_composer: Composer):
    for i, composer in enumerate(composers):
        if composer.composer_id == composer_id:
            for c in composers:
                if c.composer_id == updated_composer.composer_id and c != composer:
                    raise HTTPException(status_code=400, detail="Duplicate composer ID")
            composers[i] = updated_composer
            return "Composer updated successfully"
    composers.append(updated_composer)
    return "Composer created successfully"

@app.put("/pieces/{piece_name}")
async def update_piece(piece_name: str, updated_piece: Pieces):
    if not any(composer.composer_id == updated_piece.composer_id for composer in composers):
        raise HTTPException(status_code=400, detail="Composer ID doesn't exist")

    for i, piece in enumerate(pieces):
        if piece.name == piece_name:
            pieces[i] = updated_piece
            return "Piece updated sucssefully"
    pieces.append(updated_piece)
    return "Piece created sucssefully"

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


