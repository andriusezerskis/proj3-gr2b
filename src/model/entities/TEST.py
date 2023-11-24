from human import Human

humans = [Human() for i in range(100)]

for h in humans:
    print(h.preys)