import inquirer
import os
import ProjectOps, AuthOps
from dotenv import load_dotenv

load_dotenv()

BASE = os.getenv('BASE')

json_data = []
json_list = {}
AuthOps = AuthOps.AuthOps(BASE)
def login_screen():
    login_menu_list = ['Login', 'Create User', 'Exit']
    TOKN=""
    questions = [
        inquirer.List('login',
                      message="Login if you have created a user before...",
                      choices=login_menu_list,
                      carousel=True,
        ),
    ]
    answer = inquirer.prompt(questions)['login']
    if answer == 'Login':
        TOKN = AuthOps.user_login()
    elif answer == 'Create User':
        AuthOps.user_create()
        TOKN = AuthOps.user_login()
    elif answer == "Exit":
        exit(0)
    else:
        print("Something's Wrong")
        login_screen()
    return TOKN
TOKN = login_screen()
ProjectList = ProjectOps.ProjectsList(BASE, json_list, TOKN)

print("")
print("Welcome!")
def main():
    check_project_list('main')
    welcome_menu()
    
def check_project_list(area):
    if json_list:
        ProjectList.db_check(area)
        
def welcome_menu():
    welcome_menu_list = ['Add project', 'Remove project', 'Branch settings', 'Merge request settings', 'Clear list', 'Exit']
    questions = [
        inquirer.List('welcome',
                    message="What would you like to do with the project list?",
                    choices=welcome_menu_list,
                    carousel=True,
                    ),
    ]
    answer = inquirer.prompt(questions)['welcome']
    
    if answer == "Add project":
        print("     Add project")
        add_project_menu()
    elif answer == "Remove project":
        print("     Remove project")
        remove_from_list()
    elif answer == "Branch settings":
        print("     Branch settings")
        branch_menu()
    elif answer == "Merge request settings":
        print("     Merge request settings")
        mr_menu()
    elif answer == "Clear list":
        clean_project_list_file()
    elif answer == "Exit":
        exit(0)
    else:
        print("Try again...")
        print("")
        welcome_menu()

def add_project_menu():
    add_project_menu_list = ['With ID', 'With project path', 'With group path', 'Back']
    questions = [
        inquirer.List('add_project',
                    message="How would you like to add the project?",
                    choices=add_project_menu_list,
                    carousel=True,
                    ),
    ]
    answer = inquirer.prompt(questions)['add_project']
    
    if answer == "With group path":
        print("""
To avoid confusion in group names, it is necessary to use full path.
Group full path example: mpfinance/einvoice for url: https://gitlab.hepsiburada.com/mpfinance/einvoice
Group full path example: ugurserhattoy for url: https://gitlab.hepsiburada.com/ugurserhattoy
""")
        group_path = input("Enter Group Full Path: ")
        ProjectList.append_projects_by_group_path(group_path)
        check_project_list('main')
        add_project_menu()
    
    elif answer == "With project path":
        print("Under construction...")
        add_project_menu()
        
    elif answer == "With ID":
        append_project_by_id()
            
    elif answer == "Back":
        main()

def append_project_by_id():
    print("")
    print(" - They can be added one by one by entering the Project ID and pressing enter,")
    print(" - Multiple Project IDs can be added by leaving a space between them!")
    print(" - Leave blank to go back...")
    print("")
    user_input = input('Project ID: ')
    if user_input=="" or user_input.isspace():
        check_project_list('main')
        add_project_menu()
    else:
        id_list = map(str, user_input.split())
        id_list = list(id_list)
        ProjectList.append_projects_by_id(id_list)
        check_project_list('main')
        append_project_by_id()

def branch_menu():
    check_project_list("branch")
    add_project_menu_list = ['Change default branch', 'Protect a Branch', 'Remove protected branch', 'Back']
    questions = [
        inquirer.List('branch',
                    message="What do you want to change for branches?",
                    choices=add_project_menu_list,
                    carousel=True,
                    ),
    ]
    answer = inquirer.prompt(questions)['branch']
    if answer=="Change default branch":
        change_default_branch()
        branch_menu()
    elif answer=='Protect a Branch':
        protect_a_branch()
    elif answer=="Remove protected branch":
        remove_protected_branch()
        branch_menu()
    else:
        main()

def change_default_branch():
    questions = [
        inquirer.Text('def_branch', message="Default branch")
    ]
    answer = inquirer.prompt(questions)['def_branch']
    if answer=="" or answer.isspace():
        main()
    else:
        ProjectList.update_default_branch(answer)
        branch_menu()

def clean_project_list_file():
    question = [
        inquirer.Confirm("confirm", 
                      message="Project list will be cleared?",
                      default=False,
        ),
    ]
    answer = inquirer.prompt(question)['confirm']
    if answer:
        ProjectList.clean_project_list()
    else:
        print("List not cleared...")
        print("")
    check_project_list("main")
    welcome_menu()

def mr_menu():
    check_project_list("mr")
    add_project_menu_list = ['Squash option', 'Allow merge if all discussions resolved', 'Remove branch after merge', 'Back']
    questions = [
        inquirer.List('update_project',
                    message="Which option to update?",
                    choices=add_project_menu_list,
                    carousel=True,
                    ),
    ]
    answer = inquirer.prompt(questions)['update_project']
    if answer=="Squash option":
        update_squash_option()
        mr_menu()
    elif answer=="Allow merge if all discussions resolved":
        update_allow_mr_all_disc_resolved()
        mr_menu()
    elif answer=="Remove branch after merge":
        remove_branch_after_merge()
        mr_menu()
    else:
        main()

def protect_a_branch():
    if json_list:
        print("")
        print(" - Leave it blank to go back")
        print("")
        user_input = input('Which branch?: ')
        if user_input=="" or user_input.isspace():
            main()
        else:
            ProjectList.protect_a_branch(user_input)
            branch_menu()
    else:
        print("List is empty! Returning to the main menu...")
        main()

def remove_from_list():
    check_project_list('main')
    if json_list:
        print("")
        print(" - Leave it blank to return")
        print(" - Multiple lines can be deleted by leaving a space between them (i.e. = 7 16 9 )")
        print("")
        user_input = input('Line(s): ')
        if user_input=="" or user_input.isspace():
            main()
        else:
            ProjectList.remove_lines_from_file(user_input)
            main()
    else:
        print("List is empty! Returning back to the main menu")
        main()

def remove_branch_after_merge():
    options = ['True', 'False', 'Back']
    questions = [
        inquirer.List(
            'remove_branch',
            message="Remove branch after merge?",
            choices=options,
            carousel=True,
        ),
    ]
    answer = inquirer.prompt(questions)['remove_branch']   
    if answer=="True" or answer=="False":
        ProjectList.remove_branch_after_merge(answer)
    else:
        print("Answer is not valid!")

def remove_protected_branch():
    check_project_list('branch')
    if json_list:
        print("")
        print(" - Leave it blank to go back")
        print("")
        user_input = input('Which branch?: ')
        if user_input=="" or user_input.isspace():
            main()
        else:
            ProjectList.remove_protected_branch(user_input)
            check_project_list("branch")
            branch_menu()
    else:
        print("Empty list! Returning to the main menu")
        main()
    
def update_allow_mr_all_disc_resolved():
    options = ['True', 'False', 'Back']
    questions = [
        inquirer.List(
            'allow_mr',
            message="Allow merge if all discussions resolved?",
            choices=options,
            carousel=True,
        ),
    ]
    answer = inquirer.prompt(questions)['allow_mr']   
    if answer=="True" or answer=="False":
        ProjectList.update_only_allow_merge_if_all_discussions_resolved(answer)
    else:
        mr_menu()

def update_squash_option():
    options = ['never', 'always', 'default_on', 'default_off', 'Back']
    questions = [
        inquirer.List(
            'squash_option',
            message="Squash Option?",
            choices=options,
            carousel=True,
        ),
    ]
    answer = inquirer.prompt(questions)['squash_option']
    if answer == 'Back':
        mr_menu()
    else:
        ProjectList.update_squash_option(answer)

if __name__=="__main__":
    main()
