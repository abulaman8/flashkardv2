
from re import T
from celery import Celery
from flask import Blueprint, render_template, request,make_response, jsonify, current_app, request_finished, copy_current_request_context
from flask.helpers import send_file
from functools import wraps
from .models import User, Deck, Card
from . import db, mail
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os
import csv
import time
import jwt
import random
from . import mail
from flask_mail import Message
from . import celery
from . import cache











views = Blueprint("views", __name__)

BASE = 'http://127.0.0.1:5000'







def check_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
        if token:
            try:
                data = jwt.decode(token, current_app.config['SECRET_KEY'])
            except:
                return jsonify({'message': 'Invalid/Missing token'}), 401
        else:
            return jsonify({'message': 'Invalid/Missing token'}), 401
    return decorated




@celery.task
def export_deck(deck_name, username):
    with current_app.app_context():
        user = User.query.filter_by(username = username).first()
        msg = Message(recipients=['abulaman6@gmail.com',])
        cards = Card.query.filter_by(deck=deck_name)
        i=1
        with open(f'{deck_name}.csv', 'w', encoding="utf-8") as f:
            w=csv.writer(f)
            for card in cards:
                w.writerow([i,card.front,card.back])
                i+=1
        with current_app.open_resource(f'../{deck_name}.csv') as f:
            msg.attach(f'{deck_name}.csv', 'text/csv', f.read())
        mail.send(msg)
        
    return deck_name


@celery.task
def monthly_report(username):
    with current_app.app_context():
        user = User.query.filter_by(username= username).first()
        decks = Deck.query.filter_by(user = username)
        deck_list = [deck for deck in decks]
        





def isallowed(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".",1)[1]
    if ext.lower() == 'csv':
        return True
    else:
        return False

@cache.memoize(timeout=15)
def getDashboardData(username):
    decks = Deck.query.filter_by(user = username)
    r = []
    for deck in decks:
        r.append({'deck_name':deck.deck_name, 'score':int(deck.score), 'last_rev':str(deck.last_rev)[:9]})
    return r


@views.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data['username']
        password = data['password']
        # username = request.form.get("username")
        # password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, current_app.config['SECRET_KEY'])
                return jsonify({'token': token.decode('UTF-8')}), 200
                pass

                # return redirect('/dashboard')
            else:
                return make_response('Incorrect Password.', 401)
                
                # flash('Password is incorrect.', category='error')
        else:
            return make_response('Username does not exist.', 401)
            # flash('Username does not exist.', category='error')







@views.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        username = data['username']
        email = data['email']
        password = data['password']
        # username = request.form.get('username')
        # email = request.form.get('email')
        # password = request.form.get('password')
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return make_response({'message': 'Account with same email or username already exists'}, 401)
        new_user = User(username=username, email=email, password= generate_password_hash(password, method='sha256'))
        try:
            db.session.add(new_user)
            db.session.commit()
            return make_response({'message': 'Account created Succesfully'}, 200)
        except:
            return make_response({'message': 'Account Not Created'}, 401)












@check_token
@views.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    token = request.headers.get('token')
    data = jwt.decode(token, current_app.config['SECRET_KEY'])
    username = data['user']
    # decks = Deck.query.filter_by(user = username)
    # r = []
    # for deck in decks:
    #     r.append({'deck_name':deck.deck_name, 'score':int(deck.score), 'last_rev':str(deck.last_rev)[:9]})

    return jsonify(getDashboardData(username=username)), 200










@check_token
@views.route('/create-deck', methods = ['POST', 'GET'])
def create_deck():
    token = request.headers.get('token')
    data = jwt.decode(token, current_app.config['SECRET_KEY'])
    username = data['user']
    cardsjson = request.json
    deck_name = cardsjson['deck_name']
    cards = cardsjson['cards']
    # jsonify(cards)
    print(cards)
    print(cards[0])
    print(type(cards[0]))

    if Deck.query.filter_by(user = username, deck_name=deck_name).first():
        return make_response({'message': 'Deck Already Exists'}, 403)
    new_deck = Deck(deck_name=deck_name, user=username)
    try:
        db.session.add(new_deck)
        db.session.commit()
    except:
        return make_response({'message': 'Deck Not Created.'}, 403)
    for card in cards:
        new_card = Card(front = card['front'], back = card['back'], deck = deck_name)
        try:
            db.session.add(new_card)
            db.session.commit()
        except:
            return make_response({'message': 'Deck Not Created.'}, 403)
    return make_response({'message': 'Deck created successfully'}, 200)









@check_token
@views.route('/review/<string:deck_name>', methods=['GET', 'POST'])
def review_deck(deck_name):
    if request.method == 'GET':
        token = request.headers.get('token')
        data = jwt.decode(token, current_app.config['SECRET_KEY'])
        username = data['user']
        deck_name = deck_name
        deck = Deck.query.filter_by(user = username, deck_name= deck_name).first()
        r=[]
        
        if deck:
            cards = Card.query.filter_by(deck=deck_name)
            r = [{'front': card.front, 'back': card.back, 'id': card.card_id} for card in cards]
            random.shuffle(r)
            return jsonify(r), 200
    elif request.method == 'POST':
        token = request.headers.get('token')
        data = jwt.decode(token, current_app.config['SECRET_KEY'])
        username = data['user']
        deck_name = deck_name
        deck = Deck.query.filter_by(user = username, deck_name = deck_name).first()
        cardsjson = request.json
        cards = cardsjson['cards']

        for card in cards:
            edit_card = Card.query.filter_by(card_id = int(card['id']), deck=deck_name).first()
            edit_card.score = card['score']
            try:
                db.session.commit()
            except:
                return make_response({'message': 'Review failed'}, 403)
        deckscore = sum([card['score'] for card in cards])/len(cards)
        deck.score = deckscore
        try:
            db.session.commit()
            return make_response({'message': 'Review Succesfull'}, 200)
        except:
            return make_response({'message': 'Review failed'}, 403)














# @views.route('/email', methods=['GET', 'POST'])
# def email():
#     msg = Message(
#         'hey, bro',
#         recipients=['abulaman6@gmail.com'],

#     )
#     mail.send(msg)
#     return make_response({'message': 'email sent'}, 200)













@check_token
@views.route('/<string:deck_name>/delete', methods=['POST', 'GET'])
def delete_deck(deck_name):
    token = request.headers.get('token')
    data = jwt.decode(token, current_app.config['SECRET_KEY'])
    username = data['user']
    del_deck = Deck.query.filter_by(user=username, deck_name=deck_name).first()
    if del_deck:
        try:
            db.session.delete(del_deck)
            db.session.commit()
            return make_response({'message': 'deck deleted successfully'}, 200)
        except:
            return make_response({'message': 'Couldn\'t delete deck...'}, 403)
    return make_response({'message': 'Deck Doesn\'t exist'}, 403)













@check_token
@views.route('/<string:deck_name>/edit', methods=['POST', 'GET'])
def edit_deck(deck_name):
    if request.method == 'POST':
        token = request.headers.get('token')
        data = jwt.decode(token, current_app.config['SECRET_KEY'])
        username = data['user']
        edit_deck = Deck.query.filter_by(user=username, deck_name=deck_name).first()
        deckjson = request.json
        cards = deckjson['cards']


        if edit_deck:
            
            for card in cards:
                if card['delete'] == 'yes':
                    del_card = Card.query.flter_by(card_id = int(card['id'])).first()
                    db.session.delete(del_card)
                    try:
                        db.session.commit()
                    except:
                        return make_response({'message': 'Deck edit failed'}, 403)
                elif card['id'] != 'null' and card['delete'] == 'no':
                    edit_card = Card.query.filter_by(card_id = int(card['id']), deck=deck_name).first()
                    if edit_card:
                        edit_card.front = card['front']
                        edit_card.back = card['back']
                        try:
                            db.session.commit()
                        except:
                            return make_response({'message': 'Deck edit failed'},403)
                    return make_response({'message': 'Deck edit failed'}, 403)
                elif card['id'] == 'null' and card['delete'] == 'no':
                    new_card = Card(front = card['front'], back = card['back'], deck = deck_name)
                    try:
                        db.session.add(new_card)
                        db.session.commit()
                    except:
                        return make_response({'message': 'Deck edit failed'},403)  
            if deckjson['deck_name'] != deck_name:
                edit_deck.deck_name = deckjson['deck_name']
                try:
                    db.session.commit()
                except:
                    return make_response({'message': 'Deck edit failed'}, 403)
            return make_response({'message': 'Deck editted Successfully'}, 200)

        
        return make_response({'message': 'Deck Doesn\'t exist'}, 403)
    
    elif request.method == 'GET':
        token = request.headers.get('token')
        data = jwt.decode(token, current_app.config['SECRET_KEY'])
        username = data['user']
        deck_name = deck_name
        deck = Deck.query.filter_by(user = username, deck_name= deck_name).first()
        r=[]
        
        if deck:
            cards = Card.query.filter_by(deck=deck_name)
            r = [{'front': card.front, 'back': card.back, 'id': card.card_id} for card in cards]
            random.shuffle(r)
            return jsonify(r), 200













@check_token
@views.route('/import', methods = ['POST', 'GET'])
def import_deck(d):
    if request.method == 'POST':
        token = request.headers.get('token')
        data = jwt.decode(token, current_app.config['SECRET_KEY'])
        username = data['user']
        if request.files:
            csvfile = request.files['csvfile']
            # print(csvfile)
            if isallowed(csvfile.filename):
                csvfile.save(os.path.join('C:\\Users\\5.413U14M4N\\appdev2\\api\\flashkardv2\\static\\',csvfile.filename))
                d=Deck(deck_name=csvfile.filename.split('.')[0], user=username)
                try:
                    db.session.add(d)
                    db.session.commit()
                except:
                    return make_response({'message': 'Deck import failed'}, 403)
                with open(f'C:\\Users\\5.413U14M4N\\appdev2\\api\\flashkardv2\\static\\{csvfile.filename}', 'r') as f:
                    c=csv.reader(f)
                    next(c)
                    for i in c:
                        print(i)
                        c=Card(front=i[1], back=i[2], deck=csvfile.filename.split('.')[0])
                        try:
                            db.session.add(c)
                            db.session.commit()
                        except:
                            return make_response({'message': 'Deck Import failed'}, 403)
                return make_response({'message': 'Deck imported successfully'}, 200)
            return make_response({'message': 'Only Csv files allowed...'}, 403)














# @check_token
@views.route('export/<string:deck_name>', methods = ['POST', 'GET'])
def export(deck_name):
    token = request.headers.get('token')
    data = jwt.decode(token, current_app.config['SECRET_KEY'])
    username = data['user']
    # cards = Card.query.filter_by(deck=deck_name)
    # i=1
    # with open(f'{deck_name}.csv', 'w', encoding="utf-8") as f:
    #     w=csv.writer(f)
    #     for card in cards:
    #         w.writerow([i,card.front,card.back])
    #         i+=1
    #         time.sleep(2)
    # return send_file(f'../{deck_name}.csv', as_attachment=True)
    export_deck.delay(deck_name, username)
    return make_response(jsonify({'message': 'Export started'}), 200)
    






