from game import FreeCell, visu_card, score
from collections import deque
from queue import PriorityQueue as PQ
import time


class Code_Score(object):
    def __init__(self, game, steps) -> None:
        super().__init__()
        self.fcode = game.feat_code()
        self.score = sum([
            len(x)**2 for x in game.queue
        ]) + steps + sum([1 if x != 0 else 0 for x in game.cells]) * 10

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
    now_depth = -1
    t0 = time.time()
    # 取出一个未探索的节点
    while not (undiscover_list.empty() or flag):
        now = undiscover_list.get()
        now_game_id, now_game_score = now.fcode, now.score

        if now_depth != now_game_score:
            print("best_score_now:",
                  score(status_dict[now_game_id].game_board.heaps), ";steps:,",
                  status_dict[now_game_id].steps,
                  "time:%.4fs" % (time.time() - t0))
            print(status_dict[now_game_id].game_board)

            t0 = time.time()
            now_depth = now_game_score

        next_game_list = status_dict[
            now_game_id].game_board.all_possible_step_reg()
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


random_start = FreeCell()
random_start.new_game()
print(random_start)
print("Solved. Best:", len(dfs_freecell(random_start)))
