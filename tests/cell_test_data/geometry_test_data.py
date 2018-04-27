surface_data = {
    1: ('sx', [4, 2]),
    2: ('cx', [2]),
    3: ('px', [-3]),
    4: ('sx', [-3, 1]),
    5: ('px', [4]),
    6: ('sx', [4, 1]),
    7: ('cx', [3]),
    8: ('cx', [1]),
    9: ('px', [-5]),
    10: ('px', [8]),
}

polish_geoms = [
    [2, 'C', 3, 'I', 1, 'I', 5, 'C', 'I', 4, 'C', 'U'],
    [6, 'C', 1, 'C', 'I'],
    [6, 'C', 1, 'C', 'U'],
    [6, 1, 'I', 2, 'C', 'I', 5, 'C', 'I', 3, 'I', 4, 'C', 9, 'I', 'U', 3, 'C',
     4, 'C', 'I', 'U', 7, 'C', 'I', 10, 'C', 'I', 4, 'C', 10, 'C', 'I', 'U'],
    [5, 'C', 3, 'I', 2, 'C', 'I', 1, 'C', 'U'],
    [3, 8, 'C', 'I', 5, 'C', 'I', 4, 'C', 'U', 6, 'C', 'U', 2, 'C', 'I']
]

cell_kwargs = {'U': 5, 'IMP:N': 1, 'DEN': -4.3}

create_geom = [
    ('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]),
    ('I', [('C', [6]), ('C', [1])]),
    ('U', [('C', [6]), ('C', [1])]),
    ('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])]),
    ('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])]),
    ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])
]

node_get_surfaces = [
    [2, 3, 1, 5, 4],
    [6, 1],
    [6, 1],
    [6, 1, 2, 5, 3, 4, 9, 7, 10],
    [5, 3, 2, 1],
    [3, 8, 5, 4, 6, 2]
]

node_complexity_data = [5, 2, 2, 13, 4, 6]

simple_geoms = [
    [2, 'C', 3, 'I', 1, 'I', 5, 'C', 'I', 4, 'C', 'U'],
    [6, 'C'],
    [1, 'C'],
    [2, 'C', 3, 'I', 1, 'I', 5, 'C', 'I', 4, 'C', 'U'],
    [5, 'C', 3, 'I', 2, 'C', 'I', 1, 'C', 'U'],
    [3, 8, 'C', 'I', 5, 'C', 'I', 4, 'C', 'U', 6, 'C', 'U']
]

complement_geom = [
    ('I', [('U', [('S', [2]), ('C', [3]), ('C', [1]), ('S', [5])]), ('S', [4])]),
    ('U', [('S', [6]), ('S', [1])]),
    ('I', [('S', [6]), ('S', [1])]),
    ('I', [('U', [('S', [4]), ('S', [10])]), ('U', [('S', [7]), ('S', [10]), ('I', [('U', [('S', [3]), ('S', [4])]), ('U', [('S', [4]), ('C', [9])]), ('U', [('C', [6]), ('C', [1]), ('S', [2]), ('S', [5]), ('C', [3])])])])]),
    ('I', [('S', [1]), ('U', [('S', [5]), ('C', [3]), ('S', [2])])]),
    ('U', [('S', [2]), ('I', [('S', [6]), ('S', [4]), ('U', [('C', [3]), ('S', [8]), ('S', [5])])])])
]

intersection_geom = [
    [
        ('I', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('I', [('C', [6]), ('C', [1])])]),
        ('I', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('U', [('C', [6]), ('C', [1])])]),
        ('I', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])])]),
        ('I', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])])]),
        ('I', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])])
    ],
    [
        ('I', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('I', [('C', [6]), ('C', [1])])]),
        ('I', [('I', [('C', [6]), ('C', [1])]), ('U', [('C', [6]), ('C', [1])])]),
        ('I', [('I', [('C', [6]), ('C', [1])]), ('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])])]),
        ('I', [('I', [('C', [6]), ('C', [1])]), ('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])])]),
        ('I', [('I', [('C', [6]), ('C', [1])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])])
    ],
    [
        ('I', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('U', [('C', [6]), ('C', [1])])]),
        ('I', [('I', [('C', [6]), ('C', [1])]), ('U', [('C', [6]), ('C', [1])])]),
        ('I', [('U', [('C', [6]), ('C', [1])]), ('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])])]),
        ('I', [('U', [('C', [6]), ('C', [1])]), ('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])])]),
        ('I', [('U', [('C', [6]), ('C', [1])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])])
    ],
    [
        ('I', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])])]),
        ('I', [('I', [('C', [6]), ('C', [1])]), ('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])])]),
        ('I', [('U', [('C', [6]), ('C', [1])]), ('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])])]),
        ('I', [('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])]), ('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])])]),
        ('I', [('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])])
    ],
    [
        ('I', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])])]),
        ('I', [('I', [('C', [6]), ('C', [1])]), ('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])])]),
        ('I', [('U', [('C', [6]), ('C', [1])]), ('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])])]),
        ('I', [('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])]), ('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])])]),
        ('I', [('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])])
    ],
    [
        ('I', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])]),
        ('I', [('I', [('C', [6]), ('C', [1])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])]),
        ('I', [('U', [('C', [6]), ('C', [1])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])]),
        ('I', [('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])]),
        ('I', [('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])])
    ]
]

union_geom = [
    [
        ('U', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('I', [('C', [6]), ('C', [1])])]),
        ('U', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('U', [('C', [6]), ('C', [1])])]),
        ('U', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])])]),
        ('U', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])])]),
        ('U', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])])
    ],
    [
        ('U', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('I', [('C', [6]), ('C', [1])])]),
        ('U', [('I', [('C', [6]), ('C', [1])]), ('U', [('C', [6]), ('C', [1])])]),
        ('U', [('I', [('C', [6]), ('C', [1])]), ('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])])]),
        ('U', [('I', [('C', [6]), ('C', [1])]), ('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])])]),
        ('U', [('I', [('C', [6]), ('C', [1])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])])
    ],
    [
        ('U', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('U', [('C', [6]), ('C', [1])])]),
        ('U', [('I', [('C', [6]), ('C', [1])]), ('U', [('C', [6]), ('C', [1])])]),
        ('U', [('U', [('C', [6]), ('C', [1])]), ('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])])]),
        ('U', [('U', [('C', [6]), ('C', [1])]), ('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])])]),
        ('U', [('U', [('C', [6]), ('C', [1])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])])
    ],
    [
        ('U', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])])]),
        ('U', [('I', [('C', [6]), ('C', [1])]), ('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])])]),
        ('U', [('U', [('C', [6]), ('C', [1])]), ('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])])]),
        ('U', [('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])]), ('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])])]),
        ('U', [('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])])
    ],
    [
        ('U', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])])]),
        ('U', [('I', [('C', [6]), ('C', [1])]), ('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])])]),
        ('U', [('U', [('C', [6]), ('C', [1])]), ('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])])]),
        ('U', [('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])]), ('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])])]),
        ('U', [('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])])
    ],
    [
        ('U', [('U', [('I', [('C', [2]), ('S', [3]), ('S', [1]), ('C', [5])]), ('C', [4])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])]),
        ('U', [('I', [('C', [6]), ('C', [1])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])]),
        ('U', [('U', [('C', [6]), ('C', [1])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])]),
        ('U', [('U', [('I', [('C', [4]), ('C', [10])]), ('I', [('C', [7]), ('C', [10]), ('U', [('I', [('C', [3]), ('C', [4])]), ('I', [('C', [4]), ('S', [9])]), ('I', [('S', [6]), ('S', [1]), ('C', [2]), ('C', [5]), ('S', [3])])])])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])]),
        ('U', [('U', [('C', [1]), ('I', [('C', [5]), ('S', [3]), ('C', [2])])]), ('I', [('C', [2]), ('U', [('C', [6]), ('C', [4]), ('I', [('S', [3]), ('C', [8]), ('C', [5])])])])])
    ]
]

node_points = [
    [-6, 0, 0], [-3.5, 0, 0], [-3.5, 1.5, 0], [-2.5, 1.5, 0], [-1, 2.5, 0], [1, -1.5, 0], [1, -0.5, 0], [2.5, 0.5, 0],
    [4, -0.5, 0], [5.5, 0.5, 0], [7, -0.5, 0]
]

node_test_point_ans = [
    [-1, +1, -1, +1, -1, +1, +1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, +1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, +1, +1, +1, -1],
    [-1, +1, -1, +1, -1, +1, +1, -1, -1, -1, -1],
    [-1, -1, -1, +1, -1, +1, +1, +1, +1, +1, -1],
    [-1, +1, -1, -1, -1, -1, +1, +1, +1, -1, -1]
]

node_boxes_data = [
    {'base': [0, 0, 0], 'xdim': 2.5, 'ydim': 3.5, 'zdim': 3},
    {'base': [-2, 0, 0], 'xdim': -2.5, 'ydim': -3, 'zdim': 3},
    {'base': [4.5, 0, 0], 'xdim': 2, 'ydim': -1.5, 'zdim': 1.5}
]

node_box_ans = [
    [
        (0, [('U', [('I', [('C', [2]), ('S', [1])])])]),
        (-1, [('I', [('C', [6])])]),
        (0, [('U', [('C', [1])])]),
        (0, [('U', [('I', [('C', [7]), ('U', [('I', [('S', [1]), ('C', [2])])])])])]),
        (0, [('U', [('C', [1]), ('I', [('C', [2])])])]),
        (0, [('I', [('C', [2]), ('U', [('I', [('C', [8])])])])])
    ],
    [
        (0, [('U', [('I', [('C', [2]), ('S', [3])]), ('C', [4])])]),
        (-1, [('I', [('C', [6])]), ('I', [('C', [1])])]),
        (-1, [('U', [('C', [6]), ('C', [1])])]),
        (0, [('U', [('I', [('C', [4])]), ('I', [('C', [7]), ('U', [('I', [('C', [4]), ('C', [3])]), ('I', [('C', [4])]), ('I', [('S', [3]), ('C', [2])])])])])]),
        (0, [('U', [('I', [('C', [2]), ('S', [3])])])]),
        (0, [('I', [('C', [2]), ('U', [('C', [4]), ('I', [('C', [8]), ('S', [3])])])])])
    ],
    [
        (-1, [('U', [('C', [4]), ('I', [('C', [5])])])]),
        (0, [('I', [('C', [6]), ('C', [1])])]),
        (0, [('U', [('C', [6]), ('C', [1])])]),
        (-1, [('U', [('I', [('C', [4])]), ('I', [('U', [('I', [('C', [4])]), ('I', [('C', [4])]), ('I', [('C', [5])])])])]),
              ('U', [('I', [('C', [4])]), ('I', [('U', [('I', [('C', [3])]), ('I', [('C', [4])]), ('I', [('C', [5])])])])])]),
        (0, [('U', [('C', [1])])]),
        (0, [('I', [('C', [2]), ('U', [('C', [6])])])])
    ]
]

node_bounding_box = [
    [[-4, 4], [-2, 2], [-2, 2]],
    [[3, 5], [-1, 1], [-1, 1]],
    [[2, 6], [-2, 2], [-2, 2]],
    [[-4, 4], [-2, 2], [-2, 2]],
    [[-3, 6], [-2, 2], [-2, 2]],
    [[-4, 5], [-1, 1], [-1, 1]]
]

node_volume = [
    [7.4940, 0, 0.35997, 7.4940, 7.8540, 1.9635],
    [3.6652, 0, 0, 3.6652, 3.1416, 1.30900],
    [0, 0.1636, 2.3544, 0, 2.3544, 0.1636]
]

cell_complement_cases = [
    (0, 0), (-1, +1), (+1, -1), ([-1, 0, 1], [1, 0, -1])
]

cell_intersection_cases = [
    (-1, -1, -1), (-1, 0, -1), (-1, 1, -1), (0, -1, -1), (0, 0, 0), (0, 1, 0),
    (1, -1, -1), (1, 0, 0), (1, 1, 1),
    ([-1, -1, -1, 0, 0, 0, 1, 1, 1],
     [-1, 0, 1, -1, 0, 1, -1, 0, 1], [-1, -1, -1, -1, 0, 0, -1, 0, 1])
]

cell_union_cases = [
    (-1, -1, -1), (-1, 0, 0), (-1, 1, 1), (0, -1, 0), (0, 0, 0), (0, 1, 1),
    (1, -1, 1), (1, 0, 1), (1, 1, 1),
    ([-1, -1, -1, 0, 0, 0, 1, 1, 1],
     [-1, 0, 1, -1, 0, 1, -1, 0, 1], [-1, 0, 1, 0, 0, 1, 1, 1, 1])
]
