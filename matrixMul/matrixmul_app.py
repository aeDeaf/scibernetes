from flask import Flask, jsonify, request
import numpy

app = Flask("__name__")


@app.route("/", methods=['POST'])
def matrix_mul():
    data = request.json
    matrix = numpy.array(data['matrix'])
    vector = numpy.array(data['vector'])
    res = numpy.matmul(matrix, vector)
    res_list = [int(res[i]) for i in range(len(res))]
    return jsonify({'res': res_list})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
