class UnionFindOpt:
    def __init__(self, n):
        self._operations = 0
        self._calls = 0
        self.n = n
        self.parents = []
        self.weights = [1]*n
        for i in range(n):
            self.parents.append(i)

    def root(self, i):
        if self.parents[i] != i:
            self._operations += 1
            self.parents[i] = self.root(self.parents[i])
        return self.parents[i]

    def find(self, i, j):
        self._calls += 1
        return self.root(i) == self.root(j)

    def union(self, i, j):
        self._calls += 1
        root_i = self.root(i)
        root_j = self.root(j)
        if self.weights[root_i] < self.weights[root_j]:
            self.parents[root_i] = self.parents[root_j]
            self.weights[root_j] += self.weights[root_i]
        else:
            self.parents[root_j] = self.parents[root_i]
            self.weights[root_i] += self.weights[root_j]


if __name__ == '__main__':
    a = UnionFindOpt(10)
    a.union(0, 2)
    a.union(2, 3)
    print(a.parents)
    print(a.weights)
