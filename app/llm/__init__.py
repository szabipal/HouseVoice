try:
    from app.legacy_llm import (
        answer_grocery_question,
        ask_llm,
        classify_intent,
        classify_route,
        estimate_expiration_dates,
        estimate_meal_consumption,
        general_chat,
        generate_plan,
        generate_task_titles,
        get_client,
        parse_expense,
    )
except Exception:  # pragma: no cover - compatibility only
    pass
