# json schema for food prices
get_food_price_data = {
    "name": "get_food_price_data",
    "description": "Get food prices dataset",
    "input_schema": {"type": "object", "properties":{}, "required": []}
}


# json schema for poverty data
get_poverty_data = {
    "name": "get_poverty_data",
    "description": "Get the Poverty dataset",
    "input_schema": {"type": "object", "properties": {}, "required":[]}
}


# json scehma for 7 parameters in query data
query_data = {
    "name": "query_data",
    "description": "filters/aggregates data from cached datasets",
    "input_schema": {"type": "object", "properties": {
        "dataset": {"type": "string",
                    "description": "Dataset to query. Must be 'food_price' or 'poverty'"},
        "state": {"type": "string",
                  "description": "Name of the Indian state to filter by, e.g. 'Bihar', 'Andhra Pradesh'"},
        "commodity": {"type": "string",
                    "description": "Food commodity to filter by e.g. 'Rice', 'Wheat'. Only applies to food_price dataset"},
        "aggregation": {"type": "string",
                    "description": "Must be 'latest', 'average', or 'trend'"},
        "column": {"type": "string",
                    "description": "Column to aggregate. For poverty: 'mpi', 'headcount_ratio', 'intensity_of_deprivation'. For food_price: 'price'"},
        "date_from": {"type": "string",
                    "description": "Start date for date range filter. ISO format: YYYY-MM-DD"},
        "date_to": {"type": "string",
                    "description": "End date for date range filter. ISO format: YYYY-MM-DD"},
        }, "required": ['dataset', 'aggregation']}
}

TOOLS = [get_food_price_data, get_poverty_data, query_data]