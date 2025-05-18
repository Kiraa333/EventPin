from flask import Flask, render_template, request, redirect, url_for, flash, session
from orm import User, Event, db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import requests
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def geocode_address(address):
    base_url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": 'd09ddd62-8b37-4eab-83cb-427400d7fdba',
        "geocode": address,
        "format": "json"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    # Извлечение координат из ответа
    try:
        # Получаем первый результат
        feature_member = data['response']['GeoObjectCollection']['featureMember'][0]
        pos = feature_member['GeoObject']['Point']['pos']
        longitude, latitude = map(float, pos.split())
        return latitude, longitude
    except (KeyError, IndexError):
        return None, None


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('profile'))
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if 'user_id' in session:
        print('gg')
        return redirect(url_for('profile'))
    
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        flash('Неверный email или пароль', 'login_error')
        return redirect(url_for('auth'))
    
    session['user_id'] = user.id
    return redirect(url_for('profile'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if User.query.filter_by(email=email).first():
        flash('Пользователь с таким email уже существует', 'register_error')
        return redirect(url_for('auth'))
    
    if User.query.filter_by(username=username).first():
        flash('Пользователь с таким именем уже существует', 'register_error')
        return redirect(url_for('auth'))
    
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    session['user_id'] = new_user.id
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth'))
    
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth'))

@app.route('/events')
def events():
    if 'user_id' not in session:
        return redirect(url_for('auth'))
    all_events = Event.query.all()  # Возвращает список всех объектов Event
    return render_template('events.html', events=all_events)


@app.route('/my_events')
def my_events():
    user_data = User.query.get(session['user_id'])
    event = Event.query.filter_by(user_id=session['user_id']).all()
    print(event)
    print(session['user_id'])
    return render_template('my_events.html', user=user_data, my_events=event)


@app.route('/create_event')
def create_event():
    user_data = User.query.get(session['user_id'])
    return render_template('add_event.html', user=user_data)


@app.route('/create_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        # Получаем данные из формы
        title = request.form.get('title')
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        location = request.form.get('location')
        description = request.form.get('description')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        image = request.files.get('image')

        # Преобразуем дату и время в объект datetime
        date_time_str = f"{date_str} {time_str}"
        date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')

        # Сохраняем изображение (если оно есть)
        image_url = None
        if image:
            # Сохраняем изображение в папку static/uploads
            image_path = f"static/uploads/{image.filename}"
            image.save(image_path)
            image_url = image_path

        # Создаем новое событие
        new_event = Event(
            title=title,
            description=description,
            date=date_time,
            location=location,
            image_url=image.filename,
            user_id=session['user_id']  # Предположим, что пользователь с id=1 добавляет событие
        )

        # Добавляем событие в базу данных
        db.session.add(new_event)
        db.session.commit()
        
        print(f"Event added: {new_event}")

        flash('Событие успешно добавлено!', 'success')
        return redirect(url_for('my_events'))

# event_detail - полная страница карточки

@app.route('/event/<int:event_id>')
def event_card(event_id):
    event = Event.query.get_or_404(event_id)
    print(event.location)
    return render_template('card.html', event=event)

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)