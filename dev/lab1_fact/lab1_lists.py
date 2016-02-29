#Derek McMahon
#dmm7aj
#CS3240
#lab1_lists

def maxmin(l):
    max = None
    min = None
    for x in range(0, len(l)):
        if max == None or l[x] > max:
            max = l[x]
        if min == None or l[x] < min:
            min = l[x]
    if not(max == min == None):
        tup = (max, min)
        return tup


def common_items(list1, list2):
    common = []
    for x in range(0, len(list1)):
        for y in range(0, len(list2)):
            if list1[x] == list2[y]:
                duplicate = False
                for z in range (0, len(common)):
                    if common[z] == list1[x]:
                        duplicate = True
                if not duplicate:
                    common.append(list1[x])
    return common


def test_listfuncts():
    l1 = [1, 3, 3]
    l2 = [3, 1, -2]
    l3 = ['Q', 'Z', 'C', 'A']

    assert (3, 1) == maxmin(l1), "maxmin(l1) did not yield (3, 1)"
    assert (3, -2) == maxmin(l2), "maxmin(l2) did not yield (3, -2)"
    assert ('Z', 'A') == maxmin(l3), "maxmin(l3) did not yield ('Z', 'A')"
    assert [1,3] == common_items(l1, l2), "common_items(l1,l2) did not yield [1, 3]"
    assert [] == common_items(l1, l3), "common_items(l1,l3) did not yield []"



if __name__ == "__main__":
    test_listfuncts()
