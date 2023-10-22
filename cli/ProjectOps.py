# ProjectList class
import requests

class ProjectsList:
    # ProjectList class
    def __init__(self, BASE, json_list, TOKN):
        self.json_list = json_list
        self.BASE = BASE
        self.TOKN = {"Authorization": f"Bearer {TOKN}"}
    
    def append_projects_by_group_path(self, group):###
        response = requests.put(url = self.BASE + "projectlist",
                                json={'group': group},
                                headers=self.TOKN,)
        response = response.json()
        for k in response.keys():
            self.json_list[k] = response[k]
            # print(self.json_list)
                
    def append_projects_by_id(self, id_list):##
        for i in range(len(id_list)):
            if id_list[i].isdigit():
                response = requests.put(url = self.BASE + "projectlist",
                                        json={'id': id_list[i]},
                                        headers=self.TOKN,)
                self.json_list[id_list[i]] = response.json()[id_list[i]]
                # print(response.json())
            else:
                print(id_list[i] + " is not number")

    def clean_project_list(self):
        response = requests.delete(url = self.BASE + "projectlist")
        self.json_list.clear()
        return response
                           
    def db_check(self, area):###
        print("")
        print("-------------------------------------------------------------------------------------------")
        # print("{0: <4} {1: ^8} {2: ^35} {3: ^20} {4: ^20}".format('____', '________', "___________PROJE_LISTESI___________", '____________________', '____________________'))
        print("{0: <4} {1: ^8} {2: ^35} {3: ^20} {4: ^20}".format('', '', "PROJE LISTESI", '', ''))
        if area=="mr":
            print("{0: <4} {1: ^8} {2: ^35} {3: ^20} {4: ^20} {5: ^20}".format('----', '--------', "-----------------------------------", '--------------------', '--------------------', '--------------------'))
            print("{0: <4} {1: ^8} {2: ^35} {3: ^20} {4: ^20} {5: ^20}".format('LINE', 'ID', 'NAME', 'SQUASH OPTION', 'ALLOW MR ONLY IADR', 'RM BRANCH'))
            print("{0: <4} {1: ^8} {2: ^35} {3: ^20} {4: ^20} {5: ^20}".format('----', '--------', "-----------------------------------", '--------------------', '--------------------', '--------------------'))
        elif area=='branch':
            print("{0: <4} {1: ^8} {2: ^35} {3: ^20} {4: ^20}".format('----', '--------', "-----------------------------------", '--------------------', '--------------------'))
            print("{0: <4} {1: ^8} {2: ^35} {3: ^20} {4: ^20}".format('LINE', 'ID', 'NAME', 'DEF BRANCH', 'PROTECTED BRANCHES'))
            print("{0: <4} {1: ^8} {2: ^35} {3: ^20} {4: ^20}".format('----', '--------', "-----------------------------------", '--------------------', '--------------------'))
        else:    
            print("{0: <4} {1: ^8} {2: ^35} {3: ^20} {4: ^20}".format('----', '--------', "-----------------------------------", '--------------------', '--------------------'))
            print("{0: <4} {1: ^8} {2: ^35} {3: ^20} {4: ^20}".format('LINE', 'ID', 'NAME', 'DEF BRANCH', 'URL'))
            print("{0: <4} {1: ^8} {2: ^35} {3: ^20} {4: ^20}".format('----', '--------', "-----------------------------------", '--------------------', '--------------------'))
        line_number = 1
        for proje in self.json_list.keys():     
            if area=="mr":
                print("{0: <4} {1: ^8} {2: <35} {3: ^20} {4: ^20} {5: ^20}".format(line_number, proje, self.json_list[proje]['name'], self.json_list[proje]['squashOption'], self.json_list[proje]['allowMrOnlyIfAllDiscResolved'], self.json_list[proje]['removeBranchAfterMerge']))
            elif area=='branch':
                protected_list = []
                protected_branches = ""
                for i in self.json_list[proje]['protectedBranches']:
                    protected_list.append(i['name'])
                    protected_branches = ', '.join(protected_list)
                print("{0: <4} {1: ^8} {2: <35} {3: ^20} {4: ^20}".format(line_number, proje, self.json_list[proje]['name'], self.json_list[proje]['defBranch'], protected_branches))
            else:    
                print("{0: <4} {1: ^8} {2: <35} {3: ^20} {4: ^20}".format(line_number, proje, self.json_list[proje]['name'], self.json_list[proje]['defBranch'], self.json_list[proje]['url']))
            line_number += 1
            
            # print("{%s: >20} {%s: >20} {%s: >20} {%s: >20}".format() % (proje, p.name, p.default_branch, p.attributes['web_url']))
            # p = self.gl.projects.get(proje)
            # print("id: %s    name: %s     default branch: %s    url: %s".format() % (proje, p.name, p.default_branch, p.attributes['web_url']))
        print("")

    def protect_a_branch(self, input):
        response = requests.put(url = self.BASE + "projectlist/protectedBranches",
                        json={'idList': list(self.json_list.keys()), 'input': input},
                        headers=self.TOKN,)
        self.append_projects_by_id(list(self.json_list.keys()))
        print(response.json())

    def remove_branch_after_merge(self, input):
        response = requests.put(url = self.BASE + "projectlist/removeBranchAfterMerge",
                        json={'idList': list(self.json_list.keys()), 'input': input},
                        headers=self.TOKN,)
        self.append_projects_by_id(list(self.json_list.keys()))
        print(response.json())

    def remove_lines_from_file(self, user_input): ##
        i = 1
        line_list = list(map(int, user_input.split()))
        keys_to_delete = []
        for key in self.json_list.keys():
            if i in line_list:
                keys_to_delete.append(key)
            i += 1
        for key in keys_to_delete:
            del self.json_list[key]
        
    def remove_protected_branch(self, input):
        response = requests.delete(url = self.BASE + "projectlist/protectedBranches",
                        json={'idList': list(self.json_list.keys()), 'input': input},
                        headers=self.TOKN,)
        self.append_projects_by_id(list(self.json_list.keys()))
        print(response.json())
        
    def update_default_branch(self, def_branch):
        response = requests.put(url = self.BASE + "projectlist/defBranch",
                            json={'idList': list(self.json_list.keys()), 'input': def_branch},
                            headers=self.TOKN,)
        self.append_projects_by_id(list(self.json_list.keys()))
        print(response.json())
    
    def update_squash_option(self, squash_option): # never, always, default_on, default_off
        response = requests.put(url = self.BASE + "projectlist/squashOption",
                        json={'idList': list(self.json_list.keys()), 'input': squash_option},
                        headers=self.TOKN,)
        self.append_projects_by_id(list(self.json_list.keys()))
        print(response.json())
    
    def update_only_allow_merge_if_all_discussions_resolved(self, new_option): # True, False
        response = requests.put(url = self.BASE + "projectlist/allowMrOnlyIfAllDiscResolved",
                        json={'idList': list(self.json_list.keys()), 'input': new_option},
                        headers=self.TOKN,)
        self.append_projects_by_id(list(self.json_list.keys()))
        print(response.json())
