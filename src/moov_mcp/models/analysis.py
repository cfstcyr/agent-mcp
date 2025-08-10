from openai import BaseModel
from pydantic import Field


class SentimentAnalysisResult(BaseModel):
    """
    Represents the result of a sentiment analysis.
    """

    sentiment: float = Field(
        ...,
        description="The sentiment of the text. A value between -1 and 1, where -1 indicates negative sentiment, 0 indicates neutral sentiment, and 1 indicates positive sentiment.",
    )
    confidence: float = Field(
        ...,
        description="The confidence score of the sentiment analysis. A float between 0 and 1, indicating the model's confidence in the sentiment score.",
    )
