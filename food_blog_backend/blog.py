import sqlite3
from models import make_tables
import argparse


def make_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("database_name", type=str)
    parser.add_argument("--ingredients", type=str)
    parser.add_argument("--meals", type=str)
    return parser.parse_args()


def populate_tables():
    cur.execute(
        """
        INSERT INTO meals (meal_name)
        VALUES ('breakfast'), ('brunch'), ('lunch'), ('supper')
    """
    )

    cur.execute(
        """
        INSERT INTO ingredients (ingredient_name)
        VALUES ('milk'), ('cacao'), ('strawberry'), 
        ('blueberry'), ('blackberry'), ('sugar')
    """
    )

    cur.execute(
        """
        INSERT INTO measures (measure_name)
        VALUES ('ml'), ('g'), ('l'), ('cup'),
        ('tbsp'), ('tsp'), ('dsp'), ('bruh')
    """
    )

    conn.commit()


def make_meal():
    print("Pass the empty recipe name to exit.")

    while True:
        recipie_name = input("Recipe name: ")
        if not recipie_name:
            break  # Exit out of loop

        recipie_description = input("Recipe description: ")
        recipie = cur.execute(
            "INSERT INTO recipes (recipe_name, recipe_description) VALUES (?, ?)",
            (recipie_name, recipie_description),
        ).lastrowid

        serving_times = cur.execute("SELECT meal_id, meal_name FROM meals").fetchall()
        print(" ".join([f"{time[0]}) {time[1]}" for time in serving_times]))

        serves_at = input("When the dish can be served: ").split()
        for time in serves_at:
            cur.execute(
                "INSERT INTO serve (meal_id, recipe_id) VALUES (?, ?)",
                (time, recipie),
            )

        conn.commit()

        while True:
            input_quantity = None
            input_measurement = None
            input_ingredient = None

            _ = input("Input quantity of ingredient <press enter to stop>: ").split()
            if not _:
                # Exit out of loop
                break
            elif len(_) == 3:
                input_quantity = _[0]
                input_measurement = _[1]
                input_ingredient = _[2]
            elif len(_) == 2:
                input_quantity = _[0]
                input_measurement = "bruh"
                input_ingredient = _[1]

            measurement = cur.execute(
                """
                SELECT measure_id, measure_name
                FROM measures
                WHERE measure_name LIKE ?
            """,
                ("%" + input_measurement + "%",),
            ).fetchall()
            if len(measurement) != 1:
                print("The measure is not conclusive!")
                continue

            ingredient = cur.execute(
                """
                SELECT ingredient_id, ingredient_name
                FROM ingredients
                WHERE ingredient_name LIKE ?
            """,
                ("%" + input_ingredient + "%",),
            ).fetchall()
            if len(ingredient) != 1:
                print("The ingredient is not conclusive!")
                continue

            cur.execute(
                """
                    INSERT INTO quantity (quantity, recipe_id, measure_id, ingredient_id)
                    VALUES (?, ?, ?, ?)
                """,
                (input_quantity, recipie, measurement[0][0], ingredient[0][0]),
            )

            conn.commit()


def get_meals(ingredients, meals):
    ingredients = ingredients.split(",")
    meals = meals.split(",")

    query = f"""
        SELECT recipe_name
        FROM recipes
        WHERE recipe_id IN (
            SELECT recipe_id
            FROM quantity
            WHERE ingredient_id IN (
                SELECT ingredient_id
                FROM ingredients
                WHERE ingredient_name IN ({','.join(['?'] * len(ingredients))})
            )
            GROUP BY recipe_id
            HAVING COUNT(DISTINCT ingredient_id) = {len(ingredients)}
            INTERSECT
            SELECT recipe_id
            FROM serve
            WHERE meal_id IN (
                SELECT meal_id
                FROM meals
                WHERE meal_name IN ({','.join(['?'] * len(meals))})
            )
        )
    """

    recipies = cur.execute(query, [item for item in ingredients + meals]).fetchall()

    if len(recipies) == 0:
        print("There are no such recipes in the database.")
    else:
        print(
            "Recipes selected for you: {}".format(
                " and ".join([item[0] for item in recipies])
            )
        )


if __name__ == "__main__":
    arguments = make_args()

    conn = sqlite3.connect(arguments.database_name)
    cur = conn.cursor()

    # Enable foreign key support
    cur.execute("PRAGMA foreign_keys = ON")

    make_tables(conn)
    if not conn.execute("SELECT * FROM ingredients").fetchall():
        populate_tables()

    if arguments.ingredients and arguments.meals:
        get_meals(arguments.ingredients, arguments.meals)
    else:
        make_meal()

    conn.close()
