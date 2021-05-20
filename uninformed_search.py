morning_cost = {'A': {'B': 15},
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
peak_cost = {'A': {'B': 19},
                'B': {'A': 19, 'C': 20},
                'C': {'B': 20, 'D': 4, 'J': 7, 'I': 10},
                'D': {'C': 4, 'E': 5, 'c': 3, 'd': 13},
                'E': {'D': 4, 'F': 38, 'W': 4, 'X': 4},
                'F': {'E': 38, 'G': 20},
                'G': {'F': 20, 'e': 10},
                'H': {'I': 10},
                'I': {'H': 10, 'C': 5},
                'J': {'C': 7, 'K': 7},
                'K': {'J': 7, 'L': 5, 'S': 5, 'T': 4},
                'L': {'M': 4, 'K': 5},
                'M': {'b': 3, 'L': 4, 'N': 4, 'U': 4},
                'N': {'O': 49, 'V': 4, 'M': 4, 'W': 5},
                'O': {'N': 49, 'P': 42},
                'P': {'O': 42},
                'Q': {'R': 32},
                'R': {'Q': 32, 'S': 25},
                'S': {'R': 25, 'K': 5},
                'T': {'U': 3, 'K': 4},
                'U': {'a': 22, 'V': 3, 'T': 3, 'M': 4},
                'V': {'U': 3, 'N': 4},
                'W': {'N': 5, 'E': 4},
                'X': {'E': 4, 'Y': 10},
                'Y': {'X': 10},
                'Z': {'a': 30},
                'a': {'Z': 30, 'U': 22},
                'b': {'M': 3, 'c': 3},
                'c': {'b': 3, 'D': 5},
                'd': {'D': 13, 'e': 13},
                'e': {'G': 10, 'd': 13}}

night_cost = {'A': {'B': 17},
                'B': {'A': 17, 'C': 18},
                'C': {'B': 18, 'D': 4, 'J': 6, 'I': 5},
                'D': {'C': 4, 'E': 5, 'c': 5, 'd': 11},
                'E': {'D': 5, 'F': 33, 'W': 4, 'X': 4},
                'F': {'E': 33, 'G': 18},
                'G': {'F': 18, 'e': 9},
                'H': {'I': 9},
                'I': {'H': 9, 'C': 5},
                'J': {'C': 6, 'K': 6},
                'K': {'J': 6, 'L': 5, 'S': 5, 'T': 4},
                'L': {'M': 4, 'K': 5},
                'M': {'b': 3, 'L': 4, 'N': 4, 'U': 4},
                'N': {'O': 43, 'V': 4, 'M': 4, 'W': 5},
                'O': {'N': 43, 'P': 37},
                'P': {'O': 37},
                'Q': {'R': 28},
                'R': {'Q': 28, 'S': 22},
                'S': {'R': 22, 'K': 5},
                'T': {'U': 3, 'K': 4},
                'U': {'a': 19, 'V': 3, 'T': 3, 'M': 4},
                'V': {'U': 3, 'N': 4},
                'W': {'N': 5, 'E': 4},
                'X': {'E': 4, 'Y': 9},
                'Y': {'X': 9},
                'Z': {'a': 27},
                'a': {'Z': 27, 'U': 19},
                'b': {'M': 3, 'c': 3},
                'c': {'b': 3, 'D': 5},
                'd': {'D': 11, 'e': 11},
                'e': {'G': 9, 'd': 11}}
cost = {'morning': morning_cost, 'peak': peak_cost, 'night': night_cost}


def check_time(start_time, now_path, frontier_dict):
    time = start_time + frontier_dict[now_path]
    if 0 <= time <= 419:
        return 'morning'
    elif 420 <= time <= 1139:
        return 'peak'
    else:
        return 'night'


def UCS(start, goal, Graph, start_time):
    frontier_list = [start]
    # 紀錄每個path的cost
    frontier_dict = {start: 0}
    time = 'morning'

    while frontier_list:
        # 從frontier中取出一個新的path
        now_path = frontier_list.pop(0)

        # 確認是否找到end
        if now_path[-1] == goal:
            return now_path, frontier_dict[now_path]

        # 擴展新的node
        for neighbor in cost[time][now_path[-1]].keys():
            new_path = now_path + neighbor
            # 確認neighbor並非走過的路徑 且 目標new_path尚未探索過
            if neighbor not in now_path and new_path not in frontier_dict.keys():
                time = check_time(start_time, now_path, frontier_dict)
                frontier_dict[new_path] = frontier_dict[now_path] + Graph[time][now_path[-1]][neighbor]
                frontier_list.append(new_path)
            else:
                continue
            frontier_list = sorted(frontier_list, key=lambda path: frontier_dict[path])
    return None


if __name__ == '__main__':
    print(UCS('F', 'S', cost, 480))