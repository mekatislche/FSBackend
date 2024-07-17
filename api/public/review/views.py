from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from api.auth import current_accepted_user
from api.database import get_session
from api.public.review.crud import read_user_got_reviews, read_user_gave_reviews, create_review, update_review, \
    delete_review
from api.public.review.models import ReviewRead, ReviewCreate, ReviewUpdate
from api.public.user.models import User

router = APIRouter()


@router.post("", response_model=ReviewRead, dependencies=[Depends(current_accepted_user)])
def create_a_review(review: ReviewCreate, db: Session = Depends(get_session),
                    user: User = Depends(current_accepted_user)):
    return create_review(review=review, db=db, user=user)


@router.get("/user_got/{user_id}", response_model=list[ReviewRead], dependencies=[Depends(current_accepted_user)])
def get_user_got_reviews(
        user_id: UUID,
        offset: int = 0,
        limit: int = Query(default=100, lte=100),
        db: Session = Depends(get_session)
):
    return read_user_got_reviews(user_id=user_id, offset=offset, limit=limit, db=db)


@router.get("/user_gave/{user_id}", response_model=list[ReviewRead], dependencies=[Depends(current_accepted_user)])
def get_user_gave_reviews(
        user_id: UUID,
        offset: int = 0,
        limit: int = Query(default=100, lte=100),
        db: Session = Depends(get_session)
):
    return read_user_gave_reviews(user_id=user_id, offset=offset, limit=limit, db=db)


@router.patch("/{review_id}", response_model=ReviewUpdate, dependencies=[Depends(current_accepted_user)])
def update_a_review(review_id: int, review: ReviewUpdate, db: Session = Depends(get_session)):
    return update_review(review_id=review_id, review=review, db=db)


@router.delete("/{review_id}", dependencies=[Depends(current_accepted_user)])
def update_a_review(review_id: int, db: Session = Depends(get_session)):
    return delete_review(review_id=review_id, db=db)
