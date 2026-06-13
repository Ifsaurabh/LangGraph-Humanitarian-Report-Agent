# imports
from typing import TypedDict, Annotated, Optional
import operator


# State definition
class AgentState(TypedDict):
    question: str                          # user's input question
    food_price_result: Optional[dict]      # small filtered/aggregated result
    poverty_result: Optional[dict]         # small filtered/aggregated result
    analysis: str                          # LLM's reasoning over gathered data
    final_report: str                      # generated report text
    messages: Annotated[list, operator.add]  # tool-calling conversation history
    # here optional[dict] because LLm might not need tom call both -depending upon question
    
