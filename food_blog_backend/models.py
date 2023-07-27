MAKE_MEASURES = """
CREATE TABLE IF NOT EXISTS measures (
    measure_id INTEGER PRIMARY KEY,
    measure_name TEXT UNIQUE
)
"""

MAKE_INGREDIENTS = """
CREATE TABLE IF NOT EXISTS ingredients (
    ingredient_id INTEGER PRIMARY KEY,
    ingredient_name TEXT NOT NULL UNIQUE
)
"""

MAKE_MEALS = """
CREATE TABLE IF NOT EXISTS meals (
    meal_id INTEGER PRIMARY KEY,
    meal_name TEXT NOT NULL UNIQUE
)
"""

MAKE_RECIPE = """
CREATE TABLE IF NOT EXISTS recipes (
    recipe_id INTEGER PRIMARY KEY,
    recipe_name TEXT NOT NULL,
    recipe_description TEXT
)
"""

MAKE_SERVES = """
CREATE TABLE IF NOT EXISTS serve (
    serve_id INTEGER PRIMARY KEY,
    meal_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    FOREIGN KEY (meal_id) REFERENCES meals (meal_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id)
)
"""

MAKE_QUANTITY = """
CREATE TABLE IF NOT EXISTS quantity (
    quantity_id INTEGER PRIMARY KEY,
    quantity INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    measure_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id),
    FOREIGN KEY (measure_id) REFERENCES measures (measure_id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients (ingredient_id)
)
"""


def make_tables(conn):
    conn.execute(MAKE_MEASURES)
    conn.execute(MAKE_INGREDIENTS)
    conn.execute(MAKE_MEALS)
    conn.execute(MAKE_RECIPE)
    conn.execute(MAKE_SERVES)
    conn.execute(MAKE_QUANTITY)
