from langchain_core.prompts import PromptTemplate
from langchain_ollama.chat_models import ChatOllama
from utils.statistic import all_review_list
import pandas as pd
from pydantic import BaseModel, RootModel
from typing import Dict

# Schema for individual dish sentiment
class DishSentiment(BaseModel):
    positive: int
    negative: int

# Root model for dish → sentiment mapping
class DishInsights(RootModel[Dict[str, DishSentiment]]):
    pass


# Initialize model once
model = ChatOllama(model="llama3.1:8b")
structured_model = model.with_structured_output(DishInsights)


def top_streangth(html_file):
    all_reviews_list=all_review_list(html_file)
    
    template = PromptTemplate(
    template="""
        You are an assistant analyzing restaurant reviews.

        Task:
        1. Identify the restaurant's strengths based on the reviews.
        2. Return the answer strictly in the requested format without explanations, disclaimers, or additional commentary.


        From the reviews, extract:
        - strengths (what customers like most).
        - Common positive themes (food, service, atmosphere, etc.).

        Reviews:
        {review_list}

        """,
            input_variables=["review_list"]
        )


    # fill the values of the placeholders
    prompt = template.invoke({'review_list':all_reviews_list})

    result = model.invoke(prompt)

    return str(result.content)

def top_weakness(html_file):
    all_reviews_list=all_review_list(html_file)
    
    template = PromptTemplate(
    template="""
        You are an assistant analyzing restaurant reviews.

        Task:
        1. Identify the restaurant's weaknesses based on the reviews.
        2. Return the answer strictly in the requested format without explanations, disclaimers, or additional commentary.


        From the reviews, extract:
        - Weaknesses (what customers complain about most).
        - Common negative themes (food, service, atmosphere, price, etc.).

        Reviews:
        {review_list}

        """,
            input_variables=["review_list"]
        )


    # fill the values of the placeholders
    prompt = template.invoke({'review_list':all_reviews_list})

    result = model.invoke(prompt)

    return str(result.content)

def top_compliment(html_file):
    all_reviews_list=all_review_list(html_file)
    
    template = PromptTemplate(
    template="""
        You are an assistant analyzing restaurant reviews.

        Task:
        1. Identify the top compliments customers gave in the reviews.
        2. Return the answer strictly in the requested format without explanations, disclaimers, or extra commentary.

        From the reviews, extract:
        - Direct compliments (praise for food, staff, atmosphere, service, etc.).
        - Highlight the most frequently mentioned compliments.

        Reviews:
        {review_list}

        Return output only as:

        Compliments:
        - ...
        - ...
        - ...
        """,
            input_variables=["review_list"]
        )
     # fill the values of the placeholders
    prompt = template.invoke({'review_list':all_reviews_list})

    result = model.invoke(prompt)

    return str(result.content)


def top_complaint(html_file):
    all_reviews_list = all_review_list(html_file)
    
    template = PromptTemplate(
        template="""
        You are an assistant analyzing restaurant reviews.

        Task:
        1. Identify the top complaints customers made in the reviews.
        2. Return the answer strictly in the requested format without explanations, disclaimers, or extra commentary.

        From the reviews, extract:
        - Direct complaints (about food, service, staff, atmosphere, price, etc.).
        - Highlight the most frequently mentioned complaints.

        Reviews:
        {review_list}

        Return output only as:

        Complaints:
        - ...
        - ...
        - ...
        """,
        input_variables=["review_list"]
    )
    
    # fill the values of the placeholders
    prompt = template.invoke({'review_list': all_reviews_list})

    result = model.invoke(prompt)

    return str(result.content)

def actionable_recommendation(html_file):
    all_reviews_list = all_review_list(html_file)
    
    template = PromptTemplate(
        template="""
        You are an assistant analyzing restaurant reviews.

        Task:
        1. Provide actionable recommendations for the restaurant owner based on the reviews.
        2. Focus on practical steps they can take to improve or maintain their service.
        3. Return the answer strictly in the requested format without explanations, disclaimers, or extra commentary.

        From the reviews, extract:
        - What customers appreciate (keep doing this).
        - What customers complain about (improve this).
        - Convert these into clear, actionable recommendations.

        Reviews:
        {review_list}

        Return output only as:

        Recommendations:
        - ...
        - ...
        - ...
        """,
        input_variables=["review_list"]
    )
    
    # fill the values of the placeholders
    prompt = template.invoke({'review_list': all_reviews_list})

    result = model.invoke(prompt)

    return str(result.content)


def manu_item_insight(html_file: str) -> dict:
    reviews = all_review_list(html_file)

    template = PromptTemplate(
        template="""
        You are an assistant analyzing restaurant reviews.

        Task:
        1. Identify which dishes get the most positive/negative mentions.
        2. Return strictly in JSON format without explanations.

        Reviews:
        {reviews}

        Return format:
        {{
            "chicken biryani": {{"positive": 12, "negative": 6}},
            "pizza": {{"positive": 22, "negative": 4}}
        }}
        """,
        input_variables=["reviews"]
    )

    prompt = template.format(reviews=reviews)
    result = structured_model.invoke(prompt)

    return result.model_dump()


