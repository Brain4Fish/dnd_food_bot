import prettytable as pt

def form_table(columns, data):
    table = pt.PrettyTable(columns)
    for row in data:
        table.add_row(row)
    return table
