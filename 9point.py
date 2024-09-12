import lib
def isValid9Point(points: list[tuple[float, float]], center:tuple[float, float]) -> bool:
    lines: set[tuple[tuple[float, float], tuple[float, float]]] = set()
    for point in points:
        for other in points:
            if not other is point:
                if not (other, point) in lines:
                    lines.add((point, other))
    print(len(lines))
    intersections: dict[tuple[float, float] | None, list] = {}
    for line in lines:
        for line2 in lines:
            if not line is line2:
                c: tuple[float, float] | None = lib.linesColliding(line, line2)
                if c is not None:
                    c = (c[0].__round__(5), c[1].__round__(5))
                    if not c in line and not c in line2:
                        old = intersections.get(c, [])
                        if not (line2, line) in old:
                            old.append((line, line2))
                            intersections.update({c: old})
                    else:
                        intersections.update({None: [intersections.get(None, [0])[0]+1]})

    print({i:len(n) for (i, n) in intersections.items() if len(n)>2})
    return False

valid = [(2, 0), (.5, 3), (2.5, 3), (.10811, .64865), (3.2, 1.6), (1, 0), (1, 3.25), (.5, .25), (2.5, .25)]
print(valid, " is valid? ", isValid9Point(valid, (1.5, 1.625)))
# col = lib.linesColliding(((0.10811, 0.64865), (2.5, 0.25)), ((3.2, 1.6), (0.5, 0.25)))
col = lib.linesColliding(((0, 1), (40, 1)), ((2, 2), (2, 0)))
if col is not None:
    print("test: ", (col[0].__round__(5), col[1].__round__(5)))
else:
    print("no collision")
