from trains.models import Train


def get_graph(queryset):
    graph = {}
    for q in queryset:
        graph.setdefault(q.from_city_id, set())
        graph[q.from_city_id].add(q.to_city_id)
    return graph


def get_routes(request, form) -> dict:
    context = {'form': form}
    trains_queryset = Train.objects.all().select_related('from_city', 'to_city')
    graph = get_graph(trains_queryset)
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    travel_time = data['travel_time']
    required_cities = data['cities']

    all_ways = list(dfs_paths(graph, from_city.pk, to_city.pk))
    if not len(list(all_ways)):
        raise ValueError('Маршрута, удовлетворяющего условиям не существует')

    if required_cities:
        # Проверка, содержит ли путь все города, через которые пользователь хочет проехать, если таковые есть
        _cities = [city.id for city in required_cities]
        correct_ways = []
        for route in all_ways:
            if all(city in route for city in _cities):
                correct_ways.append(route)
        if not correct_ways:
            raise ValueError('Маршрут через выбранные города не найден')
    else:
        correct_ways = all_ways

    all_trains = {}
    on_time_routes = []
    for train in trains_queryset:
        all_trains.setdefault((train.from_city_id, train.to_city_id), [])
        all_trains[(train.from_city_id, train.to_city_id)].append(train)
    for route in correct_ways:
        tmp = {'trains': [], 'total_travel_time': 0}
        for i in range(len(route) - 1):
            # 0 элемент в candidate_train берется при условии, что в Meta классе модели стоит ordering
            # по travel_time, от меньшего к большему
            candidate_train = all_trains[(route[i], route[i + 1])][0]
            tmp['total_travel_time'] += candidate_train.travel_time
            tmp['trains'].append(candidate_train)
        if tmp['total_travel_time'] <= travel_time:
            on_time_routes.append(tmp)
    if not on_time_routes:
        raise ValueError('Нет маршрутов, подходящих под выбранное время пути')
    sorted_routes = []
    if len(on_time_routes) == 1:
        sorted_routes = on_time_routes
    else:
        times = list(set(r['total_travel_time'] for r in on_time_routes))
        times = sorted(times)
        for time in times:
            for route in on_time_routes:
                if time == route['total_travel_time']:
                    sorted_routes.append(route)
    context['routes'] = sorted_routes
    context['cities'] = {'from_city': from_city.name, 'to_city': to_city.name, 'required_cities': required_cities}
    return context


def dfs_paths(graph, start, goal):
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
