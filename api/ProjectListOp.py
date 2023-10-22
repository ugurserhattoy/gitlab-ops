class ProjectListFuncs:
    
    def __init__(self, gl, project_list):
        self.project_list = project_list
        self.gl = gl
    
    def getProjectById(self, id):
        p = self.gl.projects.get(id)
        return p

    def putProjectsByGroup(self, group):
        group_list = self.gl.groups.list(search=group)
        for g in group_list:
            if str(g.full_path)==group:
                proj_list = g.projects.list(all=True)
                for p in proj_list:
                    self.putProjectArgs(self.getProjectById(p.id))
        

    def putProjectArgs(self, p):
        self.project_list[p.id] = {
            'name': p.name,
            'defBranch': p.default_branch,
            'url': p.attributes['web_url'],
            'squashOption': p.squash_option,
            'allowMrOnlyIfAllDiscResolved': p.attributes['only_allow_merge_if_all_discussions_are_resolved'],
            'removeBranchAfterMerge': p.attributes['remove_source_branch_after_merge'],
            'protectedBranches': self.protectedBranches(p),
            }

    def protectedBranches(self, p):
        p_branches = []
        try:
            for i in p.protectedbranches.list():
                p_branches.append({'name': i.name, 'force_push': i.allow_force_push})
            return p_branches
        except:
            return p_branches
