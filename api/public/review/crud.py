from uuid import UUID

from fastapi import HTTPException, status, Depends
from sqlmodel import Session, select

from api.auth import current_accepted_user
from api.public.review.models import ReviewCreate, Review, ReviewRead, ReviewUpdate
from api.public.user.models import User


def create_review(review: ReviewCreate, db: Session = None,
                  user: User = Depends(current_accepted_user)):
    review_to_db = Review(**review.dict())
    if review_to_db.user_id_from is None:
        review_to_db.user_id_from = user.id
    db.add(review_to_db)
    db.commit()
    db.refresh(review_to_db)
    return review_to_db


def read_user_got_reviews(user_id: UUID, offset: int = 0, limit: int = 20, db: Session = None):
    reviews = db.exec(select(Review).where(Review.user_id_to == user_id).offset(offset).limit(limit)).all()

    return [ReviewRead.from_orm(review) for review in reviews]


def read_user_gave_reviews(user_id: UUID, offset: int = 0, limit: int = 20, db: Session = None):
    reviews = db.exec(select(Review).where(Review.user_id_from == user_id).offset(offset).limit(limit)).all()

    return [ReviewRead.from_orm(review) for review in reviews]


def update_review(review_id: int, review: ReviewUpdate, db: Session = None):
    review_to_update = db.get(Review, review_id)
    if not review_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review not found with id: {review_id}"
        )

    review_data = review.dict(exclude_unset=True)
    for key, value in review_data.items():
        setattr(review_to_update, key, value)

    db.add(review_to_update)
    db.commit()
    db.refresh(review_to_update)
    return review_to_update


def delete_review(review_id: int, db: Session = None):
    review = db.get(Review, review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with id: {review_id}",
        )
    db.delete(review)
    db.commit()
    return {"ok": True}
