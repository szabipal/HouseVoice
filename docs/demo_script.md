# Demo Script

Run the app:

```bash
uvicorn app.main:app --reload
```

Create a user:

```bash
curl -s -X POST http://127.0.0.1:8000/users \
  -H 'Content-Type: application/json' \
  -d '{"display_name":"Alex","telegram_id":1001}'
```

Create a household:

```bash
curl -s -X POST http://127.0.0.1:8000/households \
  -H 'Content-Type: application/json' \
  -d '{"name":"Home","owner_user_id":1}'
```

Add shared inventory:

```bash
curl -s -X POST http://127.0.0.1:8000/households/1/inventory \
  -H 'Content-Type: application/json' \
  -d '{"user_id":1,"name":"pasta","quantity":500,"unit":"g","visibility":"shared"}'
```

Add private inventory:

```bash
curl -s -X POST http://127.0.0.1:8000/households/1/inventory \
  -H 'Content-Type: application/json' \
  -d '{"user_id":1,"name":"chocolate","quantity":1,"unit":"piece","visibility":"private"}'
```

Create a recipe:

```bash
curl -s -X POST http://127.0.0.1:8000/households/1/recipes \
  -H 'Content-Type: application/json' \
  -d '{"user_id":1,"name":"Pasta","servings":2,"ingredients":[{"name":"pasta","quantity":200,"unit":"g"}]}'
```

Check if it can be cooked:

```bash
curl -s 'http://127.0.0.1:8000/households/1/recipes/1/can-make?user_id=1'
```

Log the meal:

```bash
curl -s -X POST http://127.0.0.1:8000/households/1/recipes/1/meal-logs \
  -H 'Content-Type: application/json' \
  -d '{"user_id":1,"recipe_id":1,"servings":2,"notes":"demo"}'
```

List inventory:

```bash
curl -s 'http://127.0.0.1:8000/households/1/inventory?user_id=1'
```
