class FindNeighbours:
    def __init__(self, boardRowsList):
        self.neighbours = []
        self.boardRowsList = boardRowsList

    def test_edge(self, boardRow, r, index, i):
        try:
            br = boardRow + r
            ind = index + i
            if (0 <= br <= len(self.boardRowsList) - 1) and (0 <= ind <= len(self.boardRowsList[br]) - 1):
                val = list([br, ind])
                if val not in self.neighbours and self.boardRowsList[br][ind] != '*':
                    self.neighbours.append(val)
                else:
                    pass
            else:
                pass
        except IndexError:
            pass

    def test_neighbouring_edges(self, boardRow, edgeIndex):
        #Horizontal edges
        if boardRow % 2 == 0:
            temp = edgeIndex * 2
            if boardRow == 0:
                self.test_edge(boardRow, 1, temp, 0)
                self.test_edge(boardRow, 1, temp, 1)
                self.test_edge(boardRow, 1, temp, 2)
                self.test_edge(boardRow, 1, temp, 3)

                self.test_edge(boardRow, 0, edgeIndex, -1)
                self.test_edge(boardRow, 0, edgeIndex, 1)

            elif boardRow == len(self.boardRowsList) - 1:
                self.test_edge(boardRow, -1, temp, -1)
                self.test_edge(boardRow, -1, temp, 0)
                self.test_edge(boardRow, -1, temp, 1)
                self.test_edge(boardRow, -1, temp, 2)

                self.test_edge(boardRow, 0, edgeIndex, -1)
                self.test_edge(boardRow, 0, edgeIndex, 1)

            elif boardRow == 4 or boardRow == 8 or boardRow == 12 or boardRow == 16 or boardRow == 20 or boardRow == 24:
                self.test_edge(boardRow, -1, temp, 0)
                self.test_edge(boardRow, -1, temp, 1)
                self.test_edge(boardRow, -1, temp, 2)
                self.test_edge(boardRow, -1, temp, 3)

                self.test_edge(boardRow, 1, temp, 0)
                self.test_edge(boardRow, 1, temp, 1)
                self.test_edge(boardRow, 1, temp, 2)
                self.test_edge(boardRow, 1, temp, 3)

                self.test_edge(boardRow, 0, edgeIndex, 1)
                self.test_edge(boardRow, 0, edgeIndex, -1)
            else:
                self.test_edge(boardRow, -1, temp, -1)
                self.test_edge(boardRow, -1, temp, 0)
                self.test_edge(boardRow, -1, temp, 1)
                self.test_edge(boardRow, -1, temp, 2)

                self.test_edge(boardRow, 1, temp, -1)
                self.test_edge(boardRow, 1, temp, 0)
                self.test_edge(boardRow, 1, temp, 1)
                self.test_edge(boardRow, 1, temp, 2)

                self.test_edge(boardRow, 0, edgeIndex, 1)
                self.test_edge(boardRow, 0, edgeIndex, -1)
        #Diagonal edges
        elif boardRow % 2 != 0:
            temp = -(-edgeIndex // 2)
            if boardRow == 1 or boardRow == 5 or boardRow == 9 or \
                    boardRow == 13 or boardRow == 17 or boardRow == 21 or boardRow == 25:
                #Odd numbers
                if edgeIndex % 2 != 0:
                    self.test_edge(boardRow, -1, temp, -2)
                    self.test_edge(boardRow, -1, temp, -1)

                    self.test_edge(boardRow, -2, edgeIndex, -1)
                    self.test_edge(boardRow, -2, edgeIndex, 0)

                    self.test_edge(boardRow, 1, temp, -1)
                    self.test_edge(boardRow, 1, temp, 0)

                    self.test_edge(boardRow, 2, edgeIndex, 0)
                    self.test_edge(boardRow, 2, edgeIndex, 1)

                    self.test_edge(boardRow, 0, edgeIndex, -1)
                    self.test_edge(boardRow, 0, edgeIndex, 1)
                #Even numbers
                elif edgeIndex % 2 == 0:
                    self.test_edge(boardRow, -1, temp, -1)
                    self.test_edge(boardRow, -1, temp, 0)

                    self.test_edge(boardRow, -2, edgeIndex, 0)
                    self.test_edge(boardRow, -2, edgeIndex, 1)

                    self.test_edge(boardRow, 1, temp, -1)
                    self.test_edge(boardRow, 1, temp, 0)

                    self.test_edge(boardRow, 2, edgeIndex, -1)
                    self.test_edge(boardRow, 2, edgeIndex, 0)

                    self.test_edge(boardRow, 0, edgeIndex, 1)
                    self.test_edge(boardRow, 0, edgeIndex, -1)
            if boardRow == 3 or boardRow == 7 or boardRow == 11 or \
                    boardRow == 15 or boardRow == 19 or boardRow == 23:
                # Odd numbers
                if edgeIndex % 2 != 0:
                    self.test_edge(boardRow, -1, temp, -1)
                    self.test_edge(boardRow, -1, temp, 0)

                    self.test_edge(boardRow, -2, edgeIndex, 0)
                    self.test_edge(boardRow, -2, edgeIndex, 1)

                    self.test_edge(boardRow, 1, temp, -2)
                    self.test_edge(boardRow, 1, temp, -1)

                    self.test_edge(boardRow, 2, edgeIndex, -1)
                    self.test_edge(boardRow, 2, edgeIndex, 0)

                    self.test_edge(boardRow, 0, edgeIndex, 1)
                    self.test_edge(boardRow, 0, edgeIndex, -1)
                #Even numbers
                elif edgeIndex % 2 == 0:
                    self.test_edge(boardRow, -1, temp, -1)
                    self.test_edge(boardRow, -1, temp, 0)

                    self.test_edge(boardRow, -2, edgeIndex, -1)
                    self.test_edge(boardRow, -2, edgeIndex, 0)

                    self.test_edge(boardRow, 1, temp, -1)
                    self.test_edge(boardRow, 1, temp, 0)

                    self.test_edge(boardRow, 2, edgeIndex, 0)
                    self.test_edge(boardRow, 2, edgeIndex, 1)

                    self.test_edge(boardRow, 0, edgeIndex, -1)
                    self.test_edge(boardRow, 0, edgeIndex, 1)







