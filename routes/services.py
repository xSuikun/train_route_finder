from trains.models import Train


def get_graph(queryset):
    graph = {}
    for q in queryset:
        graph.setdefault(q.from_city_id, set())
        graph[q.from_city_id].add(q.to_city_id)
    return graph


def get_dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex not in graph:
            continue
        for nxt in graph[vertex] - set(path):
            if nxt == goal:
                yield path + [nxt]
            else:
                stack.append((nxt, path + [nxt]))


def get_routes_containing_cities(required_cities, raw_routes):
    if not required_cities:
        return raw_routes
    _cities = [city.id for city in required_cities]
    correct_routes = []
    for route in raw_routes:
        if all(city in route for city in _cities):
            correct_routes.append(route)
    if not correct_routes:
        raise ValueError('Маршрут через выбранные города не найден')
    return correct_routes


def get_on_time_routes(routes, all_trains, required_time):
    on_time_routes = []
    for route in routes:
        tmp = {'trains': [], 'total_travel_time': 0}
        for i in range(len(route) - 1):
            # candidate_train[0] берется при условии, что в Meta классе модели стоит ordering
            # по travel_time, от меньшего к большему
            candidate_train = all_trains[(route[i], route[i + 1])][0]
            tmp['total_travel_time'] += candidate_train.travel_time
            tmp['trains'].append(candidate_train)
        if tmp['total_travel_time'] <= required_time:
            on_time_routes.append(tmp)
    if not on_time_routes:
        raise ValueError('Нет маршрутов, подходящих под выбранное время пути')
    return on_time_routes


def sort_routes(routes):
    sorted_routes = []
    if len(routes) == 1:
        return routes
    else:
        times = list(set(route['total_travel_time'] for route in routes))
        times = sorted(times)
        for time in times:
            for route in routes:
                if time == route['total_travel_time']:
                    sorted_routes.append(route)
    return sorted_routes


def get_routes(request, form) -> dict:
    context = {'form': form}
    trains_queryset = Train.objects.all().select_related('from_city', 'to_city')
    graph = get_graph(trains_queryset)
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    required_travel_time = data['travel_time']
    required_cities = data['cities']

    all_trains = {}
    for train in trains_queryset:
        all_trains.setdefault((train.from_city_id, train.to_city_id), [])
        all_trains[(train.from_city_id, train.to_city_id)].append(train)

    raw_routes = list(get_dfs_paths(graph, from_city.pk, to_city.pk))
    if not len(list(raw_routes)):
        raise ValueError('Маршрута, удовлетворяющего условиям не существует')
    routes_with_required_cities = get_routes_containing_cities(required_cities, raw_routes)
    on_time_routes = get_on_time_routes(routes_with_required_cities, all_trains, required_travel_time)
    sorted_routes = sort_routes(on_time_routes)

    context['routes'] = sorted_routes
    print(context['routes'])
    context['cities'] = {'from_city': from_city, 'to_city': to_city, 'required_cities': required_cities}
    return context

