from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Cards, create_db


class Flashcards:
    def __init__(self):
        self.engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
        self.session = sessionmaker(bind=self.engine)
        self.session = self.session()

        create_db(self.engine)

        self.show_menu()

    def show_menu(self):
        print("\n1. Add flashcards")
        print("2. Practice flashcards")
        print("3. Exit")

        _ = input()

        if _ == "1":
            self.add_flashcards()
        elif _ == "2":
            self.practice_flashcards()
        elif _ == "3":
            print("\nBye!")
            exit()
        else:
            print(f"\n{_} is not an option")
            self.show_menu()

    def add_flashcards(self):
        print("\n1. Add a new flashcard")
        print("2. Exit")

        _ = input()

        if _ == "1":
            question = ""
            answer = ""

            while not question:
                print("Question:")
                question = input().strip()

            while not answer:
                print("Answer:")
                answer = input().strip()

            new_card = Cards(question=question, answer=answer)

            self.session.add(new_card)
            self.session.commit()
            self.add_flashcards()
        elif _ == "2":
            self.show_menu()
        else:
            print(f"\n{_} is not an option")
            self.add_flashcards()

    def practice_flashcards(self):
        cards = self.session.query(Cards).all()

        if len(cards) == 0:
            print("\nThere is no flashcard to practice!")
            self.show_menu()

        for card in cards:
            print(f"\nQuestion: {card.question}")
            print('press "y" to see the answer:')
            print('press "n" to skip:')
            print('press "u" to update:')

            _ = input()

            if _ == "y":
                self.see_answer(card.id)
            elif _ == "n":
                continue
            elif _ == "u":
                self.modify_card(card.id)
            else:
                print(f"\n{_} is not an option")
                self.practice_flashcards()

        self.show_menu()

    def see_answer(self, card_id):
        card = self.session.query(Cards).filter(Cards.id == card_id).first()
        answer = ""

        print(f"\nAnswer: {card.answer}")

        while answer not in ("y", "n"):
            print('press "y" if your answer is correct:')
            print('press "n" if your answer is wrong:')
            answer = input().strip()

            if answer == "y":
                if card.box < 3:
                    card.box += 1
                else:
                    self.session.delete(card)
            elif answer == "n":
                card.box = 1
            else:
                print(f"{answer} is not an option\n")

        self.session.commit()

    def modify_card(self, card_id):
        card = self.session.query(Cards).filter(Cards.id == card_id).first()

        print('press "d" to delete the flashcard:')
        print('press "e" to edit the flashcard:')

        _ = input()

        if _ == "d":
            self.session.delete(card)
        elif _ == "e":
            question = ""
            answer = ""

            while not question:
                print(f"\ncurrent question: {card.question}")
                print('please write a new question:')
                question = input().strip()

            while not answer:
                print(f"\ncurrent answer: {card.answer}")
                print('please write a new answer:')
                answer = input().strip()

            card.question = question
            card.answer = answer
        else:
            print(f"{_} is not an option")
            self.modify_card(card_id)

        self.session.commit()


if __name__ == '__main__':
    flashcards = Flashcards()
