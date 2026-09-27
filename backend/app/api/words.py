from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.database.database import get_db
from sqlalchemy import select
from app.models.word import Word
from app.schemas.word import WordCreate, WordUpdate, WordResponse


router = APIRouter(prefix="/api/words", tags=["words"])


@router.get("", response_model=list[WordResponse])
async def get_all_words(
    db: AsyncSession = Depends(get_db)
):
    query = select(Word)

    result = await db.execute(query)

    return result.scalars().all()


@router.get("/{word}", response_model=WordResponse)
async def get_specific_word(
    word: str,
    db: AsyncSession = Depends(get_db)
):
    query = select(Word).where(Word.word == word)

    result = await db.execute(query)

    target_word = result.scalar_one_or_none()

    if target_word is None:
        raise HTTPException(
            status_code=404,
            detail="Word not found"
        )

    return target_word


@router.post("", response_model=WordResponse, status_code=201)
async def create_word(
    word_create: WordCreate,
    db: AsyncSession = Depends(get_db)
):
    new_word = Word(
        word=word_create.word,
        translation=word_create.translation
    )

    db.add(new_word)

    try:
        await db.commit()
        await db.refresh(new_word)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Word already exists"
        )

    return new_word


@router.put("/{word}", response_model=WordResponse)
async def update_translation(
    word: str,
    word_update: WordUpdate,
    db: AsyncSession = Depends(get_db)
):
    query = select(Word).where(Word.word == word)

    result = await db.execute(query)

    target_word = result.scalar_one_or_none()

    if target_word is None:
        raise HTTPException(
            status_code=404,
            detail="Word not found"
        )

    target_word.translation = word_update.translation

    await db.commit()
    await db.refresh(target_word)

    return target_word


@router.delete("/{word}")
async def delete_word(
    word: str,
    db: AsyncSession = Depends(get_db)
):
    query = select(Word).where(Word.word == word)
    
    result = await db.execute(query)

    target_word = result.scalar_one_or_none()

    if target_word is None:
        raise HTTPException(
            status_code=404,
            detail="Word not found"
        )

    await db.delete(target_word)
    await db.commit()

    return {
        "message": "Word deleted"
    }