import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from bipartite_to_networkflow import *


def index(request):
    return HttpResponse("<h1>Hello World</h1>")


@csrf_exempt
def get_maximum_matching(request):
    if request.method == "GET":
        print(request.GET['scenario'], type(request.GET['scenario']))
        parameters = request.GET['scenario']
        scenario = get_data(parameters)
        bipartite_graph = generate_bipartite_graph(scenario)
        g = bipartite_to_networkflow(bipartite_graph)
        maximum = EK(g,"s", "t")
        return HttpResponse(maximum)