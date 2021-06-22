def mult_pair(list_o_nums, target):
    return_me = set()
    for x in list_o_nums:
        for y in list_o_nums:
            if (x * y) == target:
                return_me.add(tuple(sorted((x, y))))
    return return_me


if __name__ == "__main__":
    target = 12
    list_o_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(mult_pair(list_o_nums, target))
