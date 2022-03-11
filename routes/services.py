from trains.models import Train


def get_graph(queryset):
    graph = {}
    for q in queryset:
        graph.setdefault(q.from_city_id, set())
        graph[q.from_city_id].add(q.to_city_id)
    return graph


def get_routes(request, form) -> dict:
    qs = Train.objects.all()
    graph = get_graph(qs)
    print(graph)

