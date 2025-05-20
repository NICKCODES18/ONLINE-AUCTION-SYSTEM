 🛒 Online Auction System

An Online Auction System built using HTML for the frontend and Python with SQL for the backend, allowing users to view, bid, and store their entries for registered items. This project focuses on connecting a website to a SQL database using Python and demonstrates how to dynamically update tables based on user actions.

---

 📌 Features

 🔐 User Registration & Login
 📋 Browse Ongoing Auctions
 💰 Place Bids on Items
 🗂️ View and Store Bids in SQL
 🔄 Real-Time Database Updates

---

 🛠️ Tech Stack

| Layer          | Technology     |
| -------------- | -------------- |
| Frontend       | HTML, CSS      |
| Backend        | Python (Flask) |
| Database       | MySQL / SQLite |
| ORM (optional) | SQLAlchemy     |

---

 🚀 How It Works

1. Users access the site and view all current auction items.
2. Users can register/login securely.
3. Once logged in, users can place bids on auctioned items.
4. Bids are saved to the SQL database, and the item’s current highest bid is updated.
5. Users can review their bid history and active items.

---

 📂 Database Schema

 `users` Table

| Field    | Type    | Description     |
| -------- | ------- | --------------- |
| id       | INT     | Primary Key     |
| username | VARCHAR | Unique Username |
| password | VARCHAR | Hashed Password |

 `auctions` Table

| Field        | Type    | Description          |
| ------------ | ------- | -------------------- |
| id           | INT     | Primary Key          |
| item\_name   | VARCHAR | Item Description     |
| base\_price  | FLOAT   | Minimum Starting Bid |
| current\_bid | FLOAT   | Current Highest Bid  |

 `bids` Table

| Field       | Type     | Description            |
| ----------- | -------- | ---------------------- |
| id          | INT      | Primary Key            |
| user\_id    | INT      | Foreign Key → users    |
| auction\_id | INT      | Foreign Key → auctions |
| bid\_amount | FLOAT    | Bid Value              |
| timestamp   | DATETIME | Time of Bid            |

---

 ⚙️ Setup Instructions

1. Clone the repository

   ```bash
   git clone https://github.com/your-username/online-auction-system.git
   cd online-auction-system
   ```

2. Create and activate a virtual environment (optional but recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate   or venv\Scripts\activate on Windows
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Configure your SQL database

    Use SQLite or connect to MySQL
    Update `config.py` or `.env` with DB credentials

5. Initialize the database (if using SQLAlchemy)

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Run the application

   ```bash
   flask run
   ```

---



 🎯 Learning Objectives

 Connect a web interface with a relational database using Python.
 Perform real-time SQL updates through form submissions.
 Manage user sessions and secure bidding workflows.
 Use Flask to structure web routes and handle server-side logic.

---

 🧠 Future Enhancements

 Countdown timers for auction expiration
 Email alerts for successful bids or outbids
 Admin dashboard to manage items and users
 Upload images for auctioned items
 Pagination & filters for auctions

---

 👨‍💻 Author

Nikunj Jain
Connect: [LinkedIn](https://www.linkedin.com/in/nikunjjain29/) 


