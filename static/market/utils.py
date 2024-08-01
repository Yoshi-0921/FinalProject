import sqlite3, os
from datetime import datetime, timedelta


def intialize_dummy_positions_if_not_exists(database_path):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    # Drop the existing positions table if it exists
    c.execute("DROP TABLE IF EXISTS positions")

    # Create the new positions table with position_time as an integer
    c.execute(
        """
    CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        shares INTEGER NOT NULL,
        portfolio_id INTEGER NOT NULL,
        position_time INTEGER NOT NULL,
        FOREIGN KEY(portfolio_id) REFERENCES portfolios(id)
    );
    """
    )

    portfolio_id = 1
    # Define positions with a past date
    past_date = datetime.now() - timedelta(days=365)  # 1 year ago
    past_timestamp = int(past_date.timestamp())  # Convert to Unix timestamp
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
                (symbol, shares, portfolio_id, past_timestamp),
            )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    intialize_dummy_positions_if_not_exists(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "market.sqlite")
    )
