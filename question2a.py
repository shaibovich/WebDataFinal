def load_data(filename):
    with open(filename) as f:
        data = f.readlines()

    ranks = {}
    order = []
    for lines in data:
        params = lines.split(',')
        name = params[0]
        score = params[1]
        ranks[name] = float(score)
        order.append(name)
    return [ranks, order]


def validate_index(variable, data):
    if variable not in data:
        lst = data.values()
        data[variable] = sum(lst)/len(lst)



def fagin_alt(data1, data2, data3, k):
    ranks1 = data1[0]
    order1 = data1[1]
    seen1 = {}

    ranks2 = data2[0]
    order2 = data2[1]
    seen2 = {}

    ranks3 = data3[0]
    order3 = data3[1]
    seen3 = {}

    seen_all = {}
    ranks_agg = {}
    i = 0

    stop = 0
    while stop != 1:
        validate_index(order1[i],ranks2)
        validate_index(order1[i],ranks3)
        ranks_agg[order1[i]] = max(ranks1[order1[i]], ranks2[order1[i]], ranks3[order1[i]])
        seen1[order1[i]] = 1
        if order1[i] in seen2 and order1[i] in seen3:
            seen_all[order1[i]] = ranks_agg[order1[i]]

        validate_index(order2[i],ranks1)
        validate_index(order2[i],ranks3)
        ranks_agg[order2[i]] = max(ranks1[order2[i]], ranks2[order2[i]], ranks3[order2[i]])
        seen2[order2[i]] = 1
        if order2[i] in seen1 and order2[i] in seen3:
            seen_all[order2[i]] = ranks_agg[order2[i]]

        validate_index(order3[i],ranks1)
        validate_index(order3[i],ranks2)
        ranks_agg[order3[i]] = max(ranks1[order3[i]], ranks2[order3[i]], ranks3[order3[i]])
        seen3[order3[i]] = 1
        if order3[i] in seen1 and order3[i] in seen2:
            seen_all[order3[i]] = ranks_agg[order3[i]]

        if len(seen_all) >= k:
            stop = 1
        i = i + 1

    print("Ranked: " + str(ranks_agg))
    print("Seen all: " + str(seen_all))
    print("Actions: " + str(i * 2) + "\n")
    return sorted(ranks_agg.items(), key=lambda x: x[1], reverse=True)[0:k]


data1 = load_data("./data1.csv")
data2 = load_data("./data2.csv")
data3 = load_data("./data3.csv")

print(fagin_alt(data1, data2, data3,1))
print(fagin_alt(data1, data2, data3,2))
print(fagin_alt(data1, data2, data3,3))
