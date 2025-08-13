import os
import webbrowser
import platform
import difflib

def get_image_path(card_number):
    """Constructs the path to the image file for a given card number."""
    # Handle both .jpg and .jpeg extensions
    for ext in ["jpg", "jpeg"]:
        path = os.path.join("Rorschach cards", f"card {card_number}.{ext}")
        if os.path.exists(path):
            return path
    # Special case for card 2 which is .jpeg in the user's file listing
    path_jpeg = os.path.join("Rorschach cards", f"card {card_number}.jpeg")
    if os.path.exists(path_jpeg):
        return path_jpeg
    return None


def show_image(path):
    """Opens an image in the default image viewer in a cross-platform way."""
    if not path or not os.path.exists(path):
        print(f"Warning: Image not found at {path}")
        return False
    try:
        if platform.system() == 'Darwin':  # macOS
            os.system(f'open "{path}"')
        elif platform.system() == 'Windows':
            os.startfile(path)
        else:  # Linux
            os.system(f'xdg-open "{path}"')
        return True
    except Exception as e:
        print(f"Error opening image: {e}")
        # Fallback to webbrowser for other cases
        try:
            webbrowser.open(f'file://{os.path.realpath(path)}')
            return True
        except Exception as web_e:
            print(f"Webbrowser fallback failed: {web_e}")
            return False


def clear_screen():
    """Clears the console screen."""
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def get_interpretation(card_number, user_input):
    """Analyzes user input against rules for a given card and returns the most likely interpretation.
    Uses difflib to find close matches for keywords.
    """
    user_input_words = user_input.lower().split()
    rules = rorschach_rules.get(card_number, {})
    scores = {}

    for keywords, interpretation in rules.items():
        score = 0
        all_keyword_words = []
        for kw in keywords:
            all_keyword_words.extend(kw.split())
        
        for user_word in user_input_words:
            if difflib.get_close_matches(user_word, all_keyword_words, n=1, cutoff=0.8):
                score += 1
        
        if score > 0:
            scores[interpretation] = score

    if not scores:
        return "No interpretation available for that response."

    # Return the interpretation with the highest score
    best_interpretation = max(scores, key=scores.get)
    return best_interpretation

rorschach_rules = {
    1: {
        ("bat", "butterfly", "moth", "female figure", "girl figure"):
            "normal/average",
        ("jack-o-lantern", "mask", "animal face"):
            "sense of paranoia",
        ("derogatory", "insulting", "ugly", "fat", "disgusting", "bad body"):
            "you have negative feelings about your own body image",
    },
    2: {
        ("butterfly", "moth"):
            "normal/average",
        ("blood",): "you have difficulty controlling your anger",
        ("two people",): "you may have trouble communicating with others",
        ("animal",): "you may have strong desire to dominate others",
    },
    3: {
        ("two male", "two men"):
            "you probably have heterosexual inclination",
        ("two females", "two women", "androgynous"):
            "you likely have some homosexual tendencies",
    },
    4: {
        ("bear", "gorilla", "man"):
            "you are confident person",
        ("menacing male", "angry man"):
            "you have feelings of inferiority and issues with authority",
        ("menacing female", "angry woman"):
            "you have issues with your mother or other female authority figures",
    },
    5: {
        ("butterfly", "moth"):
            "average/normal",
        ("bat wings", "alligator"):
            "you may have an innate hostility toward others",
        ("moving picture", "moving", "picture is moving"):
            "you may be at risk of schizophrenia",
        ("saw", "scissors", "cutting instrument"):
            "you have a castration complex",
    },
    6: {
        ("animal hide", "animal skin"):
            "you may have a particular inclination toward tactile sensations, possibly even to the point of fetish",
        ("boat", "submarine", "person with pronounced features", "long beard", "big nose"):
            "you are sexually dominant, and possibly takes a very active role in your or your sexual persuits",
        ("rug",):
            "you probably find it necessary to be in a relationship at all times, and likely finds it hard to be alone.",
        ("mushroom", "mushroom cloud"):
            "you might have been high when you looked at the card",
    },
    7: {
        ("difficulty defining", "hard to see", "unclear"):
            "you have difficulty relating to females (especially with regard to you or your mother)",
        ("female figures", "children", "faces"):
            "you probably do not have significant mother issues",
        ("women fighting", "girls fighting", "women gossiping", "girls gossiping", "negatively associated activity"):
            "you have serious relationship issues with women in your life (this sometimes originates from strain in the relationship with your mother)",
        ("thunder clouds", "storm clouds"):
            "you might feel anxiety when dealing with females",
        ("oil lamp",):
            "you may be at risk for schizophrenia",
    },
    8: {
        ("four-legged animal", "four legged animal"):
            "normal/average",
        ("not a four-legged animal", "not four legged"):
            "you find emotions distressing or difficult to handle.",
        ("unsettling", "difficulty recognizing", "hard to recognize"):
            "you have cognitive problems processing complex situation",
    },
    9: {
        ("explosion", "fire", "smoke", "blooming shapes"):
            "You have trouble defining anything at all and most likely have an extreme aversion to unstructured data, random information, or randomness in general. Anything lacking structure tends to throw these types of people off balance.",
        ("cloud on middle line", "cloud in the middle"):
            "you have paranoia",
        ("monster", "fighting"):
            "you may have problems with social interaction",
    },
    10: {
        ("crab", "lobster", "rabbit’s head", "spider"):
            "you are relatively satisfied with your present situation",
        ("caterpillars", "worms", "snakes"):
            "you feel as though you are losing control over your life",
        ("dislike card", "trouble dealing", "faces", "bubbles", "smoking"):
            "you have an oral fixation",
    }
}

card_questions = {
    1: "What might this be?",
    2: "This is the Violence interpersonal communication & Domination test. what you see in this picture?",
    3: "This is the sexual preferences test. What you see in this picture?",
    4: "This is a Authority indication test. What you see in this picture?",
    5: "This is a Hostility Castration complex & Schizophrenia test. What you see in this picture?",
    6: "This is a Subconscious sexual association. What you see in this picture?",
    7: "This is a individual’s feeling about female figures in his or her life test. What you see in this picture?",
    8: "This is a Animal not cat or dog. For legged animal test. What you see in this picture?",
    9: "This is a Social interaction test. what you see in this picture?",
    10: "This is a Oral Fixation test. What you see in this picture?"
}


def run_test(test_responses=None):
    """Main function to run the Rorschach test."""
    clear_screen()
    print("Welcome to the Rorschach Test.")
    print("\n*** DISCLAIMER ***")
    print("This is a simplified version of the Rorschach test for entertainment purposes only.")
    print("It is not a substitute for a real psychological evaluation.")
    print("The interpretations provided are based on common responses and should not be taken as a diagnosis.")
    print("********************\n")
    print("You will be shown a series of 10 inkblot cards.")
    print("For each card, you will be asked a question. Please respond with what you see.")
    print("-" * 30)

    for i in range(1, 11):
        clear_screen()
        print(f"--- Card {i} ---")
        image_path = get_image_path(i)

        if not image_path:
            print(f"Warning: Could not find image file for card {i} (e.g., 'card {i}.jpg' or 'card {i}.jpeg'). Skipping.")
            print("-" * 30)
            continue

        if show_image(image_path):
            question = card_questions.get(i, "What do you see?")
            try:
                if test_responses:
                    response = test_responses.pop(0)
                    print(f"{question}\n> {response}") # Print the response for visibility
                else:
                    response = input(f"{question}\n> ")
                interpretation = get_interpretation(i, response)
                print(f"\nInterpretation: {interpretation}\n")
            except EOFError:
                print("\nTest interrupted. Exiting.")
                break  # Exit the loop
        else:
            print(f"Could not display card {i}. Skipping.")

        print("-" * 30)

    print("The test is complete. Thank you for your participation.")


if __name__ == "__main__":
    run_test()