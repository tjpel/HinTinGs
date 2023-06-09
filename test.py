from bot import Bot

# this file tests the Q&A bot

# b = Bot("data/example1.txt")
# b.query("What is Langchain?")
# b.query("Is Langchain a framework or library?")
# b.query("What is Langchain named after?")


# b = Bot("data/example2.txt")
# b.query("What is happening in New York?")
# b.query("Where did the fire start?")
# b.query("What is the best ice cream flavor?")

# b = Bot("data/syllabus.pdf")
# b.query("What is the  class about?")
# b.query("Who is the policy for cheating?")
# b.query("What are the prerequisites for the course?")
# b.query("Can I take this course online?")

b = Bot("data/project.docx")
b.query("What tools are used in this project?")
b.query("What are the results?")
b.query("How was the work divided and who did which part?")
b.query("Show the code used in this project?")
