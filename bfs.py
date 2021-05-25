from game import FreeCell, visu_card, score, is_order, max_cnum
from collections import deque
from queue import PriorityQueue as PQ
import time


class Code_Score(object):
    def __init__(self, game, steps) -> None:
        super().__init__()
        self.fcode = game.feat_code()
        #
        #self.score = sum([
        #    len(x)**2 for x in game.queue
        #]) + steps + sum([1 if x != 0 else 0 for x in game.cells]) * 10

        self.score = steps * 3.5 + (-5 * score(game.heaps) + sum([
            is_order(x).count(False) for x in game.queue
        ]) - 2 * sum([is_order(x).count(True) for x in game.queue]))

    def __lt__(self, other):
        return self.score < other.score

    def __eq__(self, o: object) -> bool:
        return self.score == o.score

    def __ge__(self, other):
        return self.score > other.score


class FreeCellStatus(object):
    def __init__(self, game_board, parent=None) -> None:
        super().__init__()
        if parent:
            self.par_code = parent.game_board.feat_code()
            self.game_board = game_board
            self.steps = parent.steps + 1
        else:
            self.par_code = None
            self.game_board = game_board
            self.steps = 0


def traceback(s_dict, tail: FreeCellStatus) -> list:
    trace_list = []
    while tail.steps != 0:
        trace_list.append(tail.game_board)
        tail = s_dict[tail.par_code]
    return trace_list


def dfs_freecell(init_game: FreeCell) -> list:
    status_dict = {}
    undiscover_list = PQ()
    flag = False
    # add init
    init_name = init_game.feat_code()
    status_dict[init_name] = FreeCellStatus(init_game)
    undiscover_list.put(
        Code_Score(init_game, steps=status_dict[init_name].steps))
    now_depth = 1e+100
    t0 = time.time()
    # 取出一个未探索的节点
    while not (undiscover_list.empty() or flag):
        now = undiscover_list.get()
        now_game_id, now_game_score = now.fcode, now.score

        if now_depth != now_game_score:
            print("best_score_now:", now.score, ";steps:,",
                  status_dict[now_game_id].steps,
                  "time:%.4fs" % (time.time() - t0), "; length=",
                  len(undiscover_list.queue))
            print(status_dict[now_game_id].game_board)

            t0 = time.time()
            now_depth = now_game_score

        next_game_list = status_dict[
            now_game_id].game_board.all_possible_step()
        for next_game in next_game_list:
            if next_game.is_finished():
                flag = True
                return traceback(status_dict,
                                 FreeCellStatus(
                                     game_board=next_game,
                                     parent=status_dict[now_game_id]))
            else:
                next_feat_code = next_game.feat_code()
                if not next_feat_code in status_dict:
                    status_dict[next_feat_code] = FreeCellStatus(
                        game_board=next_game, parent=status_dict[now_game_id])
                    undiscover_list.put(
                        Code_Score(
                            next_game,
                            steps=status_dict[next_feat_code].steps))
    # 没搜索到
    return []


# a game with best moves of 83.
game_25003 = FreeCell(
    queue=[[21, 18, 3, 22, 2, 7, 14], [30, 49, 37, 17, 27, 48, 28],
           [29, 38, 6, 36, 12, 19, 26], [51, 43, 39, 44, 11, 45, 15],
           [25, 4, 40, 41, 42, 1], [9, 34, 33, 31, 23, 47],
           [16, 8, 52, 32, 24, 13], [10, 5, 20, 46, 35, 50]])
game_25002 = FreeCell(
    queue=[[2, 24, 20, 43, 31, 7, 49], [19, 8, 9, 33, 34, 3, 44],
           [36, 1, 25, 18, 14, 6, 41], [48, 39, 42, 16, 13, 47, 40],
           [45, 4, 22, 35, 23, 28], [30, 27, 37, 51, 11, 52],
           [32, 46, 21, 5, 50, 15], [38, 26, 10, 29, 17, 12]])

game_3243 = FreeCell(
    queue=[[11, 8, 12, 42, 18, 47, 27], [51, 34, 31, 37, 1, 9, 45],
           [10, 38, 15, 52, 35, 28, 21], [40, 3, 23, 33, 39, 36, 46],
           [22, 29, 25, 44, 7, 48], [24, 4, 30, 19, 16, 41],
           [26, 2, 5, 14, 49, 17], [43, 50, 13, 32, 6, 20]])

random_start = FreeCell()
random_start.new_game()
print(game_25002)
solution = dfs_freecell(game_3243)
print("Solved: Steps:", solution)
print("Best Moves:", len(solution))
