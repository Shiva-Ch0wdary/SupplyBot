import re
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from transformers import pipeline
from typing import Dict, Any

from database import SessionLocal
from models import Product, Supplier

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the summarization pipeline with DistilBART
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Initialize the text-generation pipeline with DistilGPT2
generator = pipeline("text-generation", model="distilgpt2")


def get_db():
    """
    Dependency to provide a database session.
    Ensures that the session is closed after the request is processed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def parse_query(query: str) -> Dict[str, Any]:
    """
    Parses the user's query to determine the intent and extract relevant entities.
    Returns a dictionary containing the intent and extracted entities.
    """
    query_lower = query.lower().strip()
    intent = None
    entities = {}

    # Define regex patterns for different intents
    patterns = {
        "greeting": r"^(hello|hi|hey|greetings)\.?$",
        "price_filter": r"^(show me|list)\s+products\s+(under|above)\s+\$?(\d+\.?\d*)\.?$",
        "compare_products": r"^compare\s+([\w\s]+)\s+with\s+([\w\s]+)\.?$",
        "fetch_products": r"^(show me|list|display)\s+(all\s+)?products\s+(by|for|under)\s+brand\s+([\w\s]+)\.?$",
        "fetch_suppliers": r"^(which|what|list|tell me about)\s+suppliers\s+(that\s+)?(provide|offer)\s+([\w\s]+)\.?$",
        "product_details": r"^(give me|provide|show)\s+details\s+(of|about|for)\s+product\s+([\w\s]+)\.?$",
        "general_query": r".*"  # Catch-all for general queries
    }

    for key, pattern in patterns.items():
        match = re.match(pattern, query_lower)
        if match:
            intent = key
            if key == "greeting":
                pass
            elif key == "price_filter":
                entities["filter_type"] = match.group(2).strip()
                entities["price"] = float(match.group(3).strip())
            elif key == "compare_products":
                entities["product_a"] = match.group(1).strip()
                entities["product_b"] = match.group(2).strip()
            elif key == "fetch_products":
                entities["brand"] = match.group(4).strip()
            elif key == "fetch_suppliers":
                entities["category"] = match.group(4).strip()
            elif key == "product_details":
                entities["product_name"] = match.group(4).strip()
            break

    if not intent:
        intent = "general_query"
        entities["question"] = query.strip()

    logger.info(f"Parsed query '{query}' as intent '{intent}' with entities {entities}")
    return {"intent": intent, "entities": entities}


def enhance_response(text: str, mode: str = "summarize") -> str:
    """
    Enhances the given text using the appropriate model to provide more context or clarity.
    Mode can be 'summarize', 'generate', or 'greeting'.
    """
    try:
        if mode == "summarize":
            input_length = len(text.split())
            if input_length < 10:
                return text  # If text is too short, return it as is
            
            # Dynamically set max_length and min_length based on input length
            max_length = min(100, int(input_length * 1.5))  # 1.5 times input length
            min_length = min(30, input_length)  # Ensure min_length does not exceed input length

            enhanced = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return enhanced[0]["summary_text"].strip()

        elif mode == "generate":
            prompt = f"User: {text}\nBot:"
            enhanced = generator(prompt, max_length=150, num_return_sequences=1, do_sample=False)
            response = enhanced[0]["generated_text"].strip()
            if "Bot:" in response:
                return response.split("Bot:")[1].strip()
            return response

        elif mode == "greeting":
            return "Hello! How can I assist you today?"

    except Exception as e:
        logger.error(f"Error in enhance_response: {e}")
        return "I'm sorry, I couldn't process your request."


@router.post("/chat")
def handle_chat(query: str, db: Session = Depends(get_db)):
    """
    Main endpoint to handle chatbot queries.
    """
    parsed = parse_query(query)
    intent = parsed.get("intent")
    entities = parsed.get("entities")

    try:
        if intent == "greeting":
            return {"response": enhance_response(query, mode="greeting")}

        elif intent == "product_details":
            product_name = entities.get("product_name")
            if not product_name:
                return {"response": "Please specify the product name to fetch details."}

            product = db.query(Product).filter(Product.name.ilike(f"%{product_name}%")).first()
            if not product:
                logger.info(f"Product '{product_name}' not found.")
                return {"response": f"No product found with name '{product_name}'."}

            product_details = {
                "id": product.id,
                "name": product.name,
                "brand": product.brand,
                "price": product.price,
                "category": product.category,
                "description": enhance_response(product.description, mode="summarize"),
            }
            return {"response": product_details}

        elif intent == "fetch_products":
            brand = entities.get("brand")
            if not brand:
                return {"response": "Please specify a brand to fetch products."}

            products = db.query(Product).filter(Product.brand.ilike(f"%{brand}%")).all()
            if not products:
                logger.info(f"No products found under brand '{brand}'.")
                return {"response": f"No products found for brand '{brand}'."}

            return {
                "response": [
                    {
                        "id": p.id,
                        "name": p.name,
                        "brand": p.brand,
                        "price": p.price,
                        "category": p.category,
                        "description": enhance_response(p.description, mode="summarize"),
                    }
                    for p in products
                ]
            }

        elif intent == "price_filter":
            filter_type = entities.get("filter_type")
            price = entities.get("price")
            if not filter_type or not price:
                return {"response": "Please specify whether to filter products 'under' or 'above' a price."}

            products = db.query(Product).filter(
                Product.price <= price if filter_type == "under" else Product.price >= price
            ).all()
            if not products:
                return {"response": f"No products found for the selected price filter."}

            return {
                "response": [
                    {
                        "id": p.id,
                        "name": p.name,
                        "brand": p.brand,
                        "price": p.price,
                        "category": p.category,
                        "description": enhance_response(p.description, mode="summarize"),
                    }
                    for p in products
                ]
            }

        elif intent == "fetch_suppliers":
            category = entities.get("category")
            if not category:
                return {"response": "Please specify the product category to fetch suppliers."}

            suppliers = db.query(Supplier).filter(Supplier.product_categories_offered.ilike(f"%{category}%")).all()
            if not suppliers:
                return {"response": f"No suppliers found offering '{category}' products."}

            return {
                "response": [
                    {
                        "id": s.id,
                        "name": s.name,
                        "contact_info": s.contact_info,
                        "product_categories_offered": s.product_categories_offered,
                        "summary": enhance_response(
                            f"Supplier Name: {s.name}\nContact Info: {s.contact_info}\nCategories Offered: {s.product_categories_offered}",
                            mode="summarize"
                        ),
                    }
                    for s in suppliers
                ]
            }

        elif intent == "compare_products":
            product_a = entities.get("product_a")
            product_b = entities.get("product_b")
            if not product_a or not product_b:
                return {"response": "Please specify both products to compare."}

            product_a_data = db.query(Product).filter(Product.name.ilike(f"%{product_a}%")).first()
            product_b_data = db.query(Product).filter(Product.name.ilike(f"%{product_b}%")).first()

            if not product_a_data or not product_b_data:
                missing = ", ".join(p for p in [product_a, product_b] if not eval(f"product_{p.lower()}_data"))
                return {"response": f"Could not find product(s): {missing}."}

            return {
                "response": {
                    "Product A": {
                        "Name": product_a_data.name,
                        "Brand": product_a_data.brand,
                        "Price": product_a_data.price,
                        "Category": product_a_data.category,
                        "Description": enhance_response(product_a_data.description, mode="summarize"),
                    },
                    "Product B": {
                        "Name": product_b_data.name,
                        "Brand": product_b_data.brand,
                        "Price": product_b_data.price,
                        "Category": product_b_data.category,
                        "Description": enhance_response(product_b_data.description, mode="summarize"),
                    },
                }
            }

        else:
            return {"response": "I'm sorry, I couldn't understand your request. Could you clarify further?"}

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again later.")
