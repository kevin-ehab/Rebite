# 🥗 ReBite – Community Food Waste Sharing Platform

**ReBite** is a Flask-based web application that helps reduce food waste by allowing community members to log and share excess food. Users can offer leftover or untouched food to others in their area, categorized as:

- 🐾 **For Pets** – suitable for animal consumption  
- 🍽️ **Untouched** – fresh and edible food for people
<p align="center">
  <img src="static/logo.png" alt="Description" width="300"/>
</p>

---

## 🌍 Purpose

Every day, tons of edible food are thrown away while others go hungry. **ReBite** was created to solve this problem by:

- Reducing food waste in communities
- Sharing extra food with those who need it
- Creating a sustainable, sharing-based food ecosystem

---

## ✨ Features

- 🔐 **User Authentication**
  - Secure signup & login
  - Password validation (8+ characters)

- 📝 **Log Waste**
  - Add a food name, type (for pets / untouched), and preparation date
  - Posts include the sharer's name and location

- 📢 **Community Feed**
  - View logged food as shareable cards
  - Each card has an **Order** button to request the item

- 📧 **Order System**
  - Clicking **Order** sends a request and simulates an email to the giver

---

## 📁 File Structure

```
├── app.py
├── Classified.csv
├── posts.html
├── static
│   ├── community.css
│   ├── community.js
│   ├── logging_waste.css
│   ├── logging_waste.js
│   ├── login&signup.css
│   ├── login.js
│   ├── logo.png
│   ├── options.css
│   ├── signup.js
│   └── style.css
└── templates
    ├── community.html
    ├── index.html
    ├── logging_waste.html
    ├── login.html
    ├── options.html
    └── signup.html
```

---

## 🕹️ Demo-Link: <a href="https://rebite.pythonanywhere.com">Rebite.com</a>

---

## 📌 Notes

- Data is stored locally in CSV and HTML files (no database required).
- Passwords are stored as plaintext for simplicity – for production, use hashed passwords.
- No real email is sent when ordering – this can be integrated later using services like SendGrid or SMTP.

---

## 🤝 Contribution

Have ideas to improve ReBite? Feel free to fork the repo and submit pull requests!

---

## 📃 License

This project is open-source under the MIT License.

---

## ❤️ Built With

- Python & Flask
- HTML/CSS (Jinja2 templating)
- pandas
