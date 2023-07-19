from bot import Bot
import pandas as pd

# from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from sentence_transformers import SentenceTransformer, util
import time
import sys


PATH_TO_TESTING_CSV = "testing_suite/testing_results.csv"

# LIMIT_QUESTIONS limits the amount of questions asked to MAX_QUESTIONS_TO_TEST. If you enable LIMIT_QUESTIONS, your results will not be saved to PATH_TO_TRAINING_CSV.
LIMIT_QUESTIONS = True
MAX_QUESTIONS_TO_TEST = 3

VERBOSE = True

SIMULARITY_THRESHOLD = 0.75


b = Bot("data")
b.load_docs()
b.process_docs()

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        b.query(arg)

    sys.exit()

test = pd.read_csv(PATH_TO_TESTING_CSV)
if LIMIT_QUESTIONS:
    test = test.head(MAX_QUESTIONS_TO_TEST)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

last_input = ""


for index, row in test.iterrows():
    time.sleep(
        15
    )  # TODO: Stops working after 10 or so prompts without this, seems the problem is Flan

    if VERBOSE:
        print(f"Current Index: {index}")

    # # dump old conversation if talking about new document
    # if last_input != row["Input File"]:
    #     b.clear_memory()

    # .iloc mess is because updating row doesn't update test
    test.iloc[
        index, test.columns.get_loc("HiNTinGs Answer")
    ] = hintings_answer = b.query(row["Question"])

    embedding_human = model.encode(row["Human Answer"], convert_to_tensor=True)
    embedding_bot = model.encode(hintings_answer, convert_to_tensor=True)

    simularity = util.pytorch_cos_sim(embedding_bot, embedding_human)

    if VERBOSE:
        print(f"Simularity (0-1): {simularity}")

    if simularity > SIMULARITY_THRESHOLD:
        test.iloc[index, test.columns.get_loc("Pass")] = 1
    else:
        test.iloc[index, test.columns.get_loc("Pass")] = 0

    last_input = row["Input File"]

print(test["Pass"].value_counts())
print(len(test[test["Pass"] == 1]) / len(test))

if not LIMIT_QUESTIONS:
    test.to_csv(PATH_TO_TESTING_CSV)
