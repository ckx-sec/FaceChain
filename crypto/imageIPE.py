import random
import numpy as np
import math
import csv
import os
def noisyCount(sensitivety, epsilon,u1,u2):
    beta = sensitivety/epsilon
    
    if u1 <= 0.5:
        n_value = -beta*np.log(1.-u2)
    else:
        n_value = beta*np.log(u2)
    # print(n_value)
    return n_value

def laplace_mech(data,u1,u2,sensitivety=1, epsilon=4):
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] += noisyCount(sensitivety, epsilon,u1,u2)
    return data

def keyGenerate(z,msk):
    """
    Compute sk
    """
    print(f'msk: {len(msk)}, z: {len(z)}')
    s = np.array(msk)
    z = np.array(z)
    sk = list(np.matmul(s, z))
    return sk

def encrypt(w,mpk,g=1.0001):
    ct0 = []
    ctx = []
    for i in range(18):
        r = random.random()
        ct0.append(pow(g, r))
        ctx.append([pow(mpk[j], r)*pow(g, w[i][j])
                    for j in range(512)])
    return ct0, ctx

def decrypt(ct0,ctx,sk, z):
    a = []
    val = 1
    for i in range(18):
        b = []
        for j in range(512):
            fenzi = 1
            fenmu = 1
            val = 1
            for k in range(512):
                fenzi *= pow(ctx[i][k], z[j][k])
            fenmu = pow(ct0[i], sk[i])
            #val *= fenzi/fenmu
            # print(val)
            b.append(fenzi/fenmu)
        a.append(b)
    return a
