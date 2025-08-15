import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import pandas as pd
classified = pd.read_csv('Classified.csv')

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/options')
def options_page():
    return render_template('options.html')

@app.route("/logging_waste")
def logging_waste_page():
    return render_template('logging_waste.html')

@app.route('/community')
def community_page():
    with open(os.path.join('templates','posts.html'), 'r') as file:
        data = {
            'posts': file.read()
        }
    return render_template('community.html', **data)

@app.route('/login2', methods=['POST'])
def login():
    global classified, account
    data = request.get_json()
    account = data.get('email')
    entered_password = data.get('password')
    if account in classified['account'].values:
            user_data = classified[classified['account'] == account].iloc[0]
            saved_password = user_data['password']
            if saved_password != entered_password:
                return jsonify({'message': "Wrong password", "redirect": 0})
            else:
                return jsonify({'message': "Logged in successfully!", 'redirect': 1})
    else:
        return jsonify({'message': "Account not found. Sign up.", "redirect": 0})


@app.route('/signup2', methods = ['POST'])
def signup():
    global classified, account
    data = request.get_json()
    account = data.get('email')
    if account in classified['account'].values:
        return jsonify({'message': "account already exists. Login.", 'redirect': 2})
    password = data.get('password')
    if len(password) < 8:
        return jsonify({'message' : "Password is too short. It should be at least 8 charachters long",
                        'redirect':0})
    name = data.get('name')
    address = data.get('address')
    saved = {
        "name": name,
        "account": account,
        "password": password,
        "address": address
    }
    classified = pd.concat([classified, pd.DataFrame([saved])], ignore_index=True)
    classified.to_csv('Classified.csv', index=False)
    return jsonify({'message': 'Account added', 'redirect': 1})

@app.route("/logging_waste2", methods=['POST'])
def logging_waste():
    data = request.get_json()

    food_type = data.get('type')
    food_name = data.get('name')
    date_of_making = data.get('date')

    user_data = classified[classified['account'] == account].iloc[0]

    food_name_html = food_name.replace('"', '&quot;')
    food_type_html = food_type.replace('"', '&quot;')
    date_html = date_of_making.replace('"', '&quot;')
    user_name = user_data["name"].replace('"', '&quot;')
    user_address = user_data["address"].replace('"', '&quot;')

    # make post
    post = f'<div class="food-card">'
    post += f' <h2>{food_name_html}</h2>'
    post += f' <p>Type: {food_type_html}</p>'
    post += f' <p>Made on: {date_html}</p>'
    post += f' <p>From: {user_name} - {user_address}</p>'
    post += f' <button onclick="order(\'{food_name_html}\', \'{food_type_html}\', \'{date_html}\', \'{user_name}\', \'{user_address}\', \'{account}\')">Order</button>'
    post += '</div>'

    # Append to posts file
    with open(os.path.join('templates','posts.html'), 'r', encoding='utf-8') as file:
        old_content = file.read()

    # Write new content at the top
    with open(os.path.join('templates','posts.html'), 'w', encoding='utf-8') as file:
        file.write(f'{post}\n{old_content}')

    return jsonify({"status": "success", "message": "Post added"}), 200

@app.route('/order', methods=['POST'])
def order():
    data = request.get_json()
    food_name = data.get('food_name')
    food_type = data.get('food_type')
    date = data.get('date')
    user_name = data.get('user_name')
    food_sender_email = data.get('account')
    address = data.get('address')
    sender_email = "###"
    receiver_email = account
    password = '###'
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "A Rebite Order"

    data = {
        'food_name': food_name,
        'user_name': user_name,
        'food_sender_email': food_sender_email,
        'address': address,
        'account': account,
        'date': date,
        'food_type': food_type
    }

    body = render_template('email.html', **data)
    message.attach(MIMEText(body, "html"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("✅ Email sent successfully!")

    with open(os.path.join('templates','posts.html'), 'r', encoding='utf-8') as file:
        lines = file.readlines()
    post = f'<div class="food-card">'
    post += f' <h2>{food_name}</h2>'
    post += f' <p>Type: {food_type}</p>'
    post += f' <p>Made on: {date}</p>'
    post += f' <p>From: {user_name} - {address}</p>'
    post += f' <button onclick="order(\'{food_name}\', \'{food_type}\', \'{date}\', \'{user_name}\', \'{address}\', \'{food_sender_email}\')">Order</button>'
    post += '</div>'
    
    lines = [line.strip() for line in lines]
    lines.remove(post)

    with open(os.path.join('templates','posts.html'), 'w', encoding='utf-8') as file:
        for line in lines:    
            file.write(line + '\n')


    return jsonify({'message': "Success! Check your email for more info."})

if __name__ == '__main__':
    app.run(debug=True)