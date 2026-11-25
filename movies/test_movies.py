import pytest

from .models import Movie


@pytest.fixture
def movie(db):
    return Movie.objects.create(
        title="Test movie",
        description="Description",
        duration=120,
        release_date="2026-01-01",
        poster_url="https://example.com/poster.jpg",
    )


def test_movie_list(api_client, movie):
    response = api_client.get("/api/movies/")
    assert response.status_code == 200
    assert len(response.data) == 1


def test_movie_detail(api_client, movie):
    response = api_client.get(f"/api/movies/{movie.id}/")
    assert response.status_code == 200
    assert response.data["title"] == "Test movie"
