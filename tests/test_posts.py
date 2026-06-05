from datetime import datetime


TEST_POSTS = [
    {
        'title': 'Тестовый заголовок поста',
        'text': 'Это подробный текст тестового поста для проверки страницы.',
        'author': 'Иванов Иван Иванович',
        'date': datetime(2025, 3, 10),
        'image_id': '7d4e9175-95ea-4c5f-8be5-92a6b708bb3c.jpg',
        'comments': [
            {
                'author': 'Петров Пётр',
                'text': 'Основной комментарий к посту.',
                'replies': [
                    {
                        'author': 'Сидорова Анна',
                        'text': 'Ответ на комментарий.'
                    }
                ]
            }
        ]
    }
]


def patch_posts(mocker):
    return mocker.patch('app.posts_list', return_value=TEST_POSTS, autospec=True)


# 1

def test_posts_page_status_code(client):
    response = client.get('/posts')
    assert response.status_code == 200


# 2

def test_posts_page_uses_posts_template(client, captured_templates, mocker):
    with captured_templates as templates:
        patch_posts(mocker)
        client.get('/posts')

        template, context = templates[0]
        assert template.name == 'posts.html'


# 3

def test_posts_page_context_contains_title(client, captured_templates, mocker):
    with captured_templates as templates:
        patch_posts(mocker)
        client.get('/posts')

        template, context = templates[0]
        assert context['title'] == 'Посты'


# 4

def test_posts_page_context_contains_posts(client, captured_templates, mocker):
    with captured_templates as templates:
        patch_posts(mocker)
        client.get('/posts')

        template, context = templates[0]
        assert context['posts'] == TEST_POSTS


# 5

def test_post_page_status_code(client, mocker):
    patch_posts(mocker)
    response = client.get('/posts/0')
    assert response.status_code == 200


# 6

def test_post_page_uses_post_template(client, captured_templates, mocker):
    with captured_templates as templates:
        patch_posts(mocker)
        client.get('/posts/0')

        template, context = templates[0]
        assert template.name == 'post.html'


# 7

def test_post_page_context_contains_title(client, captured_templates, mocker):
    with captured_templates as templates:
        patch_posts(mocker)
        client.get('/posts/0')

        template, context = templates[0]
        assert context['title'] == TEST_POSTS[0]['title']


# 8

def test_post_page_context_contains_post(client, captured_templates, mocker):
    with captured_templates as templates:
        patch_posts(mocker)
        client.get('/posts/0')

        template, context = templates[0]
        assert context['post'] == TEST_POSTS[0]


# 9

def test_post_page_contains_post_title(client, mocker):
    patch_posts(mocker)
    response = client.get('/posts/0')
    assert TEST_POSTS[0]['title'] in response.text


# 10

def test_post_page_contains_post_text(client, mocker):
    patch_posts(mocker)
    response = client.get('/posts/0')
    assert TEST_POSTS[0]['text'] in response.text


# 11

def test_post_page_contains_author_name(client, mocker):
    patch_posts(mocker)
    response = client.get('/posts/0')
    assert TEST_POSTS[0]['author'] in response.text


# 12

def test_post_page_contains_form_title_and_button(client, mocker):
    patch_posts(mocker)
    response = client.get('/posts/0')
    assert 'Оставьте комментарий' in response.text
    assert 'Отправить' in response.text
    assert '<textarea' in response.text


# 13

def test_post_page_contains_comment(client, mocker):
    patch_posts(mocker)
    response = client.get('/posts/0')
    comment = TEST_POSTS[0]['comments'][0]
    assert comment['author'] in response.text
    assert comment['text'] in response.text


# 14

def test_post_page_contains_reply_to_comment(client, mocker):
    patch_posts(mocker)
    response = client.get('/posts/0')
    reply = TEST_POSTS[0]['comments'][0]['replies'][0]
    assert reply['author'] in response.text
    assert reply['text'] in response.text


# 15

def test_post_page_contains_image(client, mocker):
    patch_posts(mocker)
    response = client.get('/posts/0')
    assert TEST_POSTS[0]['image_id'] in response.text


# 16

def test_post_page_date_has_correct_format(client, mocker):
    patch_posts(mocker)
    response = client.get('/posts/0')
    assert '10.03.2025' in response.text


# 17

def test_nonexistent_post_returns_404(client, mocker):
    patch_posts(mocker)
    response = client.get('/posts/999')
    assert response.status_code == 404


# 18

def test_base_template_contains_footer(client, mocker):
    patch_posts(mocker)
    response = client.get('/posts/0')
    assert '<footer' in response.text
    assert 'Выполнил: Щербаков Тимофей Дмитриевич' in response.text
    assert 'группа 241-371' in response.text
