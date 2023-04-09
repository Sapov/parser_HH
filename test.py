city = map(str, input().split())
print(*[i for i in city if len(i) > 5])

