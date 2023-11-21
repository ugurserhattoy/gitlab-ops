import requests
from tqdm import tqdm
import os

class TerraOps:
    def __init__(self, BASE, TOKN, full_path) -> None:
        self.full_paths = full_path #Change according to your projects' full paths in run.py terraform_menu
        self.BASE       = BASE
        self.TOKN       = {"Authorization": f"Bearer {TOKN}"}
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def get_terraform_states(self, search_string):
        results = {}
        for full_path in tqdm(self.full_paths):
            data = {'full_path': full_path}
            response = requests.get(url = self.BASE + "terraform/" + search_string, 
                                     json=data, 
                                     headers=self.TOKN)
            if response.status_code == 200:
                state_data = response.json()
                if state_data:
                    results.update(state_data)
        return results
    
    def lock_terraform_state(self, state_id, state_name):
        data     = {'state_id': state_id}
        response = requests.put(url = self.BASE + "terraform/lock",
                                    json=data,
                                    headers=self.TOKN)
        if "200" in str(response):
            self.clear_screen()
            print(state_name + " is locked!")
            print()
        else:
            print(response)
            print()
        return response
    
    def unlock_terraform_state(self, state_id, state_name):
        data     = {'state_id': state_id}
        response = requests.put(url = self.BASE + "terraform/unlock",
                                    json=data,
                                    headers=self.TOKN)
        if "200" in str(response):
            self.clear_screen()
            print(state_name + " is unlocked!")
            print()
        else:
            print(response)
            print()
        return response
    
    def delete_terraform_state(self, state_id, state_name):
        data     = {'state_id': state_id}
        response = requests.delete(url = self.BASE + "terraform",
                                    json=data,
                                    headers=self.TOKN)
        if "200" in str(response):
            self.clear_screen()
            print(state_name + " is DELETED!")
            print()
        else:
            print(response)
            print()
        return response
