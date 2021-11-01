import numpy
import requests
import grequests
import time

BLOCK_SIZE = 1000
TOTAL_BLOCKS = 20
MATRIX_SIZE = BLOCK_SIZE * TOTAL_BLOCKS

blocks = []
for i in range(TOTAL_BLOCKS):
    current_matrix = numpy.arange(0, BLOCK_SIZE ** 2, 1).reshape((BLOCK_SIZE, BLOCK_SIZE))
    blocks.append((i + 1) * current_matrix)
vector = numpy.arange(0, MATRIX_SIZE, 1)

matrix = numpy.zeros((MATRIX_SIZE, MATRIX_SIZE))
for i in range(len(blocks)):
    matrix[i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE, i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE] = blocks[i]

print('Classical multiplication')
start_time = time.time()
res1 = numpy.matmul(matrix, vector)
print('Work time: ' + str(time.time() - start_time))

matrix = None


def network_mul(url):
    global start_time
    print('Network multiplication for url: ' + url)
    start_time = time.time()
    res = []
    actions = []
    for index, block in enumerate(blocks):
        vector_part = vector[index * BLOCK_SIZE:(index + 1) * BLOCK_SIZE]
        data = {'matrix': block.tolist(), 'vector': vector_part.tolist()}
        actions.append(grequests.post(url, json=data))
    responses = grequests.map(actions)
    for response in responses:
        res.extend(response.json()['res'])
    print('Work time: ' + str(time.time() - start_time))
    delta = numpy.abs(res1 - numpy.array(res))
    if numpy.all(delta == 0):
        print('Correct')
    else:
        print('Incorrect!')
        index = numpy.where(delta != 0)
        print(index)


print('---------------------')
network_mul('http://51.159.8.213:5000')
print('-----------------------')
network_mul('http://127.0.0.1:5000')
