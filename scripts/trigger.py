import requests
import json

def hello_world(request):
    data = request.json
    
    if 'queryResult' in data and 'intent' in data['queryResult']:
        if data['queryResult']['intent']['displayName'] == 'yelp':
            execute_crawler()
        if data['queryResult']['intent']['displayName'] == 'deploy':
            execute_deployer()
        if data['queryResult']['intent']['displayName'] == 'delete':
            execute_deleter()
        if data['queryResult']['intent']['displayName'] == 'query':
            return execute_query()
        if data['queryResult']['intent']['displayName'] == 'search':
            return execute_search()
    return f'Success!'
    
def execute_search():
    try:
        requests.get("https://us-central1-big-data-architecture-ricardo.cloudfunctions.net/search", timeout=0.1)
    except requests.exceptions.ReadTimeout:
        pass

def execute_query():
    try:
        requests.get("https://us-central1-big-data-architecture-ricardo.cloudfunctions.net/query", timeout=0.1)
    except requests.exceptions.ReadTimeout:
        pass

def execute_crawler():
    try:
        requests.get("https://us-central1-big-data-architecture-ricardo.cloudfunctions.net/function-1", timeout=0.1)
    except requests.exceptions.ReadTimeout:
        pass

def execute_deployer():
    try:
        requests.get("https://us-central1-big-data-architecture-ricardo.cloudfunctions.net/deploy_cluster", timeout=0.1)
    except requests.exceptions.ReadTimeout:
        pass

def execute_deleter():
    try:
        requests.get("https://us-central1-big-data-architecture-ricardo.cloudfunctions.net/delete_cluster", timeout=0.1)
    except requests.exceptions.ReadTimeout:
        pass
