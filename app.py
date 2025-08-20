import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os

import pandas as pd
classified = pd.read_csv('Classified.csv')

import json
with open("posts.json") as f:
    posts = json.load(f)

from flask import Flask, render_template, jsonify, request, session
app = Flask(__name__)
app.secret_key = os.urandom(24)

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
    return render_template('community.html', posts=posts[::-1])

@app.route('/explore', methods=['POST'])
def explore():
    session['account'] = None
    return jsonify({"message": "explore"})

@app.route('/login2', methods=['POST'])
def login():
    global classified
    data = request.get_json()
    account = data.get('email')
    entered_password = data.get('password')
    if account in classified['account'].values:
            session['account'] = account
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
    global classified
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
    session['account'] = account
    classified = pd.concat([classified, pd.DataFrame([saved])], ignore_index=True)
    classified.to_csv('Classified.csv', index=False)
    return jsonify({'message': 'Account added', 'redirect': 1})

@app.route("/logging_waste2", methods=['POST'])
def logging_waste():
    global posts
    account = session.get("account")
    if not account:
        return jsonify({"status": "error", "message": "Not logged in"}), 401
    
    food_type = request.form.get('type')
    food_name = request.form.get('name')
    date_of_making = request.form.get('date')

    user_data = classified[classified['account'] == account].iloc[0]
    user_name = user_data["name"].replace('"', '&quot;')

    #saving the image to be used
    image = request.files.get('image')
    image.save(os.path.join('static', 'image_uploads', f'{food_name}-{date_of_making}-{user_name}.jpg'))

    food_name_html = food_name.replace('"', '&quot;')
    food_type_html = food_type.replace('"', '&quot;')
    date_html = date_of_making.replace('"', '&quot;')
    user_address = user_data["address"].replace('"', '&quot;')
    image_path = os.path.join("static", "image_uploads", f"{food_name}-{date_of_making}-{user_name}.jpg")
    # make post

    posts.append({
        'image_path': image_path,
        'food_name_html': food_name_html,
        'food_type_html': food_type_html,
        'date_html': date_html,
        'user_address': user_address,
        'user_name': user_name,
        'account': account
    })
    with open("posts.json", "w") as f:
        json.dump(posts, f, indent=4)

    return jsonify({"status": "success", "message": "Post added"})

@app.route('/order', methods=['POST'])
def order():
    global posts
    account = session.get("account")
    if not account:
        return jsonify({"error": 1, "message": "Not logged in"}), 401
    data = request.get_json()
    food_name = data.get('food_name')
    food_type = data.get('food_type')
    date = data.get('date')
    user_name = data.get('user_name')
    food_sender_email = data.get('account')
    address = data.get('address')
    image_path = os.path.join("static", "image_uploads", f"{food_name}-{date}-{user_name}.jpg")
    sender_email = "kevinplays165@gmail.com"
    receiver_email = account
    password = 'bymiztbypmfztxaw'

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
        'food_type': food_type,
    }

    body = render_template('email.html', **data)
    message.attach(MIMEText(body, "html"))

    with open(image_path, "rb") as img_file:
        img = MIMEImage(img_file.read())
        img.add_header("Content-ID", "<image1>")
        message.attach(img)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


    print("✅ Email sent successfully!")

    #Remove the post

    for i in posts:
        if i['image_path'] == image_path:
            posts.remove(i)
            with open("posts.json", "w") as f:
                json.dump(posts, f, indent=4)
            break

    return jsonify({'message': "Success! Check your email for more info."})

if __name__ == '__main__':
    app.run(debug=True)