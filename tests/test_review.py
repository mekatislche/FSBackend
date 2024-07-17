def test_create_a_review(client):
    review_data = {
        "rating": "great",
        "review_text": "test",
        "user_id_from": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "user_id_to": "52a805dc-b86e-45ee-bbfa-0de972bb801f"
    }
    response = client.post("/reviews", json=review_data)
    assert response.status_code == 200
    created_review = response.json()
    assert created_review["rating"] == review_data["rating"]
    assert created_review["review_text"] == review_data["review_text"]


def test_get_user_got_reviews(client):
    user_id = "52a805dc-b86e-45ee-bbfa-0de972bb801f"
    response = client.get(f"/reviews/user_got/{user_id}?offset=0&limit=100")
    assert response.status_code == 200
    reviews = response.json()
    assert isinstance(reviews, list)


def test_get_user_gave_reviews(client):
    user_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    response = client.get(f"/reviews/user_gave/{user_id}?offset=0&limit=100")
    assert response.status_code == 200
    reviews = response.json()
    assert isinstance(reviews, list)


def test_update_a_review(client):
    review_id = 1
    update_data = {
        "rating": "some_problems",
        "review_text": "Could be better",
        "user_id_from": "string",
        "user_id_to": "string"
    }
    response = client.patch(f"/reviews/{review_id}", json=update_data)
    assert response.status_code == 200
    updated_review = response.json()
    assert updated_review["rating"] == update_data["rating"]
    assert updated_review["review_text"] == update_data["review_text"]


def test_delete_a_review(client):
    review_id = 4
    response = client.delete(f"/reviews/{review_id}/")
    assert response.status_code == 200
    assert response.json() == {"ok": True}
