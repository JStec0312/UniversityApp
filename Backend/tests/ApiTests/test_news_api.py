def test_create_news(superior_admin_login_on_base_seed, client, db_session):
    superior_admin_login_on_base_seed()
    response = client.post("/api/news/", json={
       "title": "New News Title",
       "content": "This is the content of the new news.",
       "image_url": "http://example.com/image.jpg"
    })
    assert response.status_code == 201
    from app.models.news import News
    query = db_session.query(News).filter(News.title == "New News Title").first()
    assert query is not None
    assert query.content == "This is the content of the new news."
    assert query.image_url == "http://example.com/image.jpg"
    assert query.group_id == 1
    assert query.university_id == 1  
    assert query.title == response.json().get("title")