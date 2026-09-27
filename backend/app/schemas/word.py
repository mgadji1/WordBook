from pydantic import BaseModel


class WordCreate(BaseModel):
    word: str
    translation: str


class WordUpdate(BaseModel):
    translation: str


class WordResponse(BaseModel):
    id: int
    word: str
    translation: str

    model_config = {
        "from_attributes": True
    }