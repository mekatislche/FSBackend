from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import UUID4
from sqlmodel import SQLModel, Field, Relationship


class ReviewRating(str, Enum):
    GREAT = "great"
    SOME_PROBLEMS = "some_problems"
    BAD = "bad"

    def __str__(self) -> str:
        return self.value


class ReviewBase(SQLModel):
    rating: Optional[ReviewRating] = Field(default=None)
    review_text: Optional[str] = Field(default=None)
    user_id_from: UUID4 = Field(foreign_key='user.id')
    user_id_to: UUID4 = Field(foreign_key='user.id')


class Review(ReviewBase, table=True):
    review_id: Optional[int] = Field(primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )


class ReviewCreate(ReviewBase):
    rating: Optional[ReviewRating]
    review_text: Optional[str]
    user_id_from: UUID4
    user_id_to: UUID4


class ReviewRead(ReviewBase):
    review_id: UUID4
    rating: Optional[ReviewRating]
    review_text: Optional[str]


class ReviewUpdate(ReviewBase):
    review_id: UUID4
    rating: Optional[ReviewRating]
    review_text: Optional[str]
