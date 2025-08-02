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

def test_see_news(client, student_login_on_base_seed):
   student_login_on_base_seed() 
   response = client.get("/api/news/all")
   assert response.status_code == 200
   news_list = response.json()
   assert len(news_list) == 2
   assert all("title" in news for news in news_list)
   assert all("content" in news for news in news_list)


def test_update_news_unauthorized(client, basic_seed):
   basic_seed()
   response_login = client.post("/api/user/admin/auth", json={
         "email": "nonsuperior@gmail.com",
         "password": "password"
   })
   assert response_login.status_code == 200
   response_update = client.patch("/api/news/1", json={
         "title": "Updated News Title",
         "content": "Updated content for the news."
   })
   assert response_update.status_code == 403
