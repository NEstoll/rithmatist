# def function(var1:tuple[tuple[float, float], tuple[float, float]], var2:tuple[tuple[float, float], tuple[float, float]]) -> tuple[float, float] | None:
#     if var1 == var2:
#         return None
#     return var2[1]

# prev = None
# while True:
#     for evt in range(0, 12):
#         current = (evt/37, 4.0)
#         if prev is not None and not prev == current:
#             for i in range(2, 7):
#                 assert prev is not None
#                 temp = function((prev, current), ((0, 0), (0,0)))
#                 if temp is not None:
#                     temp2 = (temp[0]+3, temp[1]+2)
#                     current = temp2
#         prev = current