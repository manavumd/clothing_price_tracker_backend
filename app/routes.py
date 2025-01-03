from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .models import Product, PriceHistory
from .database import get_db
from .scraper import scrape_price
from .notifications import send_email
from pydantic import BaseModel, Field

router = APIRouter()

class ProductRequest(BaseModel):
    url: str
    recipient_email: str

@router.post("/add_product")
def add_product(request: ProductRequest, db: Session = Depends(get_db)):
    """
    Endpoint to add a product to the database.

    Args:
        request (ProductRequest): The product request containing the URL.
        db (Session): Database session.

    Returns:
        dict: Confirmation message and scraped product details.
    """
    try:
        # Extract URL from the request body
        url = request.url
        recipient_email = request.recipient_email

        # Check if the product already exists
        existing_product = db.query(Product).filter(Product.url == url).first()
        if existing_product:
            raise HTTPException(status_code=400, detail="Product already exists in the database.")

        # Scrape the product details
        scraped_data = scrape_price(url)
        if not scraped_data:
            raise HTTPException(status_code=400, detail="Failed to scrape product details.")

        

        # Create a new product entry
        new_product = Product(
            name=scraped_data["name"],
            url=url,
            current_price=scraped_data["price"],
            recipient_email=recipient_email,
            currency=scraped_data["currency"]
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        # Add initial price to price history
        price_history = PriceHistory(product_id=new_product.id, price=new_product.current_price)
        db.add(price_history)
        db.commit()

        return {
            "message": "Product added successfully.",
            "product": {
                "name": new_product.name,
                "url": new_product.url,
                "current_price": new_product.current_price,
                "currency": new_product.currency,
                "recipient_email": new_product.recipient_email,
                "added_at": new_product.added_at
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/check_prices")
def check_prices(db: Session = Depends(get_db)):
    try:
        notifications = []

        # Fetch all products
        products = db.query(Product).all()

        for product in products:
            scraped_data = scrape_price(product.url)
            if not scraped_data:
                continue

            new_price = scraped_data["price"]

            # Check if the price has dropped
            if new_price < product.current_price:
                notifications.append({
                    "product_name": product.name,
                    "old_price": product.current_price,
                    "new_price": new_price
                })

                # Update the current price in the database
                current_price = product.current_price
                product.current_price = new_price

                # Add a new entry to the price history
                db.add(PriceHistory(product_id=product.id, price=new_price))
                db.commit()

                # Send email notification
                subject = f"Price Drop Alert for {product.name}"
                body = f"""
                Good news! The price of '{product.name}' has dropped!
                Old Price: ${current_price}
                New Price: ${new_price}
                Link: {product.url}

                Visit the link to grab the deal!
                """
                send_email(subject, body, product.recipient_email)

        return {"notifications": notifications}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
