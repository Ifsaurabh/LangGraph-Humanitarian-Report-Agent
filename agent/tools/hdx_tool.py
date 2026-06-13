import requests

def fetch_hdx_data(dataset_name: str) -> dict:
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
    latest  = max(resources, key=lambda r: r['last_modified'])
    return{
        "download_url": latest["download_url"],
        "last_modified": latest["last_modified"],
        "format": latest['format']
    }
    