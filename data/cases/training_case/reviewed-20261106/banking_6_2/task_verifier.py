def verify_task_completion(initial_db_path: str, final_db_path: str, final_answer: str | None = None) -> dict:
    import sqlite3
    import re

    def safe_query(db_path: str, query: str, params: tuple = ()) -> list:
        try:
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception:
            return []

    # Get all card IDs from initial state
    initial_cards = safe_query(initial_db_path, "SELECT id FROM cards")
    initial_card_ids = {row[0] for row in initial_cards}

    # Get all cards from final state linked to account_id=3 (account ending in 4456)
    final_cards = safe_query(
        final_db_path,
        "SELECT id, account_id, card_type, spending_limit, currency, card_status FROM cards WHERE account_id = ?",
        (3,)
    )

    # Find new cards (cards that exist in final but not in initial)
    new_cards = [card for card in final_cards if card[0] not in initial_card_ids]

    if not new_cards:
        return {"result": "others"}

    # Check each new card to see if it matches ALL requirements
    for card in new_cards:
        card_id, account_id, card_type, spending_limit, currency, card_status = card

        # Verify all card properties
        if account_id != 3:
            continue
        if card_type != 'virtual':
            continue
        if spending_limit != 2000.0:
            continue
        if currency != 'USD':
            continue
        if card_status != 'active':
            continue

        # Now check card_controls for this card
        card_controls = safe_query(
            final_db_path,
            "SELECT international_allowed, allowed_countries FROM card_controls WHERE card_id = ?",
            (card_id,)
        )

        if not card_controls:
            continue

        international_allowed, allowed_countries = card_controls[0]

        # Verify international transactions are locked (international_allowed=0)
        if international_allowed != 0:
            continue

        # Verify allowed_countries contains US and CA
        if not allowed_countries:
            continue

        # Parse allowed countries (handle different formats like 'US,CA' or 'CA,US')
        countries = set(c.strip().upper() for c in allowed_countries.split(','))
        required_countries = {'US', 'CA'}

        if countries != required_countries:
            continue

        # All checks passed for this card
        return {"result": "complete"}

    # No card matched all requirements
    return {"result": "others"}