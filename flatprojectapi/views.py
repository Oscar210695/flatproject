from rest_framework.views import APIView 
from rest_framework.response import Response  
from rest_framework import permissions, viewsets
from git import Repo
from django.conf import settings
import os
from .serializers import MergeSerializerClass
from .models import Merges, Branches

#Path in C for download the repo
PARENT_DIR = os.path.join('/', os.pardir)
path = os.path.join(PARENT_DIR, 'flatproject')

#Check if already exists
if os.path.isdir(os.path.join(path)):
    repo = Repo(path)
    branches = [b.name.split('/')[1] for b in repo.remote().refs if not (b.name.split('/')[1] == 'HEAD' or b.name.split('/')[1] == 'dependabot')]
    for branch in branches:
        #Pull all the branches
        repo.git.checkout(branch)
        repo.git.pull('origin',branch)       
        #If there are another branch add to DB
        if not (Branches.objects.filter(description=branch).exists()):
            b = Branches(description=branch)
            b.save()

    repo.git.checkout('master')
else:
    Repo.clone_from('https://github.com/Oscar210695/flatproject.git', path, b='master')
    repo = Repo(path)
    branches = [b.name.split('/')[1] for b in repo.remote().refs if not (b.name.split('/')[1] == 'HEAD' or b.name.split('/')[1] == 'master' or b.name.split('/')[1] == 'dependabot')]
    for branch in branches:
        repo.git.checkout(branch)
        repo.git.pull('origin',branch)    
        if not (Branches.objects.filter(description=branch).exists()):
            b = Branches(description=branch)
            b.save()
    if not (Branches.objects.filter(description='master').exists()):  
        b = Branches(description='master')
        b.save()

    repo.git.checkout('master')
        
#View for List of Branches
class BranchView(APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get', 'head']

    def get(self, request, *args, **kwargs):
        branches={}
        branches['name'] = [b.name.split('/')[1] for b in repo.remote().refs if not (b.name.split('/')[1] == 'HEAD' or b.name.split('/')[1] == 'dependabot')]

        return Response(status=200, data=branches)

#View for List of Commits of a specific branch
class CommitView(APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get', 'head']

    def get(self, request, branch):
        commits={}
        repo.git.checkout(branch)
        result = [x for x in repo.iter_commits(rev=branch)]

        for commit in result:
            commits[commit.hexsha] = [commit.summary, commit.author.name, commit.author.email, str(commit.committed_datetime)]

        return Response(status=200, data=commits)

#View for Commit detail of a especific branch and a specific commit
class CommitDetailView(APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get', 'head']

    def get(self, request, commit):
        commit_detail={}
        result = repo.commit(commit)

        commit_detail['message'] = result.summary
        commit_detail['date'] = str(result.committed_datetime)
        commit_detail['files'] = result.stats.files
        commit_detail['author'] = result.author.name
        commit_detail['email'] = result.author.email
        commit_detail['number_files'] = len(result.stats.files)

        return Response(status=200, data=commit_detail)

#View for merge branches
class MergeBranchesView(APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['head', 'post']

    def post(self, request):
        try:
            current = repo.branches[request.data['branch_1']]
            master = repo.branches[request.data['branch_2']]
            description = request.data['description']

            repo.git.checkout(request.data['branch_2'])

            base = repo.merge_base(current, master)
            repo.index.merge_tree(master, base=base)

            repo.index.commit(description, parent_commits=(current.commit, master.commit))

            repo.git.push('origin', request.data['branch_2'])

            return Response(status=200, data={"resp":True, "data":{'author': current.commit.author.name, 'email': current.commit.author.email}})
        except Exception as ex:
            return Response(status=200, data={"resp":False, "data":str(ex)})
  
#View for list al the merges
class getMerges(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get', 'head', 'patch', 'post']

    serializer_class = MergeSerializerClass         
    queryset = Merges.objects.all()
