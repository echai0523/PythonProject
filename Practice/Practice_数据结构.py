# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/7/4 14:56

input: 
output: 
Short Description: 

Change History:

"""
import copy

"""00. 按要求写出选择排序"""
i = input()
l_ = list(map(int, input().split()))
# 双重循环实现选择排序
# 循环i
for i in range(len(l_)):
    num_min = l_[i]
    index_min = i
    # 循环j
    for j in range(i, len(l_)):
        if l_[j] < num_min:
            num_min = l_[j]
            index_min = j
    # 循环j结束后，将最小值交换到它该放的位置
    l_[i], l_[index_min] = l_[index_min], l_[i]
print(l_)

"""01. 实现 list"""
class Stack:
    def __init__(self):
        self.list = list()

    def append(self, value):
        self.list.append(value)

    def pop(self, index=None):
        if len(self.list) == 0:
            return None
        else:
            if index > 0:
                return self.list.pop(index - 1)
            elif index == 0:
                return self.list.pop(index)
            else:
                return None

    def print(self):
        print(self.list)


if __name__ == '__main__':
    stack = Stack()
    stack.append(1)
    stack.append(3)
    # stack.append(6)
    print(stack.pop(2))  # None
    print(stack.pop(1))  # 3

"""02. 检查栈操作"""
class Stack:
    def __init__(self):
        self.list = list()

    def push(self, value):
        self.list.append(value)

    def pop(self, index):
        if len(self.list) == 0:
            return None
        else:
            try:
                if index:
                    self.list.pop(index-1)
                    return "yes"
                else:
                    return "yes"
            except:
                return "no"

    def print(self):
        print(self.list)


if __name__ == '__main__':
    stack = Stack()
    stack.push(1)
    print(stack.pop(1))

"""03. 二叉树的遍历"""
class BinaryTree:
    class Node:
        def __init__(self, value, left=None, right=None):
            self.value = value
            self.left = left
            self.right = right

    def __init__(self, root=None):
        self.root = root

    def lcrTravle(self, node):
        if node is not None:
            self.lcrTravle(node.right)  # 先遍历右边子树
            print(node.value, end=' ')
            self.lcrTravle(node.left)  # 先遍历左边子树


rootNode = BinaryTree.Node(5)
tree = BinaryTree(rootNode)
tree.root.left = BinaryTree.Node(3)
tree.root.right = BinaryTree.Node(7)
tree.root.left.left = BinaryTree.Node(2)
tree.root.left.left.left = BinaryTree.Node(1)
tree.root.left.right = BinaryTree.Node(4)
tree.root.right.left = BinaryTree.Node(6)
tree.root.right.right = BinaryTree.Node(8)
tree.lcrTravle(tree.root)
print()

"""04. 无向带权图"""
class Graph:
    def __init__(self, numberOfNodes):
        self.numberOfNodes = numberOfNodes
        self.matrix = [[0 for i in range(numberOfNodes+1)] for j in range(numberOfNodes+1)]
        self.du = [0] * (numberOfNodes+1)

    def addEdge(self, node1, node2):
        self.matrix[node1][node2] = 1
        self.matrix[node2][node1] = 1
        self.du[node1] += 1
        self.du[node2] += 1


graph = Graph(8)
graph.addEdge(1, 2)
graph.addEdge(1, 3)
graph.addEdge(1, 5)
graph.addEdge(2, 4)
graph.addEdge(3, 4)
graph.addEdge(3, 6)
graph.addEdge(4, 8)
graph.addEdge(5, 6)
graph.addEdge(5, 7)
graph.addEdge(6, 8)
graph.addEdge(7, 8)











