import sqlite3

DB_NAME = 'game_scores.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            game_id INTEGER NOT NULL,
            best_score INTEGER DEFAULT 0,
            UNIQUE(user_id, game_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (game_id) REFERENCES games(id)
        )''')

        conn.commit()

def get_connection():
    return sqlite3.connect(DB_NAME)

#User functions --------------------------------------------------------------------
def create_user(username, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        return cursor.lastrowid
    conn.commit()

def get_user_by_username(username):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password FROM users WHERE username = ?', (username,))
        return cursor.fetchone()
    
def get_user_by_id(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password FROM users WHERE id = ?', (user_id,))
        return cursor.fetchone()
    
def delete_user(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()

    
def save_score(user_id, game_id, score):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO scores (user_id, game_id, best_score)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, game_id) DO UPDATE SET best_score = 
            CASE 
                WHEN excluded.best_score > scores.best_score THEN excluded.best_score 
                ELSE scores.best_score 
            END
        ''', (user_id, game_id, score))
        conn.commit()
# --------------------------------------------------------------------

#Game functions --------------------------------------------------------------------
def create_game(name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO games (name) VALUES (?)', (name,))
        return cursor.lastrowid
    conn.commit()
    
    
def delete_game(game_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM games WHERE id = ?', (game_id,))
        conn.commit()

def get_game_by_id(game_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM games WHERE id = ?', (game_id,))
        return cursor.fetchone()


def game_exists(game_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM games WHERE id = ?', (game_id,))
        return cursor.fetchone()[0] > 0
    
def get_best_score(user_id, game_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT best_score FROM scores WHERE user_id = ? AND game_id = ?', (user_id, game_id))
        row = cursor.fetchone()
        return row[0] if row else 0
    
def get_best_score_of_game(game_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(best_score) FROM scores WHERE game_id = ?', (game_id,))
        return cursor.fetchone()[0] if cursor.fetchone() else 0

def get_all_users_with_scores_for_game(game_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT users.id, users.username, scores.best_score
            FROM scores
            JOIN users ON scores.user_id = users.id
            WHERE scores.game_id = ? AND scores.best_score > 0
            ORDER BY scores.best_score DESC
        ''', (game_id,))
        return cursor.fetchall()
    
def get_all_data():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT users.username, games.name, scores.best_score
            FROM scores
            JOIN users ON scores.user_id = users.id
            JOIN games ON scores.game_id = games.id
        ''')
        return cursor.fetchall()

    
#create empty db----------------------------------------------------
if __name__ == "__main__":
    init_db()
    print("Database and tables created!")