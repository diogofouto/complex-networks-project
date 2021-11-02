from math import exp

def sigmoid(x):
    return 1 / (1 + exp(-x))


def add_delta(bias, delta, bias_weight):
    d = 0.5 + delta/2 
    return bias * bias_weight + d * (1-bias_weight)