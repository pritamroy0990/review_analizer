# from langchain_ollama import ChatOllama
# from typing import Literal
# from pydantic import BaseModel, Field

# model = ChatOllama(model='llama3.1:8b')

# # schema
# class Review(BaseModel):
#     key_themes: list[str] = Field(
#         description="All key themes discussed in the review, extracted as short keywords"
#     )
#     summary: str = Field(
#         description="A one-sentence summary of the review"
#     )
#     sentiment: Literal["pos", "neg"] = Field(
#         description="Sentiment of the review: 'pos' for positive, 'neg' for negative"
#     )
#     reply: str = Field(
#         description="A polite reply as the restaurant owner, addressing the customer's comment"
#     )

# structured_model = model.with_structured_output(Review)

# # Add system-style instruction
# review_text = '''Their food was pretty good.
# But in the scale of 1-10 i would give them 4 on their service.
# They took almost 1 hour to prepare food.'''

# rating='''5 stars'''
# prompt = f"""
# You are an assistant that analyzes restaurant reviews.

# Task:
# 1. Extract key themes as a list of short keywords.
# 2. Summarize the review in one sentence.
# 3. Decide sentiment: 'pos' for positive, 'neg' for negative.
# 4. Write a professional reply as if you are the restaurant owner.

# Review: "{review_text}"
# """

# result = structured_model.invoke(prompt)
# print(result)


# --------------------------------------------------------------


# from langchain_ollama import ChatOllama
# from typing import Literal
# from pydantic import BaseModel, Field

# # Choose an instruction-following model
# model = ChatOllama(model='llama3.1:8b')

# # schema
# class Review(BaseModel):
    
#     key_themes: list[str] = Field(
#         description="All key themes discussed in the review, extracted as short keywords and phrase"
#     )
#     summary: str = Field(
#         description="A one-sentence summary of the review"
#     )
#     sentiment: Literal["pos", "neg"] = Field(
#         description="Sentiment of the review: 'pos' for positive, 'neg' for negative"
#     )
#     reply: str = Field(
#         description="A polite reply as the restaurant owner, addressing the customer's comment"
#     )
#     actionable_recommendation: str = Field(
#         description="write a short actionable recommendation"
#     )
#     customer_emotions: dict = Field(
#         description="Distribution of emotions with percentage values (e.g., {'angry': 12, 'happy': 70, 'frustrated': 8, 'neutral': 10})."
#     )

# structured_model = model.with_structured_output(Review)

# # Example review
# review_text = '''Services and food's taste were so good. But 14th may when we visit last time, we ordered   "classic chicken burger" and "mexican chow mein" (it was a offer combo) suddenly I saw a leg of a butterfly or grasshopper! It was so much disgusting filling. After complaint they changed it so quickly by cooking another dish and was apologize. They said that they cooked each time of order so that they don’t have any stock of that dish. Quality of that food was good enough.'''
# reviewer_name = "John Doe"  # you can pass dynamically
# customer_rating = 3 # Provided by customer


# prompt = f"""
# You are an assistant that analyzes restaurant reviews.

# Task:
# 1. Extract key themes as short keywords and phreases.
# 2. Summarize the review in one sentence.
# 3. Decide sentiment: 'pos' for positive, 'neg' for negative.
# 4. Include the reviewer name if available, otherwise don't do anything.
# 5. Write a professional reply as if you are the restaurant owner.
# 6.write a short actionable recommendation
# 7.Analyze customer emotions beyond sentiment (happy, sad, angry, frustrated, neutral).Return percentages that sum to 100.

# Review text: "{review_text}"
# Reviewer name: "{reviewer_name}"
# Customer rating: {customer_rating}
# """

# result = structured_model.invoke(prompt)
# print(result)



# ----------------------------------------------------------------------------------------


# from langchain_ollama import ChatOllama
# from typing import Literal,Optional,Dict
# from pydantic import BaseModel, Field


# # Choose an instruction-following model
# model = ChatOllama(model='llama3.1:8b')

# # schema
# class Review(BaseModel):
    
#     key_themes: list[str] = Field(
#         description="All key themes discussed in the review, extracted as short keywords and phrase"
#     )
#     summary: str = Field(
#         description="A one-sentence summary of the review"
#     )
#     sentiment: Literal["pos", "neg"] = Field(
#         description="Sentiment of the review: 'pos' for positive, 'neg' for negative"
#     )
#     reply: str = Field(
#         description="A polite reply as the restaurant owner, addressing the customer's comment, customer rating and aspect rating that rating out of 5"
#     )
#     actionable_recommendation: str = Field(
#         description="write a short actionable recommendation"
#     )
#     customer_emotions: dict = Field(
#         description="Distribution of emotions with percentage values (e.g., {'angry': 12, 'happy': 70, 'frustrated': 8, 'neutral': 10})."
#     )


# structured_model = model.with_structured_output(Review)

# # Example review
# review_text = ''''''
# reviewer_name = "John Doe"  # you can pass dynamically
# customer_rating = 2 # Provided by customer
# aspect_rating='''
# {'Food': 1, 'Service': 1, 'Atmosphere': 1}
# '''


# prompt = f"""
# You are an assistant that analyzes restaurant reviews.

# Task:
# 1. Extract key themes as short keywords and phreases.
# 2. Summarize the review in one sentence  beased on review text, customer rating and aspect rating as if you are the restaurant owner.aspect rating is out of 5"
# 3. Decide sentiment: 'pos' for positive, 'neg' for negative.
# 4. Include the reviewer name if available, otherwise don't do anything.
# 5. Write a professional reply beased on review text, customer rating and aspect rating as if you are the restaurant owner.aspect rating is out of 5"
# 6.write a short actionable recommendation
# 7.Analyze customer emotions beyond sentiment (happy, sad, angry, frustrated, neutral).Return percentages that sum to 100.


# Review text: "{review_text}"
# Reviewer name: "{reviewer_name}"
# Customer rating: {customer_rating}
# aspect rating: {aspect_rating}
# """

# result = structured_model.invoke(prompt)
# print(result)
# ----------------------------------------------------------------------


from langchain_ollama import ChatOllama
from typing import Literal,Optional,Dict
from pydantic import BaseModel, Field



# Choose an instruction-following model
model = ChatOllama(model='llama3.1:8b')

class Emotions(BaseModel):
    happy:int
    sad:int
    angry:int
    frustrated:int
    neutral:int

# schema
class Review(BaseModel):
    
    key_themes: list[str] = Field(
        description="All key themes discussed in the review, extracted as short keywords and phrase"
    )
    summary: str = Field(
        description="A one-sentence summary of the review"
    )
    sentiment: Literal["pos", "neg"] = Field(
        description="Sentiment of the review: 'pos' for positive, 'neg' for negative"
    )
    reply: str = Field(
        description="A polite reply as the restaurant owner, addressing the customer's comment, customer rating and aspect rating that rating out of 5"
    )
    actionable_recommendation: str = Field(
        description="write a short actionable recommendation"
    )
    customer_emotions: Emotions = Field(
        description="Distribution of emotions with percentage values (e.g., {'angry': 12, 'happy': 70, 'frustrated': 8, 'sad': 5, 'neutral': 5})."
    )


structured_model = model.with_structured_output(Review)

def sentiment(review_text,reviewer_name,customer_rating,aspect_rating):
# Example review
# review_text = review_text
# reviewer_name = reviewer_name  # you can pass dynamically
# customer_rating = 2 # Provided by customer
# aspect_rating='''
# {'Food': 1, 'Service': 1, 'Atmosphere': 1}
# '''


    prompt = f"""
    You are an assistant that analyzes restaurant reviews.

    Task:
    1. Extract key themes as short keywords and phreases.
    2. Summarize the review in one sentence  beased on review text, customer rating and aspect rating as if you are the restaurant owner.aspect rating is out of 5"
    3. Decide sentiment: 'pos' for positive, 'neg' for negative.
    4. Include the reviewer name if available, otherwise don't do anything.
    5. Write a professional reply beased on review text, customer rating and aspect rating as if you are the restaurant owner.aspect rating is out of 5"
    6.write a short actionable recommendation
    7.Analyze customer emotions beyond sentiment (happy, sad, angry, frustrated, neutral).Return percentages that sum to 100.


    Review text: "{review_text}"
    Reviewer name: "{reviewer_name}"
    Customer rating: {customer_rating}
    aspect rating: {aspect_rating}
    """

    result = structured_model.invoke(prompt)
    result.customer_emotions=dict(result.customer_emotions)
    return result
