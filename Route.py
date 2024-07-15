from ast import literal_eval
import ast
import os
import hmac
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from flask import  json, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user
from flask_migrate import Migrate
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from Forms import RegistrationForm,LoginForm,ResetPasswordForm,RequestResetForm
#from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from read_User_credentials import read_credentials

from DbModel import *

global usernameU, password, MailUsername, MailPassword
usernameU, password, MailUsername, MailPassword ,SECRET_KEY,default_secret_key= read_credentials()


app.secret_key = SECRET_KEY

# Configurazione del database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NewDb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

login_manager = LoginManager(app)
login_manager.login_view = 'login'


SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD =  MailPassword
SENDER_EMAIL = MailUsername 
migrate = Migrate(app, db)

db.create_all()

# Funzione per caricare un utente
@login_manager.user_loader
def load_user(user_id):
    
    
    
    return User.query.get(int(user_id))  # Assuming user ID is stored as an integer


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    print("51 ")
    if form.validate_on_submit():
        print("50 ")
        username = form.username.data
        email = form.email.data
        password = form.password.data
        print("56 username",username)
        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered.')
            return redirect(url_for('register'))

        # Hash password and create new user
        ###hashed_password = generate_password_hash(password, method='sha256')
        #new_user = User(username=username, email=email, password_hash= password)
        #new_user = User(email=email, password=generate_password_hash(password), username=username)
                # Create new user with hashed password
        new_user = User(email=email, password=password, username=username)
        db.session.add(new_user)
        db.session.commit()

        flash('dopo in .py file Registration successful!')
        return redirect(url_for('login'))
    print("75 ")
    print(form.errors)

    return render_template('DBregister copy.html', form=form)

"""

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("Form validated successfully!")
        # Continua con il processo di registrazione
    else:
        print("Form validation failed. Errors:", form.errors)
    return render_template('DBregister copy.html', form=form)

"""


@app.route('/logout')
def logout():
    print("session[email]  " , session["email"])
    session.pop('email', None)
    print("79")
    
    logout_user()  # Call Flask-Login's logout function
    print("current_user.is_authenticated:",current_user.is_authenticated)
    print("81")
    flash('Logout successful!', 'success')  # Set flash message
    return redirect(url_for('login'))

@app.route('/loginPg', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print("87")
        #return "hi"
        redirect(url_for('dashboard'))

    form = LoginForm()
    
    if request.method == 'POST':
        if request.is_json:
            # Gestione della richiesta JSON dall'app mobile
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            print("105")
        if form.validate_on_submit():
            print("106")
            # Gestione del form HTML
            email = form.email.data
            password = form.password.data
            print("110  email",email)
            print("111  password ",password)

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!')
            session[ "email"] = email
            if request.is_json:
                return jsonify({'status': 'success', 'message': 'Login successful!'})
            else:
                return redirect(url_for('dashboard'))
        else:
            error_message = 'Invalid email or password.'
            if request.is_json:
                return jsonify({'status': 'error', 'message': error_message})
            else:
                flash(error_message)

    return render_template('DBlogin copy.html', form=form)        


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    print("196")
    if 'email' not in session:
        print("183")
        return redirect(url_for('login'))
    if request.method == 'POST':
        print("186")
        num_buttons = request.form['num_buttons']
        button_labels = [request.form.get(f'button{i+1}') for i in range(int(num_buttons))]
        # Handle saving button settings logic
        print("email",session['email'])
        print("num_buttons",num_buttons)
        print("button_labels",button_labels)
        return render_template('DBdashboard.html', email=session['email'])
    print("243   session['email']",session['email'])
    return render_template('DBdashboard.html', email=session['email'])
@app.route('/')
def index():
    # Your route logic here (if any)
    #return render_template('index.html')
    #return "lion"
    return redirect(url_for('login'))

@app.route('/state', methods=['POST'])
@login_required
def update_state():
    print("182")
    # Recupera l'utente corrente
    user = current_user

    # Recupera le impostazioni del pulsante per l'utente corrente
    button_settings = ButtonSettings.query.filter_by(user_id=user.id).first()
    #print("button_settings.button_states 374 ",button_settings.button_states)
    #print("type(button_settings.button_states) 375 ", type(button_settings.button_states))
    if not button_settings:
        return jsonify({'error': 'Button settings not found for the current user.'}), 404
    # Ottieni i dati JSON dalla richiesta
    data = request.get_json()
    button_id = int(data.get('buttonId'))
    print("button_id",button_id)
    new_state = data.get('state')
    button_label = data.get('buttonLabel')
    print("button_label",button_label)
    
    print("---Line 108 ---------data from esp32 /state-------button_id---------")
    print(button_id)
    print("-@@@@@@@@@@--data from esp32 /state-------button_label---------")
    print(button_label)
    print("button_settings.button_states[button_id] 389 ",button_settings.button_states[button_id])    
    print("-----------fine /state ---data from esp32 ----------------")
    # Aggiorna lo stato del pulsante nel database
    #button_settings.button_states[button_id] = "new_state"
    print("393")
    print(type(new_state))
    print("Updated button_states:393 ", button_settings.button_states)
    print("Updated button_labels:", button_settings.button_labels)

        # Ensure button_states is a list or dictionary
    button_states = literal_eval(button_settings.button_states)
    button_states[button_id] = new_state
    button_settings.button_states = str(button_states)

    db.session.commit()    
    

    #print(" 408     DOPO UPDATE ")
    button_settings = ButtonSettings.query.filter_by(user_id=user.id).first()
    #print("Updated button_states:420", button_settings.button_states)
    #print("Updated button_labels:", button_settings.button_labels)

    # Passa i dati necessari al template Jinja
    num_buttons = len(button_settings.button_labels)  # Numero dei pulsanti
    button_labels = button_settings.button_labels  # Etichette dei pulsanti
    button_states = button_settings.button_states  # Stati dei pulsanti
    
    '''
    print("button_id 386 : ",button_id)
    print("new_state ",new_state)
    print("button_states ",button_states)
    print("button_label  : ",button_label)
    # Supponendo che button_data sia già preparato correttamente altrove nel codice
    #button_data = [...]  # Dati dei pulsanti

    # Esempio di come potresti passare i dati al template
    #return render_template('toggle.html', num_buttons=num_buttons, button_labels=button_labels, button_states=button_states, button_data=button_data)
    '''
    return jsonify({'message': f'State updated for button {button_label}'})


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        print("155",form.email.data)
        #user = User.query.filter_by(email=email).first()
        user = User.query.filter_by(email=form.email.data).first()
        print("155")
        if user:
            token = user.get_reset_token()
            body = f"To reset your password, visit the following link: {url_for('reset_token', token=token, _external=True)}"
            #send_registration_email(form.email.data, body)
            flash('An email has been sent with instructions to reset your password.', 'info')
            print("155")
            print(body)
            return redirect(url_for('login'))
    
    return render_template('reset_request.html', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', form=form)
def string_to_list(s):
    # Convert the string representation of a list to an actual list
    return ast.literal_eval(s)
def custom_list_to_json(lst):
    # Join elements without quotes, assuming they are valid JSON tokens (like variable names)
    json_string = "[" + ", ".join(lst) + "]"
    return json_string

@app.route('/toggle', methods=['GET', 'POST'])
@login_required
def toggle():
    if 'email' not in session:
        flash('You are not logged in. Please log in to access this page.', 'danger')
        return redirect(url_for('login'))    
    user = User.query.filter_by(email=session['email']).first()
    button_settings = ButtonSettings.query.filter_by(user_id=user.id).first()
    print("245 session['email'] ",session['email'])
    print("246",user.id)
    print("247 button_settings ",button_settings)
    
    
    if request.method == 'POST':
        if request.is_json:
            # Gestione della richiesta JSON dall'app mobile
            data = request.get_json()
            num_buttons = data.get('num_buttons')
            button_labels = data.get('button_labels')
            print("303")
            print("num_buttonsj",num_buttons)
            print("306 button_labels1 ",button_labels)
            print(" type(button_labels1) ", type(button_labels))
        else:
            print("post 309")
            num_buttons = int(request.form['num_buttons'])
            button_labels = [request.form[f'button{i+1}'] for i in range(num_buttons)]
            
            
            print("313  type(button_labels) ", type(button_labels))



        button_states = ['off'] * num_buttons
        
        if button_settings:
            button_settings.num_buttons = num_buttons
            button_settings.button_labels = json.dumps(button_labels)
            #print("264 type(button_labels)",type(button_labels))
            button_settings.button_states = json.dumps(button_states)
            print("321 type(button_labels)",type(json.dumps(button_labels)))
        else:
            new_button_settings = ButtonSettings(
                num_buttons=num_buttons,
                button_labels=json.dumps(button_labels),
                button_states=json.dumps(button_states),
                user_id=user.id
            )
            db.session.add(new_button_settings)
        db.session.commit()

    if button_settings:
        
        
        num_buttons = button_settings.num_buttons
        print("269",num_buttons)
        button_labels =button_settings.button_labels
        button_states = button_settings.button_states
        #button_labels = json.loads(button_settings.button_labels)
        #button_states = json.loads(button_settings.button_states).split(", ")
        print("278 button_labels",button_labels)
        print("279 button_labels",button_labels.strip("[]").strip('"'))
        print("280 type(button_labels)",type(button_labels))
        

        # Example usage
        input_string = "['led1', 'GT']"

        # Step 1: Convert string to list
        my_list = string_to_list(button_labels)
        button_states = string_to_list(button_settings.button_states)
        '''
        print("296 type(button_labels)",type(my_list))
        # Step 2: Convert list to custom JSON-like string
        custom_json = custom_list_to_json(my_list)
        #button_labels = custom_list_to_json(my_list)
        
        json_string = json.dumps(my_list)
        print("303 type(button_labels)",type(json_string))
        print(custom_json)  # Output: [led1, GT]
        '''
        button_labels= my_list

        
        
    else:
        num_buttons = 0
        button_labels = []
        button_states = []
        print("279",num_buttons)
    if request.is_json:
        #return jsonify({'message': 'Data received successfully'}), 200
        print("*************  377 **************************")
        return jsonify({'num_buttons':num_buttons, 'button_labels':button_labels, 'button_states':button_states}), 200
    else:
        
        user_agent = request.headers.get('User-Agent')
        if 'Kivy' in user_agent:
            print("*************  379  **************************")
            return jsonify({'num_buttons':num_buttons, 'button_labels':button_labels, 'button_states':button_states})
        else:
            print(" web 386 ")
            return render_template('toggle.html', num_buttons=num_buttons, button_labels=button_labels, button_states=button_states)



@app.route('/Pstate', methods=['GET', 'POST'])
@login_required
def Pupdate_state():
    global aved_button_id, aved_button_label, Sbutton_data, button_data
    global  saved_button_Pin

    user = current_user
    settings = user.settings
    print("559  settings   ", settings)
    
    if settings:
        saved_button_Pin = [2] * settings.num_buttons
        print("562  type(saved_button_Pin :    ", type(saved_button_Pin))
        print("563  saved_button_Pin   ", saved_button_Pin)
        #print("548 settings.num_buttons  ", settings.num_buttons)
        saved_button_labels = settings.button_labels
        saved_button_states = settings.button_states
        num_buttons = settings.num_buttons
        
        print("340  saved_button_labels :    ", saved_button_labels)
        print("341  saved_button_states   ", saved_button_states)
        print("342  num_buttons   ", num_buttons)
        
    else:
        saved_button_Pin = []
        saved_button_labels = []
        saved_button_states = []
        num_buttons = 0  # Add this line to handle the case where settings is None

    Sbutton_data = []
    if request.method == 'POST':
        data = request.get_json()
        button_id = int(data.get('buttonId'))
        buttonPin = data.get('buttonPin')
        print("-line 134 ----------data from esp32 /state-------buttonPin---------")
        #print(buttonPin)
        button_label = data.get('buttonLabel')
        
        '''
        print("Line 166 saved_button_PIN prima")
        print(saved_button_Pin)
        print(f"Line 168 len(saved_button_PIN) prima", len(saved_button_Pin))
        print(len(saved_button_Pin))
        print(f"num_buttons:", num_buttons)
        '''
        
        for rin in range(num_buttons):
            '''
            print("Line 172 buttonPin dentro if ")
            print(f"buttonPin::", buttonPin)
            print(f"rin:", rin)
            '''
            saved_button_Pin[rin] = buttonPin
        
        '''print("Line 169 saved_button_PIN   dopo ")
        print(saved_button_Pin)
        '''
        aved_button_id = button_id
        aved_button_label = button_label
        '''
        print("------POST----data from esp32 /Pstate-------button_id---------")
        print(button_id)
        print("-line 134 ----------data from esp32 /state-------buttonPin---------")
        print(buttonPin)
        print("---line 135 ######## POST ###--data from esp32 /Pstate-------button_label---------")
        print(button_label)
        print("---Line 138 ---------data from esp32 /Pstate----------------")
        print(data)
        print("-----------fine /Pstate ---data from esp32 ----------------")
        '''
        Sbutton_data = [{'buttonId': button_id, 'buttonLabel': button_label}]
        '''
        print("-line 141-------button data  dentro---------------------")
        print("#####  Line 142 ############   button_data   type  ######################")
        print(type(Sbutton_data))
        print(Sbutton_data)
        print("Line 157 saved_button_PIN")
        print(saved_button_Pin)
        print("Line 158 saved_button_labels")
        print(aved_button_label)
        '''
        session['button_id'] = button_id
        session['button_label'] = button_label
        '''
        print("lINE 150 session['button_label']")
        print(session['button_label'])
        '''
        return render_template('hity.html', button_data=Sbutton_data)

    # Handle GET request
    if not Sbutton_data:
        print("#line 151  impongo  Sbutton_data valori default   fuori Sbutton data#############")
        #print(Sbutton_data)
        
        button_id = session.get('button_id')
        button_label = session.get('button_label')
        #print("Line 165session.get('button_id')")
        #print(session.get('button_id'))
        Sbutton_data = [{'buttonId': button_id, 'buttonLabel': button_label}]
        #print("#line 155   Sbutton_data DOPO  fuori Sbutton data#############")
        print(Sbutton_data)
    
    # Ensure `aved_button_id` and `aved_button_label` have default values
    aved_button_id = aved_button_id if 'aved_button_id' in globals() else 0
    aved_button_label = aved_button_label if 'aved_button_label' in globals() else 'default'
    
    button_id = aved_button_id
    button_label = aved_button_label
    button_data = [{'buttonId': button_id, 'buttonLabel': button_label}]
    '''
    print("Line 182 saved_button_Pin")
    print(saved_button_Pin)
    print("Line 184 saved_button_labels")
    print(saved_button_labels)
    print("type(saved_button_labels) 512 ",type(saved_button_labels))
    '''
    result = []
    resultp = []

    for i in range(len(saved_button_Pin)):
        button_id = saved_button_Pin[i]
        #button_label = saved_button_labels[i]
        #button_label = saved_button_labels.split(", ")[i]
        #####button_label = saved_button_labels.strip("[]").split(", ")[i]
        button_label = saved_button_labels.strip("[]").split(", ")[i].strip('"')
        resultp.append( button_label)
        result.append({'buttonId': button_id, 'buttonLabel': button_label})
        print(" lINE  204  --result---:")

    print(result) 
    print(resultp) 
    print(type(resultp))
    print(" lINE  209  --result-TYPE--:")

    print(type(result))

    # Ensure that button_index is within the valid range
    button_index = 0
    if len(saved_button_labels) > 0:
        button_index = len(saved_button_labels) - 1
    print("#line 198  ##################     fuori Sbutton data####################")
    print(button_data)

    return render_template('toggle.html', num_buttons=num_buttons, button_labels= resultp, button_states=saved_button_states, button_data=result)

