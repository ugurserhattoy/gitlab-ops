import gitlab

class SetThingsUp:
    def __init__(self, gl):
        self.gl = gl
        
    def defBranch(self, input, project_list):
        for project in project_list:
            p = self.gl.projects.get(int(project))
            if p.branches.list(search=input):
                p.default_branch = input
                p.save()
                print(p.name+" changed to " + input)
            else:
                print(p.name+" is passed! [BranchNotExist]")
        return {'defBranch': input}
                
    def squashOption(self, input, project_list): # never, always, default_on, default_off
        for project in project_list:
            p = self.gl.projects.get(int(project))
            p.squash_option = input
            p.save()
        return {'squashOption': input}
    
    def allowMrOnlyIfAllDiscResolved(self, input, project_list): # True, False
        for project in project_list:
            p = self.gl.projects.get(project)
            p.only_allow_merge_if_all_discussions_are_resolved = input
            p.save()
        return {'allowMrOnlyIfAllDiscResolved': input}
    
    def removeBranchAfterMerge(self, input, project_list): # True, False
        for project in project_list:
            p = self.gl.projects.get(project)
            p.remove_source_branch_after_merge = input
            p.save()
        return {'removeBranchAfterMerge': input}
    
    def protectedBranches(self, input, project_list):
        branches = []
        for project in project_list:
            p = self.gl.projects.get(project)
            for b in p.branches.list():
                branches.append(b.name)
            if input in branches:
                p.protectedbranches.create({
                    'name': input,
                    'merge_access_level': gitlab.const.AccessLevel.DEVELOPER,
                    'push_access_level': gitlab.const.AccessLevel.DEVELOPER,
                    'allow_force_push': 'False'
                })
                branches.clear()
            else:
                branches.clear()
                print(str(project) + "[NoBranchFound]: " + input)
        return {'protectedBranch': input}
    
    def removeBranchProtection(self, input, project_list):
        p_branches = []
        for project in project_list:
            p = self.gl.projects.get(project)
            for i in p.protectedbranches.list():
                p_branches.append(i.name)
            if input in p_branches:
                p.protectedbranches.delete(input)
                p_branches.clear()
            else:
                p_branches.clear()
                print(str(project) + "[NoProtectionForBranch]: " + input)
        return {'removedProtection': input}
    