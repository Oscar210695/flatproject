from django.shortcuts import render, HttpResponse, redirect
import requests
from flatprojectmain.forms import MergeForm
from django.contrib import messages

#View to index page and list all the branches from the API
def index(request):
    route = 'http://' + request.META.get('HTTP_HOST') + '/api/branches/'

    resp = requests.get(route)

    branches = []

    if resp.status_code != 200:
        return HttpResponse(f"<h2>Error while consulting API</h2>")

    for branch in resp.json()['name']:
        branches.append(branch)

    return render(request, 'index.html',{
        'title': 'Branches',
        'branches': branches
    })

#View to list all the commits of a specific branch
def commits(request, branch):
    route = 'http://' + request.META.get('HTTP_HOST') + '/api/commits/' + branch

    resp = requests.get(route)

    commits = []

    if resp.status_code != 200:
        return HttpResponse(f"<h2>Error while consulting API</h2>")

    for commit in resp.json():
        commits.append({
            'key': commit,
            'message': resp.json()[commit][0],
            'email': resp.json()[commit][1],
            'date': resp.json()[commit][2],
        })

    return render(request, 'commits.html',{
        'title': branch,
        'commits': commits
    })

#View for commit detail of a specific commit of a branch
def commit_detail(request, commit):
    route = 'http://' + request.META.get('HTTP_HOST') + '/api/commit_detail/' + commit

    resp = requests.get(route)

    if resp.status_code != 200:
        return HttpResponse(f"<h2>Error while consulting API</h2>")

    commit_detail = resp.json()

    return render(request, 'commit_detail.html',{
        'title': commit,
        'commit_detail': commit_detail,
        'route': route,
    })

#View for list all the merges
def list_merges(request):
    ruta = 'http://' + request.META.get('HTTP_HOST') + '/api/merges/'

    resp = requests.get(ruta)

    merges = []

    if resp.status_code != 200:
        return HttpResponse(f"<h2>Error while consulting API</h2")
    for merge in resp.json():
        merges.append({
            'merge_id': merge['id'],
            'title': merge['title'],
            'description': merge['description'],
            'base_branch': merge['base_branch']['description'],
            'compare_branch': merge['compare_branch']['description'],
            'author': merge['author'],
            'email': merge['email'],
            'status': merge['status']['description'],
            'status_id': merge['status']['id'],
        })

    return render(request, 'merges.html',{
        'title': 'Merges',
        'merges': merges,
    })

#View for save a merge and merged or only saved
def save_merge(request):
    if request.method == 'POST':
        form = MergeForm(request.POST)

        if form.is_valid():
            data_form = form.cleaned_data

            base_branch = data_form.get('base_branch').id
            compare_branch = data_form.get('compare_branch').id

            if base_branch == compare_branch:
                messages.warning(request, f'You must choose two different branches')
                return redirect('add_merge')

            status = data_form.get('status').id
            author = None
            email = None
            description = data_form.get('description')

            if status == 3:
                ruta = 'http://' + request.META.get('HTTP_HOST') + '/api/merge_branch/'
                resp = requests.post(ruta, json={'branch_1':str(data_form.get('compare_branch')), 'branch_2':str(data_form.get('base_branch')), 'description': description})

                if resp.status_code != 200:
                    messages.error(request, f'We can´t merge, try again')
                    return redirect('add_merge')
                else:
                    if not resp.json()['resp']:
                        messages.error(request, f'We can´t merge these branches, try again: Exception: {resp.json()["data"]}')
                        return redirect('add_merge')

                    author = resp.json()['data']['author']
                    email = resp.json()['data']['email']

            title = data_form.get('title')

            ruta = 'http://' + request.META.get('HTTP_HOST') + '/api/merges/'
            resp = requests.post(ruta, json={'title':title, 'description':description, 
                                            'base_branch': base_branch, 'compare_branch': compare_branch, 
                                            'author': author, 'email': email, 'status':status})

            if resp.status_code != 201:
                messages.error(request, f'We can´t save the merge {title}, try again')
                return redirect('add_merge')
            else:
                messages.success(request, f'Merge {title} saved/merged succesfully')
                return redirect('merges')
            
    else:
        form = MergeForm()

    return render(request, 'add_merge.html', {
        'title': 'Add Merge',
        'form': form,
    })

#View for close the merge if it is open
def close_merge(request, id):
    ruta = 'http://' + request.META.get('HTTP_HOST') + '/api/merges/' + id + '/'
    resp = requests.patch(ruta, json={'status': 2})

    if resp.status_code != 200:
        messages.error(request, f'We can´t close the merge')
        return redirect('merges')

    messages.success(request, f'Merge has been closed')

    return redirect('merges')