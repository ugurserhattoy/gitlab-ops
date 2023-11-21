import requests
import json

class TerraOps:
    def __init__(self, private_token) -> None:
        self.graph_url     = "https://gitlab.example.com/api/graphql"
        self.headers       = {'Authorization': f'Bearer {private_token}'}
        
    def find_terraform_state(self, search_string, terra_path):
        cursor = None
        found_states = {}
        while True:
            # GraphQL query
            query = """
            {{
            project(fullPath: "{terra_path}") {{
                terraformStates(first: 100, after: {cursor}) {{
                pageInfo {{
                    endCursor
                    hasNextPage
                }}
                nodes {{
                    name
                    lockedAt
                    id
                }}
                }}
            }}
            }}
            """.format(terra_path=terra_path, cursor=json.dumps(cursor) if cursor != 'null' else 'null')
            # API call
            response = requests.post(
                self.graph_url,
                headers=self.headers,
                json={'query': query}
            )
            # Check
            if response.status_code == 200:
                json_response = response.json()
                # print(json_response)
                states = json_response['data']['project']['terraformStates']['nodes']
                for state in states:
                    if search_string.lower() in state['name'].lower():
                        found_states[state['name']] = {'lockedAt': state['lockedAt'], 'id': state['id']}
                
                # get page info
                page_info = json_response['data']['project']['terraformStates']['pageInfo']
                cursor = page_info['endCursor']
                has_next_page = page_info['hasNextPage']
                
                # last page check
                if not has_next_page:
                    break
            else:
                return response.json()
        return found_states
    
    def lock_terraform_state(self, state_id):
        mutation = """
        mutation {
            terraformStateLock(input: {id: "%s"}) {
                clientMutationId
            }
        }
        """ % state_id
        response = requests.post(self.graph_url, 
                                 json={'query': mutation}, 
                                 headers=self.headers)
        return response.json()
    
    def unlock_terraform_state(self, state_id):
        mutation = """
        mutation {
            terraformStateUnlock(input: {id: "%s"}) {
                clientMutationId
            }
        }
        """ % state_id
        response = requests.post(self.graph_url, 
                                 json={'query': mutation}, 
                                 headers=self.headers)
        return response.json()
    
    def delete_terraform_state(self, state_id):
        mutation = """
        mutation {
            terraformStateDelete(input: {id: "%s"}) {
                clientMutationId
            }
        }
        """ % state_id
        response = requests.post(self.graph_url, 
                                 json={'query': mutation}, 
                                 headers=self.headers)
        return response.json()
