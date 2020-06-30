# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/6/29
# @Author  : Yingke Ding
# @File    : query_binary_tree.py
# @Software: PyCharm
from bitarray import bitarray  # please run command: pip install bitarray


def _process_print(algorithm_results, id_length):
    print("---------------------------------------")
    print("Step No.  |  Query     |  Response")
    step_no = 0
    result_format = "%-" + str(id_length + 5) + "s"
    for result in algorithm_results:
        print("%-10s" % str(step_no) + "|  " + result_format % result['Query'] + "| " + result['Response'])
        step_no += 1


def judge_status(query, ids_list):
    """
    Match all ids with the specific query.
    :param query: a bitarray of 01 list.
    :param ids_list: list of bitarrays of tag ids
    :return: the hit target ids if matches, or zero length list if not match.
    """
    hits = []
    for binary_id in ids_list:
        if query == binary_id[0: query.length()]:
            hits.append(binary_id)

    return hits


class Algorithm:
    """
    In this algorithm, I use bitwise operations to replace stack.
    A stack pop is equal to a binary query right shift,
    a stack push 0 is equal to a binary query left shift,
    and a stack push 1 is equal to a binary query left shift and then add 1.

    This kind of operations is faster than using character-wise operations for stack.
    """
    def __init__(self, _tag_ids):
        """
        Constructor.
        :param _tag_ids: list of bitarrays of tag ids
        """
        self.tag_ids = _tag_ids
        self.results = []  # save query and response results in a list of dict

        self._algorithm()

    def _algorithm(self):
        binary_query = bitarray('0')

        hit_count = 0  # used for flag of end loop
        while True:
            hits = judge_status(binary_query, self.tag_ids)

            if len(hits) == 0:
                # IDLE
                self.results.append({"Query": binary_query.to01(), "Response": "Idle"})

                while binary_query[-1]:
                    del binary_query[-1]  # pop
                binary_query[-1] = 1  # 0 to 1 is just like pop 0 and push 1

            elif len(hits) == 1:
                # HIT
                self.results.append({"Query": binary_query.to01(), "Response": hits[0].to01()})
                hit_count += 1
                if hit_count == len(self.tag_ids):
                    break

                if not binary_query[-1]:
                    binary_query[-1] = 1  # pop 0 and push 1
                else:
                    while binary_query[-1]:
                        del binary_query[-1]  # pop
                    binary_query[-1] = 1

            elif len(hits) > 1:
                # COLLISION
                self.results.append({"Query": binary_query.to01(), "Response": "Collision"})

                binary_query.append(0)  # left shift

    def get_results(self):
        return self.results


if __name__ == '__main__':
    # 010,101,000,111,110,001,011
    # 11001,11111,00101,00111
    # 11010101,11111111,01000000,10101010,01010101
    string = input("Please input the id set: \n")

    tag_ids = string.split(",")
    length = len(tag_ids[0])
    tag_ids = [bitarray(tag_id) for tag_id in tag_ids]

    results = Algorithm(tag_ids).get_results()
    _process_print(results, length)
