from flask import Flask, render_template

app = Flask(__name__)

# Пример данных о событиях
events = [
    {
        "title": "Концерт классической музыки",
        "date": "15 июня 2023, 19:00",
        "location": "Московская консерватория",
        "description": "Вечер классической музыки с участием ведущих музыкантов страны.",
        "image_url": "/static/play.jpg"
    },
    {
        "title": "Выставка современного искусства",
        "date": "20 июня 2023, 10:00",
        "location": "Галерея современного искусства",
        "description": "Работы современных художников со всего мира.",
        "image_url": "/static/art.jpg"
    },
    {
        "title": "Театральная премьера",
        "date": "25 июня 2023, 18:30",
        "location": "Большой театр",
        "description": "Премьера нового спектакля от известного режиссера.",
        "image_url": "/static/theater.jpg"
    },
    {
        "title": "Театральная премьера",
        "date": "25 июня 2023, 18:30",
        "location": "Большой театр",
        "description": "Премьера нового спектакля от известного режиссера.",
        "image_url": "/static/theater.jpg"
    }
]

# Данные пользователя
user_data = {
    "username": "Иван Иванов",
    "email": "ivan@example.com",
    "phone": "+7 (900) 123-45-67",
    "birthdate": "1990-01-01",
    "events_count": 12,
    "friends_count": 5,
    "avatar": "/static/avatar.jpg"
}


@app.route('/')
def home():
    return render_template('try.html')


@app.route('/events')
def show_events():
    return render_template('events.html', events=events)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/card')
def card():
    return render_template('card.html')


@app.route('/profile')
def profile():
    return render_template('profile.html', user=user_data)

@app.route('/my_events')
def my_events():
    return render_template('my_events.html', user=user_data)


if __name__ == '__main__':
    app.run(debug=True)
