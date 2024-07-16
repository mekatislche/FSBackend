from fastapi.testclient import TestClient

from api.public.review.views import router

client = TestClient(router)


def test_create_a_review():
    review_data = {
        "rating": "great",
        "review_text": "Тест",
        "user_id_from": "Хэш юзера",
        "user_id_to": "Хэш юзера",
    }
    response = client.post("/reviews/", json=review_data)
    assert response.status_code == 200
    created_review = response.json()
    assert created_review["rating"] == review_data["rating"]
    assert created_review["review_text"] == review_data["review_text"]


def test_get_user_got_reviews():
    user_id = "хэш"
    response = client.get(f"/reviews/user_got/{user_id}/")
    assert response.status_code == 200
    reviews = response.json()
    assert isinstance(reviews, list)


def test_get_user_gave_reviews():
    user_id = "хэш"
    response = client.get(f"/reviews/user_gave/{user_id}/")
    assert response.status_code == 200
    reviews = response.json()
    assert isinstance(reviews, list)


def test_update_a_review():
    review_id = 1
    update_data = {
        "rating": "some_problems",
        "review_text": "Could be better",
    }
    response = client.patch(f"/reviews/{review_id}/", json=update_data)
    assert response.status_code == 200
    updated_review = response.json()
    assert updated_review["rating"] == update_data["rating"]
    assert updated_review["review_text"] == update_data["review_text"]


def test_delete_a_review():
    review_id = 1
    response = client.delete(f"/reviews/{review_id}/")
    assert response.status_code == 200
    assert response.json() == {"ok": True}
