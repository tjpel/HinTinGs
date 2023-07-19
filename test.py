from bot import Bot
import pandas as pd
#from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from sentence_transformers import SentenceTransformer, util
import time
import sys


b = Bot("data")
b.load_docs()
b.process_docs()

b.query("Based on the document, what is langchain")
print("Source: ", b.lastSource)
b.query("Where did the fire start?")
print("Source: ", b.lastSource)
b.query("Based on the document, who did Xingyu do on the arduino project?")
print("Source: ", b.lastSource)

# PATH_TO_TESTING_CSV = "testing_suite/testing_results.csv"

# # LIMIT_QUESTIONS limits the amount of questions asked to MAX_QUESTIONS_TO_TEST. If you enable LIMIT_QUESTIONS, your results will not be saved to PATH_TO_TRAINING_CSV.
# LIMIT_QUESTIONS = True
# MAX_QUESTIONS_TO_TEST = 1

# VERBOSE = True

# # bot support system commands
# b = Bot("data")
# if len(sys.argv) > 1:
#     for arg in sys.argv[1:]:
#         b.query(arg)

#     sys.exit()

# test = pd.read_csv(PATH_TO_TESTING_CSV)
# if LIMIT_QUESTIONS:
#     test = test.head(MAX_QUESTIONS_TO_TEST)

# model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
# tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")

# last_input = ""


# for index, row in test.iterrows():
#     time.sleep(
#         15
#     )  # TODO: Stops working after 10 or so prompts without this, seems the problem is Flan

#     if VERBOSE:
#         print(f"Current Index: {index}")

#     # dump old conversation if talking about new document
#     if last_input != row["Input File"]:
#         b.clear_memory()

#     # .iloc mess is because updating row doesn't update test
#     test.iloc[
#         index, test.columns.get_loc("HiNTinGs Answer")
#     ] = hintings_answer = b.query(row["Question"])

#     prompt = f"""
#         Giving just yes or no as an answer, do these two phrases have the same main point? Hint: this document does not
#         answer the question is the same as saying that no context is given

#         Phrase #1: {row['Human Answer']}
#         Phrase #2: {hintings_answer}
#         """

#     if VERBOSE:
#         print(prompt)

#     inputs = tokenizer(prompt, return_tensors="pt")

#     outputs = model.generate(**inputs, max_length=3)
#     res = tokenizer.batch_decode(outputs, skip_special_tokens=True)

#     if VERBOSE:
#         print(res)

#     if "yes" in res[0]:
#         test.iloc[index, test.columns.get_loc("Pass")] = 1
#     else:
#         test.iloc[index, test.columns.get_loc("Pass")] = 0

#     last_input = row["Input File"]

# print(test["Pass"].value_counts())
# print(len(test[test["Pass"] == 1]) / len(test))

# if not LIMIT_QUESTIONS:
#     test.to_csv(PATH_TO_TESTING_CSV)
