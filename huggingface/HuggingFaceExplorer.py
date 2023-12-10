import requests
import pandas as pd
from huggingface_hub import HfApi

def get_top_models_from_leaderboard():
    leaderboard_url = 'https://huggingface.co/api/models?sort=downloads&direction=-1'
    try:
        response = requests.get(leaderboard_url)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

def sort_filter_models(models_df, sort_key=None, filter_key=None, filter_value=None):
    if filter_key and filter_value:
        if filter_key in models_df.columns:
            models_df = models_df[models_df[filter_key] == filter_value]
        else:
            print(f"Warning: Filter key '{filter_key}' not found in DataFrame. Skipping filter.")
    if sort_key and sort_key in models_df.columns:
        models_df = models_df.sort_values(by=sort_key, ascending=False)
    else:
        print(f"Warning: Sort key '{sort_key}' not found in DataFrame. Skipping sort.")
    return models_df

def download_model(model_name):
    try:
        api = HfApi()
        model_info = api.model_info(model_name)
        model_url = model_info.siblings[0].rfilename
        response = requests.get(model_url)
        response.raise_for_status()
        with open(f"{model_name}.bin", 'wb') as f:
            f.write(response.content)
        print(f"Model {model_name} downloaded successfully.")
    except requests.exceptions.HTTPError as err:
        print(f"Error downloading model {model_name}: {err}")
    except Exception as e:
        print(f"Unexpected error downloading model {model_name}: {e}")

def search_models(query):
    api = HfApi()
    try:
        models_generator = api.list_models(filter=query)
        models = [model for model in models_generator]
        return pd.DataFrame(models)
    except Exception as e:
        print(f"Error searching for models: {e}")

# Example Usage
try:
    # Get top models from the leaderboard
    top_models_df = get_top_models_from_leaderboard()
    print("Top Models from Leaderboard:")
    print(top_models_df.head())  # Display top 5 models for brevity

    # Sort and filter (example: filter by task and sort by downloads)
    filtered_models_df = sort_filter_models(top_models_df, sort_key='downloads', filter_key='task', filter_value='text-generation')
    print("\nSorted and Filtered Models:")
    print(filtered_models_df.head())  # Display top 5 models for brevity

    # Download a model (example: downloading the first model from the filtered list)
    if not filtered_models_df.empty:
        model_id = filtered_models_df.iloc[0]['modelId']
        download_model(model_id)

    # Search for models (example: searching for "gpt" models)
    gpt_search_results = search_models("gpt")
    print("\nSearch Results for 'gpt':")
    print(gpt_search_results.head())  # Display top 5 models for brevity

except Exception as e:
    print(f"An error occurred: {e}")