# imports
import requests
import pandas as pd


# data fetch function
def fetch_hdx_data(dataset_name: str, keyword: str = None) -> dict:
    url = f"https://data.humdata.org/api/3/action/package_show?id={dataset_name}"
    try:
        raw_data = requests.get(url=url, timeout=10)
        raw_data.raise_for_status()
        data_json = raw_data.json()
    except requests.RequestException as req_err:
        return {"error": str(req_err)}
    except ValueError as verror:
        return {"error": str(verror)}
        
    resources = data_json['result']['resources']
    if not resources:
        return {"error": "No resources found in this dataset"}
    
    if keyword:
        filtered = [r for r in resources if keyword.lower() in r['name'].lower()]
        if not filtered:
            return {"error": f"No resources matching '{keyword}' found"}
    else:
        filtered = resources
            
    latest  = max(filtered, key=lambda r: r['last_modified'])
    return{
        "download_url": latest["download_url"],
        "last_modified": latest["last_modified"],
        "format": latest['format']
    }
    
    
    
def load_hdx_csv(download_url: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(download_url)
    except Exception as e:
        return {"error": str(e)}
    return df

