from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
from datetime import datetime, timedelta
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Connect to the MySQL database
def get_db_connection():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="nikunjjain2005@SQL",
        database="auctiondb"
    )
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT auction_id, item_name, start_price, end_time FROM auctions")
    auctions = cursor.fetchall()

    cursor.execute("SELECT auction_id, MAX(bid_amount) AS highest_bid FROM bids GROUP BY auction_id")
    highest_bids = cursor.fetchall()

    auction_data = []
    for auction in auctions:
        auction_id = auction[0]
        highest_bid = next((bid[1] for bid in highest_bids if bid[0] == auction_id), auction[2])
        auction_data.append({
            'auction_id': auction_id,
            'item_name': auction[1],
            'start_price': auction[2],
            'highest_bid': highest_bid,
            'end_time': auction[3]
        })

    cursor.close()
    conn.close()
    return render_template('index.html', auctions=auction_data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            flash('Username already exists!')
            return redirect(url_for('register'))
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password_hash = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials!')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

@app.route('/createauction', methods=['GET', 'POST'])
def create_auction():
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        item_name = request.form['item_name']
        start_price = float(request.form['start_price'])
        end_time = request.form['end_time']

        # Debug print statements
        print(f"Creating auction with item_name={item_name}, start_price={start_price}, end_time={end_time}, user_id={session['user_id']}")

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO auctions (item_name, start_price, end_time, user_id) VALUES (%s, %s, %s, %s)",
                           (item_name, start_price, end_time, session['user_id']))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Auction created successfully!')
            return redirect(url_for('home'))
        except Exception as e:
            flash(f"Error occurred: {e}")
            print(e)
            return redirect(url_for('create_auction'))

    return render_template('createauction.html')

@app.route('/auction/<int:auction_id>', methods=['GET', 'POST'])
def auction_detail(auction_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM auctions WHERE auction_id = %s", (auction_id,))
    auction = cursor.fetchone()

    cursor.execute("SELECT MAX(bid_amount) FROM bids WHERE auction_id = %s", (auction_id,))
    highest_bid = cursor.fetchone()[0] or auction[2]

    if request.method == 'POST':
        if 'user_id' not in session:
            flash('Please login to place a bid.')
            return redirect(url_for('login'))
        bid_amount = float(request.form['bid_amount'])
        if bid_amount <= highest_bid:
            flash('Bid must be higher than the current highest bid.')
        else:
            cursor.execute("INSERT INTO bids (auction_id, user_id, bid_amount, bid_time) VALUES (%s, %s, %s, %s)",
                           (auction_id, session['user_id'], bid_amount, datetime.now()))
            conn.commit()
            flash('Bid placed successfully!')
        return redirect(url_for('auction_detail', auction_id=auction_id))  # ✅ fixed line

    cursor.execute(""" 
    SELECT b.bid_amount, u.username, b.bid_time 
    FROM bids b 
    JOIN users u ON b.user_id = u.user_id 
    WHERE b.auction_id = %s 
    ORDER BY b.bid_amount DESC
    """, (auction_id,))

    bids = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('auctiondetails.html', auction=auction, bids=bids, highest_bid=highest_bid)

if __name__ == '__main__':
    app.run(debug=True)
