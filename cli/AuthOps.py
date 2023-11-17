import inquirer
import requests

class AuthOps:
    
    def __init__(self, BASE) -> None:
        self.BASE = BASE
    
    def user_login(self):
        print()
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        while True:    
            questions = [
                inquirer.Text("user", message="Username", validate=lambda _, x: x != "."),
                inquirer.Password("password", message="Password"),
            ]
            answers = inquirer.prompt(questions) #Dict
            user = answers.get('user')
            password = answers.get('password')
            response = requests.post(url=self.BASE + "token",
                                    data={'username': user, 
                                        'password': password},
                                    headers=headers)
            # print(str(response.status_code)+": "+response.json())
            if response.status_code == 200:
                break
            else:
                print()
                print(response.json())
                print()
            
        TOKN=str(response.json()['access_token'])
        return TOKN
        
        
    def user_create(self):
        headers = {'Content-Type': 'application/json'}
        questions = [
            inquirer.Text("user", message="Username", validate=lambda _, x: x != "."),
            inquirer.Password("password", message="Password"),
            inquirer.Text("token", message="Private Token"),
        ]
        answers = inquirer.prompt(questions)
        print(answers)
        response = requests.post(url=self.BASE + "register",
                                 json={'username': answers.get('user'), 
                                       'password': answers.get('password'),
                                       'private_token': answers.get('token')},
                                 headers=headers)
        print(response.json())
        print(response.status_code)
        print(response)
        
    def me_check(self, TOKN):
        response = requests.get(url=self.BASE + "users/me",
                                headers={"Authorization": "Bearer "+TOKN}
                                 )
        # print(response.status_code)
        print(response.json())
        
        