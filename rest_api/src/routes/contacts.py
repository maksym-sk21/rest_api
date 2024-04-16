from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from ..repository.contacts import create_contact, get_contact, get_contacts, update_contact, delete_contact
from ..schemas import Contact, ContactCreate, ContactUpdate
from ..database.db import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/contacts/", response_model=Contact)
async def create_new_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return create_contact(db, contact)


@router.get("/contacts/", response_model=List[Contact])
async def get_all_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_contacts(db, skip=skip, limit=limit)


@router.get("/contacts/{contact_id}", response_model=Contact)
async def get_single_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = get_contact(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/contacts/{contact_id}", response_model=Contact)
async def update_single_contact(
    contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)
):
    updated_contact = update_contact(db, contact_id, contact)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact


@router.delete("/contacts/{contacts_id}")
async def delete_single_contact(
    contact_id: int, db: Session = Depends(get_db)
):
    success = delete_contact(db, contact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}