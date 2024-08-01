import sqlite3, os
from datetime import datetime, timedelta


def create_dummy_positions_if_not_exists(database_path):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    portfolio_id = 1
    # Define positions with a past date
    past_date = datetime.now() - timedelta(days=365)  # 1 year ago
    positions = [("AAPL", 10), ("NVDA", 20), ("MS", 30)]

    # Insert positions into portfolio with ID 1 if they do not exist
    for symbol, shares in positions:
        c.execute(
            "SELECT id FROM positions WHERE symbol = ? AND portfolio_id = ?",
            (symbol, portfolio_id),
        )
        if not c.fetchone():
            c.execute(
                "INSERT INTO positions (symbol, shares, portfolio_id, position_time) VALUES (?, ?, ?, ?)",
                (symbol, shares, portfolio_id, past_date),
            )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_dummy_positions_if_not_exists(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "market.sqlite")
    )
