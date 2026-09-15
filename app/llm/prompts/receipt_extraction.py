PROMPT = (
    "This is a supermarket receipt. Extract every grocery product and return a JSON array. "
    "Each object must have these fields: "
    "name (string, the product name cleaned up), "
    "quantity (number, how many units were bought), "
    "unit (string: 'piece', 'g', 'kg', 'ml', 'l', 'pack', etc.), "
    "price (number, the line total, or null if unclear). "
    "Skip non-food items like bags, deposit fees, loyalty points, and totals. "
    "Return only the raw JSON array with no markdown or explanation."
)
