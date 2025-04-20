import genanki
import random

def generate_anki_deck(flashcards: list, topic: str = 'generated_flashcards'):
    deck_id = random.randint(1 << 30, 1 << 31)
    model_id = random.randint(1 << 30, 1 << 31)

    deck = genanki.Deck(
        deck_id,
        topic
    )

    model = genanki.Model(
        model_id,
        topic,
        fields=[
            {'name': 'Front'},
            {'name': 'Back'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Front}}',
                'afmt': '{{Front}}<hr id="answer">{{Back}}',
            },
        ]
    )

    # Add flashcards
    for card in flashcards:
        front = card.get("front", "").strip()
        back = card.get("back", "").strip()
        if front and back:
            note = genanki.Note(model=model, fields=[front, back])
            deck.add_note(note)

    # Write to .apkg
    genanki.Package(deck).write_to_file(f"./anki-decks/{topic}.apkg")
    print(f"Anki deck saved as: {topic}.apkg")

# # TESTING
# cards = [{'front': 'α-approximation Algorithm', 'back': 'A polynomial-time algorithm that returns a solution within a factor α of the optimal solution.'}, {'front': 'Vertex Cover Problem', 'back': 'A minimization problem where we want to find a subset of vertices in a graph that covers all edges.'}, {'front': 'Load Balancing Problem', 'back': 'A problem of scheduling jobs on machines to minimize the maximum load.'}, {'front': 'Approximation Ratio', 'back': 'The smallest α such that the algorithm is an α-approximation algorithm.'}, {'front': 'Matching in a Graph', 'back': 'A subset of edges with no shared endpoints.'}]

# generate_anki_deck(cards, 'algs')