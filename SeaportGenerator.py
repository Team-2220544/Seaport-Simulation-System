import random
import numpy as np

random.seed(1)


class SeaportGenerator():
    def __init__(self, width, length, dnode, dedge):
        self.width = width
        self.length = length
        self.dnode = dnode
        self.dedge = dedge

    def get_nodes(self, width, length, dnode):
        area = width*length
        node_num = int(area*dnode)
        node_list = [[random.randint(0, length), 0], [
            random.randint(1, length), width-1]]
        for i in range(node_num-2):
            random_point = [random.randint(
                0, length), random.randint(0, width)]
            while random_point in node_list:
                random_point = [random.randint(
                    0, length), random.randint(0, width)]
            node_list.append(random_point)
        node_list = sorted(node_list, key=lambda x: x[1])
        return node_list

    def init_matrix(self, node_list):
        dim = len(node_list)
        return np.zeros([dim, dim])

    def update_matrix(self, node_list, matrix):
        for i in range(len(node_list)-1):
            distance = abs(node_list[i][0]-node_list[i+1][0]) + \
                abs(node_list[i][1]-node_list[i+1][1])
            matrix[i][i+1] = distance
            matrix[i+1][i] = distance
        return matrix

    def add_rest_edge(self, node_list, matrix, dedge, width, length):
        n = len(node_list)
        current_num = n-1
        num_edge = int(n*(n-1)//2*dedge)
        while num_edge-current_num > 0:
            random_point = random.sample(node_list, 2)
            p = node_list.index(random_point[0])
            q = node_list.index(random_point[1])
            while matrix[p][q] > 0 and p == q:
                random_point = [random.randint(
                    0, length), random.randint(0, width)]
                p = node_list.index(random_point[0])
                q = node_list.index(random_point[1])
            distance = abs(node_list[p][0]-node_list[q][0]) + \
                abs(node_list[p][1]-node_list[q][1])
            matrix[p][q] = distance
            matrix[q][p] = distance
            current_num += 1
        return matrix

    def get_random_network(self):
        node_list = self.get_nodes(self.width, self.length, self.dnode)
        matrix = self.init_matrix(node_list)
        matrix = self.update_matrix(node_list, matrix)
        matrix = self.add_rest_edge(
            node_list, matrix, self.dedge, self.width, self.length)
        return matrix

    def get_head_to_list(self, matrix):
        dim = len(matrix)
        head_to_list = []
        for i in range(dim):
            next_list = []
            for j in range(i, dim):
                if matrix[i][j]:
                    next_list.append(j)
            head_to_list.append(next_list)
        return head_to_list


if __name__ == "__main__":
    SeaportGenerator = SeaportGenerator(100, 100, 0.001, 0.2)
    matrix = SeaportGenerator.get_random_network()
    head_to_list = SeaportGenerator.get_head_to_list(matrix)
