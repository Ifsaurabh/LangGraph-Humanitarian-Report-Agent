# main graph

# imports and setup ------------------------------------------------
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
import operator
from anthropic import Anthropic
from dotenv import load_dotenv
from agent.state import AgentState
from agent.tools.tool_definitions import TOOLS
from agent.tools.hdx_tool import fetch_hdx_data, load_hdx_csv
from agent.tools.query_tool import query_data
from datetime import datetime
import os
import boto3


load_dotenv()
anthropic_client = Anthropic()
graph = StateGraph(AgentState)


# Creating nodes ------------------------------------------

# data gathering node
def data_gathering_node(state: AgentState) -> dict:
    question = state['question']
    food_price_result = None
    poverty_result = None
    food_price_df=None
    poverty_df=None
    
    # First API call
    messages = [{"role": "user", "content": question}]
    response = anthropic_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system="You are a humanitarian data analyst, use tools to gather information and data before answering.",
        tools=TOOLS,
        messages=messages
        )
    
    # ReAct Loop
    while response.stop_reason == "tool_use":
        messages.append({"role": "assistant", "content": response.content})
    
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                if block.name == "get_food_price_data":
                    result = fetch_hdx_data("hdx-hapi-ind", "food prices")
                    food_price_result = result
                    food_price_df = load_hdx_csv(result["download_url"])
                elif block.name == 'get_poverty_data':
                    result = fetch_hdx_data("hdx-hapi-ind", "poverty rate")
                    poverty_result = result
                    poverty_df = load_hdx_csv(result["download_url"])
                elif block.name == 'query_data':
                    cached_dfs = {"food_price": food_price_df, "poverty": poverty_df}
                    result = query_data(cached_dfs, **block.input)
                    
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content" : str(result)
                    })
            
            # appending result, then calling API again
        messages.append({"role": "user", "content": tool_results})
        response = anthropic_client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system="You are a humanitarian data analyst, use tools to gather information and data before answering.",
            tools=TOOLS,
            messages=messages
            )
    
    return {
        "messages": messages,
        "food_price_result": food_price_result,
        "poverty_result": poverty_result
    }        
      
      
# analysis node
# analysis node
def analysis_node(state: AgentState) -> dict:
    question = state['question']
    messages = state['messages']
    
    # Adding analysis instruction to exixsting conversation
    messages.append({"role":"user", "content":"Based on the data you gathered above, analyze the key patterns and relationships. Use the actual numbers from the data."})
    response = anthropic_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        system="You are a humanitarian data analyst. Analyze the data already gathered and identify risk patterns. Use exact numbers from the data. Do not make up statistics.",
        messages= messages
)
    return {"analysis": response.content[0].text}



# report generation node
def generate_report_node(state: AgentState) -> dict:
    question = state['question']
    analysis = state['analysis']
    context = f"Question: {question}\n\nAnalysis: {analysis}"
    response = anthropic_client.messages.create(
        model='claude-haiku-4-5-20251001',
        max_tokens=4096,
        system=(
            "You are a humanitarian data analyst. Generate a structured "
            "markdown report with sections: Executive Summary, Key Findings, "
            "Risk Assessment, and Recommendations. "
            "If the analysis indicates that a data source failed, errored, "
            "or could not be retrieved, explicitly state this as a limitation "
            "in the report (e.g. under Key Findings or as a noted gap). "
            "Do not fabricate, estimate, or guess values for missing or failed data."
        ),
        messages=[{"role":"user", "content": context}]
    )
    return {"final_report": response.content[0].text}


# save/store report node -
def save_report_node(state: AgentState) -> dict:
    boto_client = boto3.client(
    's3',
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name= "ap-south-1")
    
    question =  state['question']
    final_report = state['final_report']
    question_slug = question[:30].replace(" ", "_").replace("?", "")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{timestamp}_{question_slug}.md"
    
    output_dir = "lang_food_poverty_output"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w") as f:
        f.write(final_report)
        
    boto_client.upload_file(
        Filename= filepath,
        Bucket= "my-test-bucket9966",
        Key= f"reports/{filename}"
    )

    return {"final_report": final_report}



# merging nodes into graph --------------------------------------------------

# adding nodes to the graph
graph.add_node("gather_data", data_gathering_node)
graph.add_node("analyze", analysis_node)
graph.add_node("generate_report", generate_report_node)
graph.add_node("save_report", save_report_node)

# setting entry point
graph.set_entry_point("gather_data")


# adding edges to the graph
graph.add_edge("gather_data", "analyze")
graph.add_edge("analyze", "generate_report")
graph.add_edge("generate_report", "save_report")
graph.add_edge("save_report", END)

# complile into app
app = graph.compile()
