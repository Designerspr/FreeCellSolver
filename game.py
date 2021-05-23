# rules
# cards:[1,52]
# 0 for empty
import random
import copy

max_cnum = 13

card_symbol = ['♠', '♥', '♣', '♦']
visu_card = lambda cid: card_symbol[(cid - 1) // max_cnum] + str((cid - 1) % max_cnum + 1)
score = lambda heaps: sum(heaps) - 6 * max_cnum
fmt_str_card = lambda x: "%02d" % x

# complex version
#complex_card = ['J','Q','K']
#visu_card_cmp = lambda cid: card_symbol[(cid - 1) // max_cnum] + (str(cid%max_cnum) if (cid-1)%max_cnum<10 else ['J','Q','K'][(cid-1)%max_cnum%10])


def is_order_single(x, y):
    x, y = x - 1, y - 1
    return True if ((x // max_cnum + y // max_cnum) % 2
                    and (x % max_cnum == y % max_cnum + 1)) else False


def is_order(x):
    #print(list(map(visu_card, x)))
    bet_order = [is_order_single(u, d)
                 for (u, d) in zip(x[:-1], x[1:])] + [True]
    for i in reversed(range(len(bet_order) - 1)):
        bet_order[i] = bet_order[i] and bet_order[i + 1]
    #print(bet_order)
    return bet_order


class FreeCell(object):
    card_num = [7, 7, 7, 7, 6, 6, 6, 6]

    def __init__(self, cells=None, heaps=None, queue=None):
        self.cells = cells if cells else [0 for i in range(4)]
        self.heaps = heaps if heaps else [i * max_cnum for i in range(4)]
        self.queue = queue if queue else [[]
                                          for i in range(len(self.card_num))]
        assert sum(self.card_num) == max_cnum * 4, "invaild sum number!"

    def new_game(self):
        self.cells = [0 for i in range(4)]
        self.heaps = [i * max_cnum for i in range(4)]
        card_seq = [x + 1 for x in range(sum(self.card_num))]
        random.shuffle(card_seq)
        self.queue = []
        for num in self.card_num:
            self.queue.append(card_seq[:num])
            card_seq = card_seq[num:]

    def __repr__(self):
        ret = "\n----FreeCell Games----\nHash Code:" + hex(
            self.__hash__()) + "\n"
        ret += "cells:" + " ".join(
            ["[%3s]" % visu_card(x) if x else "[   ]"
             for x in self.cells]) + "\n"
        ret += "heaps:" + " ".join([
            "[%3s]" % visu_card(x) if x > i * max_cnum else "[   ]"
            for (i, x) in enumerate(self.heaps)
        ]) + "\n"
        max_len = max(map(len, self.queue))
        for i in range(max_len):
            ret += " ".join([
                "[%3s]" % visu_card(x[i]) if len(x) > i else "     "
                for x in self.queue
            ]) + "\n"
        return ret

    def __cmp__(self, other):
        return score(self.heaps) - score(other)

    def all_possible_step_reg(self):
        # 检查是否有列可以向堆顶加牌
        for i, card in enumerate(self.cells):
            for j, hnum in enumerate(self.heaps):
                if card == hnum + 1:
                    new_heap = self.heaps.copy()
                    new_heap[j] += 1
                    new_cells = self.cells.copy()
                    new_cells[i] = 0
                    return ([
                        FreeCell(
                            cells=new_cells, heaps=new_heap, queue=self.queue)
                    ])
        for i, lst in enumerate(self.queue):
            if len(lst) > 0:
                for j, hnum in enumerate(self.heaps):
                    if lst[-1] == hnum + 1:
                        new_queue = copy.deepcopy(self.queue)
                        new_heap = self.heaps.copy()
                        new_queue[i].pop()
                        new_heap[j] += 1
                        return ([
                            FreeCell(
                                cells=self.cells,
                                heaps=new_heap,
                                queue=new_queue)
                        ])
        return self.all_possible_step()

    def all_possible_step(self):
        # 构建所有可能的下一步
        # 计算自由度
        fdeg = self.cells.count(0) + list(map(lambda x: len(x),
                                              self.queue)).count(0) + 1
        possible_next = []
        # 移动一张牌到Cell
        if self.cells.count(0) > 0:
            for i, lst in enumerate(self.queue):
                if len(lst) > 0:
                    new_cells = self.cells.copy()
                    new_queue = copy.deepcopy(self.queue)
                    new_cells[self.cells.index(0)] = lst[-1]
                    new_queue[i].pop()
                    possible_next.append(
                        FreeCell(
                            cells=new_cells, heaps=self.heaps,
                            queue=new_queue))
        '''
        # 检查是否有列可以向堆顶加牌
        for i, card in enumerate(self.cells):
            for j, hnum in enumerate(self.heaps):
                if card == hnum + 1:
                    new_heap = self.heaps.copy()
                    new_heap[j] += 1
                    new_cells = self.cells.copy()
                    new_cells[i] = 0
                    possible_next.append(
                        FreeCell(
                            cells=new_cells, heaps=new_heap, queue=self.queue))
        for i, lst in enumerate(self.queue):
            if len(lst) > 0:
                for j, hnum in enumerate(self.heaps):
                    if lst[-1] == hnum + 1:
                        new_queue = copy.deepcopy(self.queue)
                        new_heap = self.heaps.copy()
                        new_queue[i].pop()
                        new_heap[j] += 1
                        possible_next.append(
                            FreeCell(
                                cells=self.cells,
                                heaps=new_heap,
                                queue=new_queue))
        '''
        # 比较复杂的部分：移动逻辑判定
        possible_move = []
        target_pos = []
        # 考虑所有可以被移动的和被移入的
        for i, lst in enumerate(self.queue):
            if len(lst) > 0:
                order_lst = is_order(lst)
                for j in range(fdeg):
                    if j < len(order_lst) and order_lst[-j - 1]:
                        possible_move.append({
                            "position": (i, j),
                            "value": lst[-j - 1]
                        })
                target_pos.append(lst[-1])
            else:
                target_pos.append(-1)
        # O(n^2)逐个匹配
        for move in possible_move:
            i, j = move["position"]
            for x, target in enumerate(target_pos):
                if x != i:
                    if target == -1:
                        if j < fdeg - 1:
                            new_queue = copy.deepcopy(self.queue)
                            new_queue[x] = new_queue[i][-j - 1:]
                            new_queue[i] = new_queue[i][:-j - 1]
                            possible_next.append(
                                FreeCell(
                                    cells=self.cells,
                                    heaps=self.heaps,
                                    queue=new_queue))
                    else:
                        if is_order_single(target, move["value"]):
                            new_queue = copy.deepcopy(self.queue)
                            new_queue[x].extend(new_queue[i][-j - 1:])
                            new_queue[i] = new_queue[i][:-j - 1]
                            possible_next.append(
                                FreeCell(
                                    cells=self.cells,
                                    heaps=self.heaps,
                                    queue=new_queue))
        for i, card in enumerate(self.cells):
            if card:
                for x, target in enumerate(target_pos):
                    if target == -1 or is_order_single(target, card):
                        new_queue = copy.deepcopy(self.queue)
                        new_cells = self.cells.copy()
                        new_queue[x].append(card)
                        new_cells[i] = 0
                        possible_next.append(
                            FreeCell(
                                cells=new_cells,
                                heaps=self.heaps,
                                queue=new_queue))

        return possible_next

    def is_finished(self):
        return score(self.heaps) == 4 * max_cnum

    def feat_code(self) -> str:
        # 特征序列
        # 0-7：Cells
        # 8-15：heaps
        # else：cards.
        cell_code = "".join(map(fmt_str_card, sorted(self.cells)))
        heap_code = "".join(map(fmt_str_card, sorted(self.heaps)))
        queue_code = "00".join([
            "".join(map(fmt_str_card, x))
            for x in sorted(self.queue, key=lambda x: x[0] if x else 0)
        ])
        return cell_code + heap_code + queue_code

    def __hash__(self) -> int:
        return hash(self.feat_code())


# test code
if __name__ == '__main__':
    game_main = FreeCell()
    game_main.new_game()
    print(game_main)
    game_main.all_possible_step()
    print(game_main.is_finished())
