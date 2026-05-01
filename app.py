from flask import Flask, render_template, request, jsonify, session
import random, json

app = Flask(__name__)
app.secret_key = "grocery_ai_secret_2026"

# Product database
PRODUCTS = [
    {"id": 1, "name": "Organic Whole Milk", "category": "dairy", "price": 320, "tags": ["healthy", "calcium", "kids"], "rating": 4.8, "emoji": "🥛", "stock": 50},
    {"id": 2, "name": "Greek Yogurt", "category": "dairy", "price": 180, "tags": ["healthy", "protein", "probiotic"], "rating": 4.7, "emoji": "🍶", "stock": 30},
    {"id": 3, "name": "Cheddar Cheese", "category": "dairy", "price": 450, "tags": ["kids", "snack", "calcium"], "rating": 4.5, "emoji": "🧀", "stock": 25},
    {"id": 4, "name": "Brown Eggs (12 pack)", "category": "dairy", "price": 280, "tags": ["protein", "healthy", "breakfast"], "rating": 4.9, "emoji": "🥚", "stock": 60},
    {"id": 5, "name": "Whole Wheat Bread", "category": "bakery", "price": 150, "tags": ["healthy", "fiber", "breakfast"], "rating": 4.3, "emoji": "🍞", "stock": 40},
    {"id": 6, "name": "Sourdough Loaf", "category": "bakery", "price": 220, "tags": ["artisan", "probiotic", "breakfast"], "rating": 4.8, "emoji": "🥖", "stock": 15},
    {"id": 7, "name": "Croissants (4 pack)", "category": "bakery", "price": 190, "tags": ["snack", "kids", "breakfast"], "rating": 4.6, "emoji": "🥐", "stock": 20},
    {"id": 8, "name": "Basmati Rice (5kg)", "category": "grains", "price": 850, "tags": ["staple", "gluten-free", "family"], "rating": 4.9, "emoji": "🍚", "stock": 100},
    {"id": 9, "name": "Rolled Oats", "category": "grains", "price": 200, "tags": ["healthy", "fiber", "breakfast"], "rating": 4.7, "emoji": "🌾", "stock": 45},
    {"id": 10, "name": "Pasta (Spaghetti)", "category": "grains", "price": 130, "tags": ["family", "quick-cook", "dinner"], "rating": 4.4, "emoji": "🍝", "stock": 80},
    {"id": 11, "name": "Chicken Breast (1kg)", "category": "meat", "price": 700, "tags": ["protein", "healthy", "fitness"], "rating": 4.8, "emoji": "🍗", "stock": 35},
    {"id": 12, "name": "Ground Beef (500g)", "category": "meat", "price": 550, "tags": ["protein", "family", "dinner"], "rating": 4.5, "emoji": "🥩", "stock": 28},
    {"id": 13, "name": "Salmon Fillet", "category": "seafood", "price": 1200, "tags": ["healthy", "omega-3", "protein"], "rating": 4.9, "emoji": "🐟", "stock": 12},
    {"id": 14, "name": "Broccoli", "category": "vegetables", "price": 120, "tags": ["healthy", "fiber", "vitamin-c"], "rating": 4.6, "emoji": "🥦", "stock": 50},
    {"id": 15, "name": "Spinach (bag)", "category": "vegetables", "price": 90, "tags": ["healthy", "iron", "fitness"], "rating": 4.5, "emoji": "🌿", "stock": 40},
    {"id": 16, "name": "Tomatoes (1kg)", "category": "vegetables", "price": 100, "tags": ["healthy", "vitamin-c", "salad"], "rating": 4.7, "emoji": "🍅", "stock": 60},
    {"id": 17, "name": "Bananas (1kg)", "category": "fruits", "price": 80, "tags": ["healthy", "potassium", "kids"], "rating": 4.8, "emoji": "🍌", "stock": 70},
    {"id": 18, "name": "Apples (1kg)", "category": "fruits", "price": 150, "tags": ["healthy", "fiber", "snack"], "rating": 4.7, "emoji": "🍎", "stock": 55},
    {"id": 19, "name": "Orange Juice (1L)", "category": "beverages", "price": 250, "tags": ["vitamin-c", "breakfast", "kids"], "rating": 4.5, "emoji": "🍊", "stock": 30},
    {"id": 20, "name": "Green Tea (25 bags)", "category": "beverages", "price": 200, "tags": ["healthy", "antioxidant", "fitness"], "rating": 4.8, "emoji": "🍵", "stock": 40},
    {"id": 21, "name": "Olive Oil (500ml)", "category": "oils", "price": 650, "tags": ["healthy", "cooking", "mediterranean"], "rating": 4.9, "emoji": "🫒", "stock": 25},
    {"id": 22, "name": "Dark Chocolate (100g)", "category": "snacks", "price": 180, "tags": ["antioxidant", "snack", "treat"], "rating": 4.7, "emoji": "🍫", "stock": 45},
    {"id": 23, "name": "Mixed Nuts (250g)", "category": "snacks", "price": 420, "tags": ["healthy", "protein", "snack"], "rating": 4.8, "emoji": "🥜", "stock": 35},
    {"id": 24, "name": "Honey (500g)", "category": "condiments", "price": 380, "tags": ["natural", "healthy", "kids"], "rating": 4.9, "emoji": "🍯", "stock": 20},
]

def ai_recommend(preferences, budget, family_size, health_goals):
    """AI recommendation engine based on user profile"""
    scored = []
    for product in PRODUCTS:
        score = 0
        tags = product["tags"]
        
        # Health goal matching
        if "weight-loss" in health_goals:
            if any(t in tags for t in ["healthy", "protein", "fiber"]):
                score += 30
        if "muscle-gain" in health_goals:
            if "protein" in tags:
                score += 35
        if "family" in health_goals:
            if any(t in tags for t in ["family", "kids"]):
                score += 25
        if "energy" in health_goals:
            if any(t in tags for t in ["breakfast", "healthy"]):
                score += 20
                
        # Preference matching
        for pref in preferences:
            if pref in tags:
                score += 20
                
        # Budget filter
        if product["price"] <= budget:
            score += 15
        elif product["price"] <= budget * 1.2:
            score += 5
            
        # Family size
        if family_size > 3 and any(t in tags for t in ["family", "staple"]):
            score += 10
            
        # Rating bonus
        score += (product["rating"] - 4.0) * 20
        
        # Random slight variation (AI "creativity")
        score += random.uniform(-5, 5)
        
        if score > 20:
            scored.append({**product, "match_score": round(score, 1)})
    
    # Sort by score
    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return scored[:8]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    preferences = data.get("preferences", [])
    budget = int(data.get("budget", 500))
    family_size = int(data.get("family_size", 2))
    health_goals = data.get("health_goals", [])
    
    recommendations = ai_recommend(preferences, budget, family_size, health_goals)
    
    session["cart"] = session.get("cart", [])
    
    return jsonify({
        "recommendations": recommendations,
        "total_products": len(PRODUCTS),
        "ai_message": f"Found {len(recommendations)} perfect matches for your profile!"
    })

@app.route("/all-products")
def all_products():
    return jsonify(PRODUCTS)

@app.route("/cart/add", methods=["POST"])
def add_to_cart():
    data = request.json
    cart = session.get("cart", [])
    product_id = data.get("product_id")
    
    # Find existing
    for item in cart:
        if item["id"] == product_id:
            item["qty"] += 1
            session["cart"] = cart
            return jsonify({"cart": cart, "message": "Quantity updated!"})
    
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if product:
        cart.append({**product, "qty": 1})
        session["cart"] = cart
        return jsonify({"cart": cart, "message": f"{product['name']} added to cart!"})
    
    return jsonify({"error": "Product not found"}), 404

@app.route("/cart/remove", methods=["POST"])
def remove_from_cart():
    data = request.json
    cart = session.get("cart", [])
    cart = [item for item in cart if item["id"] != data.get("product_id")]
    session["cart"] = cart
    return jsonify({"cart": cart})

@app.route("/cart", methods=["GET"])
def get_cart():
    cart = session.get("cart", [])
    total = sum(item["price"] * item["qty"] for item in cart)
    return jsonify({"cart": cart, "total": total})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
