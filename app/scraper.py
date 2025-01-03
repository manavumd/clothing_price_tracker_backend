from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = FirecrawlApp()


class Product(BaseModel):
    """Schema for creating a new clothing product"""

    url: str = Field(description="The URL of the webpage")
    name: str = Field(description="The product name/title")
    currency: str = Field(description="Currency code (USD, etc)")
    price: float = Field(description="The current price of the product")


def scrape_price(url: str):
    try:
        extracted_data = app.scrape_url(
            url,
            params={
                "formats": ["extract"],
                "extract": {"schema": Product.model_json_schema()},
            },
        )


        return {"name":extracted_data["extract"]["name"],
                "price":extracted_data["extract"]["price"],
                "currency":extracted_data["extract"]["currency"],
                "timestamp":datetime.utcnow(),
                "url":url}
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None


if __name__ == "__main__":
    product = "https://www2.hm.com/en_us/productpage.0751471001.html"

    print(scrape_price(product))
