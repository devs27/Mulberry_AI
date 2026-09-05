from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.user import User
from app.models.listing import CocoonListing
from app.schemas.listing import ListingCreate, ListingOut
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/listings", tags=["listings"])


@router.post("/create", response_model=ListingOut)
def create_cocoon_listing(
    payload: ListingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Save the listing, deriving ownership user_id strictly from JWT auth context
    listing = CocoonListing(
        user_id=current_user.id,
        variety=payload.variety,
        price_per_kg=payload.price_per_kg,
        quantity_kg=payload.quantity_kg,
        location=payload.location,
        contact_phone=payload.contact_phone,
        status="active",
        description=payload.description
    )
    
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing


@router.get("/search", response_model=List[ListingOut])
def search_cocoon_listings(
    variety: Optional[str] = Query(None, description="Filter by cocoon variety (case-insensitive)"),
    location: Optional[str] = Query(None, description="Filter by location/village (case-insensitive)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Query active listings, newest first
    query = db.query(CocoonListing).filter(CocoonListing.status == "active")
    
    if variety and variety.strip():
        query = query.filter(CocoonListing.variety.ilike(f"%{variety.strip()}%"))
        
    if location and location.strip():
        query = query.filter(CocoonListing.location.ilike(f"%{location.strip()}%"))
        
    listings = query.order_by(CocoonListing.created_at.desc()).all()
    return listings


@router.get("/my", response_model=List[ListingOut])
def get_my_listings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Fetch all listings owned by the authenticated farmer
    listings = (
        db.query(CocoonListing)
        .filter(CocoonListing.user_id == current_user.id)
        .order_by(CocoonListing.created_at.desc())
        .all()
    )
    return listings


@router.post("/{listing_id}/sold", response_model=ListingOut)
def mark_listing_as_sold(
    listing_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Retrieve listing and enforce ownership validation check
    listing = db.query(CocoonListing).filter(CocoonListing.id == listing_id).first()
    
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
        
    if listing.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not own this listing")
        
    listing.status = "sold"
    db.commit()
    db.refresh(listing)
    return listing
