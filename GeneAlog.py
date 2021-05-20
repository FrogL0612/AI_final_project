import random as rd
import copy


class Location:
    def __init__(self, name):
        self.name = name

    def distance_between(self, goal):
        global searched_path
        if (self.name, goal.name) not in searched_path.keys():
            searched_path[(self.name, goal.name)] = self.UCS_search(goal)
        return searched_path[(self.name, goal.name)]

    def UCS_search(self, goal):
        global Graph
        goal = goal.name
        start = self.name
        frontier_list = [start]
        # 紀錄每個path的cost
        frontier_dict = {start: 0}

        while frontier_list:
            # 從frontier中取出一個新的path
            now_path = frontier_list.pop(0)

            # 確認是否找到end
            if now_path[-1] == goal:
                return frontier_dict[now_path]

            # 擴展新的node
            for neighbor in Graph[now_path[-1]].keys():
                new_path = now_path + neighbor
                # 確認neighbor並非走過的路徑 且 目標new_path尚未探索過
                if neighbor not in now_path and new_path not in frontier_dict.keys():
                    frontier_dict[new_path] = frontier_dict[now_path] + Graph[now_path[-1]][neighbor]
                    frontier_list.append(new_path)
                else:
                    continue
                frontier_list = sorted(frontier_list, key=lambda path: frontier_dict[path])
        return None


class Route:
    def __init__(self, path):
        self.path = path
        self.length = self._set_length()

    def _set_length(self):
        total_length = 0
        path_copy = self.path[:]
        now_here = path_copy.pop(0)
        init_node = copy.deepcopy(now_here)
        while path_copy:
            to_there = path_copy.pop(0)
            total_length += to_there.distance_between(now_here)
            now_here = copy.deepcopy(to_there)
        return total_length


class GeneticAlgo:
    def __init__(self, target_loc, level=10, population=100, variant=3,
                 mutate_percent=0.01, elite_save_percent=0.2):
        # 目標地點
        self.target_loc = target_loc
        # 子代數目
        self.level = level
        # 群體大小
        self.population = population
        self.variant = variant
        # 變異比例
        self.mutates = int(mutate_percent * population)
        self.elite = int(elite_save_percent * population)

    # 用來隨機生成一組route
    def _gen_rand_path(self):
        Target_copy = self.target_loc[:]
        route = list()
        while Target_copy:
            rand_target = Target_copy.pop(Target_copy.index(rd.choice(Target_copy)))
            route.append(rand_target)
        return route

    # 生成等同population數的routes
    def _init_routes(self):
        Routes = list()
        for _ in range(self.population):
            rand_gen_route = Route(self._gen_rand_path())
            Routes.append(rand_gen_route)
        return Routes

    def _next_generation(self, routes):
        routes.sort(key=lambda x: x.length, reverse=False)
        elites = routes[:self.elite][:]
        next_generation = self._crossover(elites)
        return next_generation[:] + elites

    def _crossover(self, elites):
        normal_breeds, mutate_breeds = list(), list()
        mutate_ones = list()
        for _ in range(self.population - self.mutates):
            father, mother = rd.choices(elites[:4], k=2)
            index_start = rd.randrange(0, len(father.path) - self.variant - 1)

            father_gene = father.path[index_start: index_start + self.variant]
            father_gene_names = [loc.name for loc in father_gene]

            mother_gene = [gene for gene in mother.path if gene.name not in father_gene_names]
            mother_gene_cut = rd.randrange(1, len(mother_gene))

            next_route_path = mother_gene[:mother_gene_cut] + father_gene + mother_gene[mother_gene_cut:]
            next_route = Route(next_route_path)

            normal_breeds.append(next_route)

            copy_father = copy.deepcopy(father)
            idx = range(len(copy_father.path))
            gene1, gene2 = rd.sample(idx, 2)
            copy_father.path[gene1], copy_father.path[gene2] = copy_father.path[gene2], copy_father.path[gene1]

            mutate_ones.append(copy_father)
            mutate_breeds = rd.choices(mutate_ones, k=self.mutates)

        return normal_breeds + mutate_breeds

    def evolution(self):
        routes = self._init_routes()
        for _ in range(self.level):
            routes = self._next_generation(routes)
        routes.sort(key=lambda x: x.length, reverse=False)
        return routes[0].path, routes[0].length


Graph = {'A': {'B': 15},
         'B': {'A': 15, 'C': 16},
         'C': {'B': 16, 'D': 3, 'J': 5, 'I': 4},
         'D': {'C': 3, 'E': 4, 'c': 4, 'd': 10},
         'E': {'D': 4, 'F': 30, 'W': 3, 'X': 3},
         'F': {'E': 30, 'G': 16},
         'G': {'F': 16, 'e': 8},
         'H': {'I': 8},
         'I': {'H': 8, 'C': 4},
         'J': {'C': 5, 'K': 5},
         'K': {'J': 5, 'L': 4, 'S': 4, 'T': 3},
         'L': {'M': 3, 'K': 4},
         'M': {'b': 2, 'L': 3, 'N': 3, 'U': 3},
         'N': {'O': 39, 'V': 3, 'M': 3, 'W': 4},
         'O': {'N': 39, 'P': 33},
         'P': {'O': 33},
         'Q': {'R': 25},
         'R': {'Q': 25, 'S': 20},
         'S': {'R': 20, 'K': 4},
         'T': {'U': 2, 'K': 3},
         'U': {'a': 17, 'V': 2, 'T': 2, 'M': 3},
         'V': {'U': 2, 'N': 3},
         'W': {'N': 4, 'E': 3},
         'X': {'E': 3, 'Y': 8},
         'Y': {'X': 8},
         'Z': {'a': 24},
         'a': {'Z': 24, 'U': 17},
         'b': {'M': 2, 'c': 2},
         'c': {'b': 2, 'D': 4},
         'd': {'D': 10, 'e': 10},
         'e': {'G': 8, 'd': 10}}

searched_path = dict()


def create_Route_target(target_loc):
    route = list()
    for loc in target_loc:
        route.append(Location(loc))
    return route


if __name__ == '__main__':
    question_loc = create_Route_target(['I', 'N', 'T', 'W', 'e'])
    Gene_algo = GeneticAlgo(question_loc, level=30, population=100, variant=3, mutate_percent=0.02,
                            elite_save_percent=0.3)
    best_route, best_route_length = Gene_algo.evolution()
    print([loc.name for loc in best_route], best_route_length)