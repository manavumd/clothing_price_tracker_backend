# Clothing Price Tracker Backend

This backend application tracks prices for clothing items from various e-commerce websites. It allows users to monitor product prices, store product details, track price changes over time, and receive email notifications when prices drop.

---

## Features

- **Add Clothing Products**:
  - Users can add clothing product URLs and recipient emails for tracking.
  - Product details (name, price) are automatically scraped using the Firecrawl SDK.
- **Price Tracking**:
  - Periodic checks to monitor price changes.
  - Maintains a history of price changes for each product.
- **Email Notifications**:
  - Sends alerts to users when prices drop for tracked items.
- **Support for Clothing Websites**:
  - Designed for e-commerce clothing platforms like H&M, Zara, and similar.

---

## Technologies Used

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Web Scraping**: Firecrawl SDK
- **Email Notifications**: Python `smtplib`

---

## Prerequisites

- Python 3.9 or higher
- PostgreSQL database
- Firecrawl API key
- SMTP server credentials (e.g., Gmail)

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd clothing-price-tracker-backend
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the root directory:
   ```
   DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database>
   FIRECRAWL_API_KEY=<your-firecrawl-api-key>
   MAIL_APP_EMAIL=<your-email>
   MAIL_APP_PASSWORD=<your-email-password>
   ```

5. **Set Up Database**:
   Create the required tables:
   ```sql
   CREATE TABLE products (
       `id` int NOT NULL AUTO_INCREMENT,
        `name` varchar(255) NOT NULL,
        `url` varchar(500) NOT NULL,
        `current_price` float NOT NULL,
        `added_at` datetime DEFAULT NULL,
        `recipient_email` text NOT NULL,
        `currency` text NOT NULL,
   );

   CREATE TABLE price_history (
       id SERIAL PRIMARY KEY,
       product_id INT REFERENCES products(id) ON DELETE CASCADE,
       price FLOAT NOT NULL,
       timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

---

## Usage

1. **Start the Server**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **API Endpoints**:

   - **Add a Clothing Product**:
     - **Endpoint**: `POST /add_product`
     - **Description**: Adds a clothing product URL and recipient email to track price changes.
     - **Request Body**:
       ```json
       {
           "url": "https://example.com/product-page",
           "recipient_email": "user@example.com"
       }
       ```
     - **Response**:
       ```json
       {
           "message": "Product added successfully.",
           "product": {
               "name": "Example Clothing Item",
               "url": "https://example.com/product-page",
               "current_price": 49.99,
               "recipient_email": "user@example.com",
               "added_at": "2025-01-02T15:00:00.000000"
           }
       }
       ```

   - **Check Prices**:
     - **Endpoint**: `GET /check_prices`
     - **Description**: Checks current prices for all products, updates the database, and sends email notifications if prices drop.
     - **Response**:
       ```json
       {
           "notifications": [
               {
                   "product_name": "Example Clothing Item",
                   "old_price": 49.99,
                   "new_price": 39.99
               }
           ]
       }
       ```

---

## Scheduler

To check prices periodically:
- **Using Cron Job**:
  Add this line to your crontab (`crontab -e`):
  ```bash
  0 */8 * * * curl -X GET http://127.0.0.1:8000/check_prices
  ```
- **Using APScheduler**:
  Add a periodic job in your application to call the `check_prices` logic every 8 hours.

---

