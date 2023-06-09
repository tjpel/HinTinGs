from langchain.prompts import PromptTemplate

custom_combine_prompt_template = """Given the following extracted parts of a long document and a question, create up to three possible answers to the question using the given content. Separate the answers with ":::".
If the provided content is insufficient to answer the question, respond with "I don't know".
Cite the sources used in the answer with "SOURCES".
ALWAYS return a "SOURCES" part in your answer.
QUESTION: What is Flat Earth Theory?
==========
Content: The tinfoil hat community has concluded that the Earth is flat from scientific measurements of the local concrete.
Source: 15-pl
Content: The Earth is the center of the solar system. As a result, the sun rotates around it to cause day and night. This is more evidence of the Flat Earth Theory
Source: 19-pl
==========
FINAL ANSWER: A theory that the Earth is flat
SOURCES: 15-pl
QUESTION: What are the pros and cons to box pleating?
==========
Content: Box pleating lets you have more control over the paper and design more complex models.
Source: 39-pl
Content: Box pleating makes everything into grids, causing you to have to fold a lot of boring precreases.
Source: 13-pl
Content: Box pleating has a higher learning curve compared to other techniques.
Source: 12-pl 
==========
FINAL ANSWER: Pros: Box pleating lets you have more control over the paper and design more complex models. Cons: Box pleating causes a lot of boring precreases and has a higher learning curve.
SOURCES: 39-pl, 13-pl, 12-pl
QUESTION: Which state/country's law governs the interpretation of the contract?
==========
Content: This Agreement is governed by English law and the parties submit to the exclusive jurisdiction of the English courts in  relation to any dispute (contractual or non-contractual) concerning this Agreement save that either party may apply to any court for an  injunction or other relief to protect its Intellectual Property Rights.
Source: 28-pl
Content: No Waiver. Failure or delay in exercising any right or remedy under this Agreement shall not constitute a waiver of such (or any other)  right or remedy.\n\n11.7 Severability. The invalidity, illegality or unenforceability of any term (or part of a term) of this Agreement shall not affect the continuation  in force of the remainder of the term (if any) and this Agreement.\n\n11.8 No Agency. Except as expressly stated otherwise, nothing in this Agreement shall create an agency, partnership or joint venture of any  kind between the parties.\n\n11.9 No Third-Party Beneficiaries.
Source: 30-pl
Content: (b) if Google believes, in good faith, that the Distributor has violated or caused Google to violate any Anti-Bribery Laws (as  defined in Clause 8.5) or that such a violation is reasonably likely to occur,
Source: 4-pl
=========
FINAL ANSWER: This Agreement is governed by English law. ::: This Agreement is governed by the English government. ::: The English law
SOURCES: 28-pl
QUESTION: What did the president say about Michael Jackson?
=========
Content: Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans.  \n\nLast year COVID-19 kept us apart. This year we are finally together again. \n\nTonight, we meet as Democrats Republicans and Independents. But most importantly as Americans. \n\nWith a duty to one another to the American people to the Constitution. \n\nAnd with an unwavering resolve that freedom will always triumph over tyranny. \n\nSix days ago, Russia’s Vladimir Putin sought to shake the foundations of the free world thinking he could make it bend to his menacing ways. But he badly miscalculated. \n\nHe thought he could roll into Ukraine and the world would roll over. Instead he met a wall of strength he never imagined. \n\nHe met the Ukrainian people. \n\nFrom President Zelenskyy to every Ukrainian, their fearlessness, their courage, their determination, inspires the world. \n\nGroups of citizens blocking tanks with their bodies. Everyone from students to retirees teachers turned soldiers defending their homeland.
Source: 0-pl
Content: And we won’t stop. \n\nWe have lost so much to COVID-19. Time with one another. And worst of all, so much loss of life. \n\nLet’s use this moment to reset. Let’s stop looking at COVID-19 as a partisan dividing line and see it for what it is: A God-awful disease.  \n\nLet’s stop seeing each other as enemies, and start seeing each other for who we really are: Fellow Americans.  \n\nWe can’t change how divided we’ve been. But we can change how we move forward—on COVID-19 and other issues we must face together. \n\nI recently visited the New York City Police Department days after the funerals of Officer Wilbert Mora and his partner, Officer Jason Rivera. \n\nThey were responding to a 9-1-1 call when a man shot and killed them with a stolen gun. \n\nOfficer Mora was 27 years old. \n\nOfficer Rivera was 22. \n\nBoth Dominican Americans who’d grown up on the same streets they later chose to patrol as police officers. \n\nI spoke with their families and told them that we are forever in debt for their sacrifice, and we will carry on their mission to restore the trust and safety every community deserves.
Source: 24-pl
Content: And a proud Ukrainian people, who have known 30 years  of independence, have repeatedly shown that they will not tolerate anyone who tries to take their country backwards.  \n\nTo all Americans, I will be honest with you, as I’ve always promised. A Russian dictator, invading a foreign country, has costs around the world. \n\nAnd I’m taking robust action to make sure the pain of our sanctions  is targeted at Russia’s economy. And I will use every tool at our disposal to protect American businesses and consumers. \n\nTonight, I can announce that the United States has worked with 30 other countries to release 60 Million barrels of oil from reserves around the world.  \n\nAmerica will lead that effort, releasing 30 Million barrels from our own Strategic Petroleum Reserve. And we stand ready to do more if necessary, unified with our allies.  \n\nThese steps will help blunt gas prices here at home. And I know the news about what’s happening can seem alarming. \n\nBut I want you to know that we are going to be okay.
Source: 5-pl
Content: More support for patients and families. \n\nTo get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health. \n\nIt’s based on DARPA—the Defense Department project that led to the Internet, GPS, and so much more.  \n\nARPA-H will have a singular purpose—to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more. \n\nA unity agenda for the nation. \n\nWe can do this. \n\nMy fellow Americans—tonight , we have gathered in a sacred space—the citadel of our democracy. \n\nIn this Capitol, generation after generation, Americans have debated great questions amid great strife, and have done great things. \n\nWe have fought for freedom, expanded liberty, defeated totalitarianism and terror. \n\nAnd built the strongest, freest, and most prosperous nation the world has ever known. \n\nNow is the hour. \n\nOur moment of responsibility. \n\nOur test of resolve and conscience, of history itself. \n\nIt is in this moment that our character is formed. Our purpose is found. Our future is forged. \n\nWell I know this nation.
Source: 34-pl
=========
FINAL ANSWER: I don't know
SOURCES:
QUESTION: {question}
=========
{summaries}
=========
FINAL ANSWER:"""
# custom_combine_prompt_template = """Given the following extracted parts of a long document and a question, create a final answer with references ("SOURCES"). 
# If you don't know the answer, just say that you don't know. Don't try to make up an answer. 
# ALWAYS return a "SOURCES" part in your answer.
# QUESTION: Which state/country's law governs the interpretation of the contract?
# =========
# Content: This Agreement is governed by English law and the parties submit to the exclusive jurisdiction of the English courts in  relation to any dispute (contractual or non-contractual) concerning this Agreement save that either party may apply to any court for an  injunction or other relief to protect its Intellectual Property Rights.
# Source: 28-pl
# Content: No Waiver. Failure or delay in exercising any right or remedy under this Agreement shall not constitute a waiver of such (or any other)  right or remedy.\n\n11.7 Severability. The invalidity, illegality or unenforceability of any term (or part of a term) of this Agreement shall not affect the continuation  in force of the remainder of the term (if any) and this Agreement.\n\n11.8 No Agency. Except as expressly stated otherwise, nothing in this Agreement shall create an agency, partnership or joint venture of any  kind between the parties.\n\n11.9 No Third-Party Beneficiaries.
# Source: 30-pl
# Content: (b) if Google believes, in good faith, that the Distributor has violated or caused Google to violate any Anti-Bribery Laws (as  defined in Clause 8.5) or that such a violation is reasonably likely to occur,
# Source: 4-pl
# =========
# FINAL ANSWER: This Agreement is governed by English law.
# SOURCES: 28-pl
# QUESTION: What did the president say about Michael Jackson?
# =========
# Content: Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans.  \n\nLast year COVID-19 kept us apart. This year we are finally together again. \n\nTonight, we meet as Democrats Republicans and Independents. But most importantly as Americans. \n\nWith a duty to one another to the American people to the Constitution. \n\nAnd with an unwavering resolve that freedom will always triumph over tyranny. \n\nSix days ago, Russia’s Vladimir Putin sought to shake the foundations of the free world thinking he could make it bend to his menacing ways. But he badly miscalculated. \n\nHe thought he could roll into Ukraine and the world would roll over. Instead he met a wall of strength he never imagined. \n\nHe met the Ukrainian people. \n\nFrom President Zelenskyy to every Ukrainian, their fearlessness, their courage, their determination, inspires the world. \n\nGroups of citizens blocking tanks with their bodies. Everyone from students to retirees teachers turned soldiers defending their homeland.
# Source: 0-pl
# Content: And we won’t stop. \n\nWe have lost so much to COVID-19. Time with one another. And worst of all, so much loss of life. \n\nLet’s use this moment to reset. Let’s stop looking at COVID-19 as a partisan dividing line and see it for what it is: A God-awful disease.  \n\nLet’s stop seeing each other as enemies, and start seeing each other for who we really are: Fellow Americans.  \n\nWe can’t change how divided we’ve been. But we can change how we move forward—on COVID-19 and other issues we must face together. \n\nI recently visited the New York City Police Department days after the funerals of Officer Wilbert Mora and his partner, Officer Jason Rivera. \n\nThey were responding to a 9-1-1 call when a man shot and killed them with a stolen gun. \n\nOfficer Mora was 27 years old. \n\nOfficer Rivera was 22. \n\nBoth Dominican Americans who’d grown up on the same streets they later chose to patrol as police officers. \n\nI spoke with their families and told them that we are forever in debt for their sacrifice, and we will carry on their mission to restore the trust and safety every community deserves.
# Source: 24-pl
# Content: And a proud Ukrainian people, who have known 30 years  of independence, have repeatedly shown that they will not tolerate anyone who tries to take their country backwards.  \n\nTo all Americans, I will be honest with you, as I’ve always promised. A Russian dictator, invading a foreign country, has costs around the world. \n\nAnd I’m taking robust action to make sure the pain of our sanctions  is targeted at Russia’s economy. And I will use every tool at our disposal to protect American businesses and consumers. \n\nTonight, I can announce that the United States has worked with 30 other countries to release 60 Million barrels of oil from reserves around the world.  \n\nAmerica will lead that effort, releasing 30 Million barrels from our own Strategic Petroleum Reserve. And we stand ready to do more if necessary, unified with our allies.  \n\nThese steps will help blunt gas prices here at home. And I know the news about what’s happening can seem alarming. \n\nBut I want you to know that we are going to be okay.
# Source: 5-pl
# Content: More support for patients and families. \n\nTo get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health. \n\nIt’s based on DARPA—the Defense Department project that led to the Internet, GPS, and so much more.  \n\nARPA-H will have a singular purpose—to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more. \n\nA unity agenda for the nation. \n\nWe can do this. \n\nMy fellow Americans—tonight , we have gathered in a sacred space—the citadel of our democracy. \n\nIn this Capitol, generation after generation, Americans have debated great questions amid great strife, and have done great things. \n\nWe have fought for freedom, expanded liberty, defeated totalitarianism and terror. \n\nAnd built the strongest, freest, and most prosperous nation the world has ever known. \n\nNow is the hour. \n\nOur moment of responsibility. \n\nOur test of resolve and conscience, of history itself. \n\nIt is in this moment that our character is formed. Our purpose is found. Our future is forged. \n\nWell I know this nation.
# Source: 34-pl
# =========
# FINAL ANSWER: The president did not mention Michael Jackson.
# SOURCES:
# QUESTION: {question}
# =========
# {summaries}
# =========
# FINAL ANSWER:"""

CUSTOM_COMBINE_PROMPT = PromptTemplate(
    template=custom_combine_prompt_template, input_variables=["summaries", "question"]
)


validation_prompt = """
Given a list of statements and the following extracted parts of a long document, respond with one of the statements from the list that is most similar in word choice to the document. 
If none of the statements are similar in word choice to the content, respond with "I don't know".

Statements: Pie contains many calories. ::: Pie is a meal enjoyed by many. ::: Pie contains a lot of carbohydrates.
=========
Content: Pie is a popular meal enjoyed by many during thanksgiving.
Content: Pie is a mathematical constant denotating the ratio of a circle's diameter and circumference.
Content: Pie is made with bread, sugar, and milk.
=========
RELATED: Pie is a meal enjoyed by many.

Statements: Cheesits taste good ::: bob likes broccoli ::: why are LLMs so hard to work with
=========
Content: Cheese is a national delicacy.
Content: We should give all dogs mandatory breaks.
Content: cats are better than dogs and you cannot change my mind.
Content: Slimes are very squishy.
=========
RELATED: I don't know

Statements: bob likes broccoli ::: LLMs are hard to work with ::: Cheese tastes good 
=========
Content: Cheese is a national delicacy.
Content: We should give all dogs mandatory breaks.
Content: cats are better than dogs and you cannot change my mind.
Content: Slimes are very squishy.
=========
RELATED: I don't know

Statements: Cheesits taste good
=========
Content: Cheeseits taste very good.
=========
RELATED: Cheesits taste good

Statements: Michondria are the powerhouse of the cell ::: The singular of mitochondria is mitochondrion ::: Mitochondria are organelles of cells
=========
Content: Mitochondria is an organelle found in large numbers in most cells, in which the biochemical processes of respiration and energy production occur. It has a double membrane, the inner layer being folded inward to form layers (cristae).
Content: Mitochondria are membrane-bound cell organelles (mitochondrion, singular) that generate most of the chemical energy needed to power the cell's biochemical reactions. Chemical energy produced by the mitochondria is stored in a small molecule called adenosine triphosphate (ATP). Mitochondria contain their own small chromosomes.
Content: mitochondrion, membrane-bound organelle found in the cytoplasm of almost all eukaryotic cells (cells with clearly defined nuclei), the primary function of which is to generate large quantities of energy in the form of adenosine triphosphate (ATP).
=========
RELATED: Mitochondria are organelles of cells

Statements: {statements}
=========
{contents}
=========
RELATED:"""