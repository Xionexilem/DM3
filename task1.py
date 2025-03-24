import turtle
import pandas as pd

ALPHABET = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '

class Node:
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

def create_parent_for_children(children):
    parent = Node(sum(child.value for child in children))
    for child in children:
        child.parent = parent
        parent.add_child(child)
    return parent

def generate_prefix_codes(node, prefix='', codes=None):
    if codes is None:
        codes = {}

    if not node.children:
        codes[prefix] = node.value
        return codes

    for index, child in enumerate(node.children):
        generate_prefix_codes(child, prefix + str(index), codes)

    return codes

def draw_tree(t, node, x, y, dx, cof):
    if node is None:
        return

    t.penup()
    t.goto(x, y)
    t.pendown()
    t.dot(5, "black")
    t.write(round(node.value, 2), align="center", font=("Arial", 7, "bold"))

    for index, child in enumerate(node.children):
        new_x = x + (index - len(node.children) / (cof + cof % 4)) * dx
        new_y = y - 50
        t.penup()
        t.goto(x, y)
        t.pendown()
        t.goto(new_x, new_y)
        draw_tree(t, child, new_x, new_y, dx / cof, cof)

def calculation_rates(text, alphabet):
    len_text = len(text)
    count_symbols = {symbol: text.count(symbol) for symbol in alphabet}
    rates = {symbol: count / len_text for symbol, count in count_symbols.items()}
    return rates

def encode_Huffman(rates, q, to_save):
    old_rates = rates
    rates = sorted(rates.values())
    rates = [Node(rate) for rate in rates]
    to_save = f"{to_save}.csv"

    q2 = (len(rates) - 1) % (q - 1) if len(rates) > 2 else 0
    q2 = q if q2 == 1 else q - 1 if q2 == 0 else q2

    while len(rates) > 1:
        children_nodes = rates[:q]
        rates = rates[q:]
        new_node = create_parent_for_children(children_nodes)
        rates.append(new_node)
        rates.sort(key=lambda rate: rate.value)

    screen = turtle.Screen()
    t = turtle.Turtle()
    t.speed(0)

    prefix_codes = generate_prefix_codes(rates[0])

    codes_with_symbols = {}

    old_rates = sorted(old_rates.items(), key=lambda item: item[1], reverse=True)
    prefix_codes = sorted(prefix_codes.items(), key=lambda item: item[1], reverse=True)
    print(f"{"Символ:":<8} Код")
    for i in range(len(old_rates)):
        codes_with_symbols[old_rates[i][0]] = prefix_codes[i][0]
        print(f"{old_rates[i][0]:^8} {prefix_codes[i][0]}")
    df = pd.DataFrame(codes_with_symbols.items(), columns=["Символ", "Код"])
    df.to_csv(to_save, index=False, encoding='utf-8')

    screen.clear()

def redundancy(file_codes, rates):
    with open(file_codes, encoding='utf-8') as file:
        file.readline()
        task7 = file.readlines()
        task7 = [i.rstrip().split(',') for i in task7]
        return round(sum([rates[i[0]] * len(i[1]) for i in task7]), 2)

with open('text02.txt', 'r', encoding='utf-8') as file:
    text = file.readline()

rate_symbols = calculation_rates(text, ALPHABET)

encode_Huffman(rate_symbols, 2, 'task7_a')
encode_Huffman(rate_symbols, 4, 'task7_b')

print('Избыточность а:', redundancy('task7_a.csv', rate_symbols))
print('Избыточность б:', redundancy('task7_b.csv', rate_symbols))
