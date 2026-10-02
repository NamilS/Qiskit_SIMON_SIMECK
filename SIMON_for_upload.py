from qiskit import QuantumCircuit, QuantumRegister

# Decomposition Type 1 
# (T-depth = 4, full depth = 8, total gate count = 15)
# def ccx_like(qc: QuantumCircuit, a, b, c):
#     qc.tdg(a)
#     qc.tdg(b)
#     qc.h(c)
#     qc.cx(c, a)
#     qc.t(a)
#     qc.cx(b, c)
#     qc.cx(b, a)
#     qc.t(c)
#     qc.tdg(a)
#     qc.cx(b, c)
#     qc.cx(c, a)
#     qc.t(a)
#     qc.tdg(c)
#     qc.cx(b, a)
#     qc.h(c)

# Decomposition Type 2 
# (T-depth = 3, full depth = 9, total gate count = 16)
def ccx_like(qc: QuantumCircuit, a, b, c):
    qc.h(c)
    qc.t(a)
    qc.t(b)
    qc.t(c)
    qc.cx(b, a)
    qc.cx(c, b)
    qc.cx(a, c)
    qc.tdg(b)
    qc.cx(a, b)
    qc.tdg(a)
    qc.tdg(b)
    qc.t(c)
    qc.cx(c, b)
    qc.cx(a, c)
    qc.cx(b, a)
    qc.h(c)

def apply_ccx(qc: QuantumCircuit, a, b, c, decomp: bool):
    if decomp:
        ccx_like(qc, a, b, c)
    else:
        qc.ccx(a, b, c)

def is_t_family(instr):
    return instr.operation.name in {"t", "tdg"}

def count_t_resources(qc: QuantumCircuit):
    ops = qc.count_ops()
    t_count = ops.get("t", 0) + ops.get("tdg", 0)
    t_depth = qc.depth(filter_function=is_t_family)
    return {
        "t_count": t_count,
        "t_depth": t_depth,
        "ops": ops,
    }

# =========================================================
# RC tables
# =========================================================
def get_simon_rc(state_size: int, m: int):
    if m == 4:
        if state_size == 16:   # SIMON32/64
            return [1,1,1,1,1,0,1,0,0,0,1,0,0,1,0,1,0,1,1,0,0,0,0,1,1,1,0,0,1,1,0,1,1,1,1,1,0,1,0,0,0,1,0,0,1,0,1,0,1,
                    1,0,0,0,0,1,1,1,0,0,1,1,0]
        elif state_size == 24: # SIMON48/96
            return [1,0,0,0,1,1,1,0,1,1,1,1,1,0,0,1,0,0,1,1,0,0,0,0,1,0,1,1,0,1,0,1,0,0,0,1,1,1,0,1,1,1,1,1,0,0,1,0,0,
                    1,1,0,0,0,0,1,0,1,1,0,1,0]
        elif state_size == 32: # SIMON64/128
            return [1,1,0,1,1,0,1,1,1,0,1,0,1,1,0,0,0,1,1,0,0,1,0,1,1,1,1,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,1,0,0,1,1,1,0,
                    0,1,1,0,1,0,0,0,0,1,1,1,1]
        elif state_size == 64: # SIMON128/256
            return [1,1,0,1,0,0,0,1,1,1,1,0,0,1,1,0,1,0,1,1,0,1,1,0,0,0,1,0,0,0,0,0,0,1,0,1,1,1,0,0,0,0,1,1,0,0,1,0,1,
                    0,0,1,0,0,1,1,1,0,1,1,1,1]

    elif m == 2:
        if state_size == 48:   # SIMON96/96
            return [1,0,1,0,1,1,1,1,0,1,1,1,0,0,0,0,0,0,1,1,0,1,0,0,1,0,0,1,1,0,0,0,1,0,1,0,0,0,0,1,0,0,0,1,1,1,1,1,1,
                    0,0,1,0,1,1,0,1,1,0,0,1,1]
        elif state_size == 64: # SIMON128/128
            return [1,0,1,0,1,1,1,1,0,1,1,1,0,0,0,0,0,0,1,1,0,1,0,0,1,0,0,1,1,0,0,0,1,0,1,0,0,0,0,1,0,0,0,1,1,1,1,1,1,
                    0,0,1,0,1,1,0,1,1,0,0,1,1]

    elif m == 3:
        if state_size == 24:   # SIMON48/72
            return [1,1,1,1,1,0,1,0,0,0,1,0,0,1,0,1,0,1,1,0,0,0,0,1,1,1,0,0,1,1,0,1,1,1,1,1,0,1,0,0,0,1,0,0,1,0,1,0,1,
                    1,0,0,0,0,1,1,1,0,0,1,1,0]
        elif state_size == 32: # SIMON64/96
            return [1,0,1,0,1,1,1,1,0,1,1,1,0,0,0,0,0,0,1,1,0,1,0,0,1,0,0,1,1,0,0,0,1,0,1,0,0,0,0,1,0,0,0,1,1,1,1,1,1,
                    0,0,1,0,1,1,0,1,1,0,0,1,1]
        elif state_size == 48: # SIMON96/144
            return [1,1,0,1,1,0,1,1,1,0,1,0,1,1,0,0,0,1,1,0,0,1,0,1,1,1,1,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,1,0,0,1,1,1,0,
                    0,1,1,0,1,0,0,0,0,1,1,1,1]
        elif state_size == 64: # SIMON128/192
            return [1,1,0,1,1,0,1,1,1,0,1,0,1,1,0,0,0,1,1,0,0,1,0,1,1,1,1,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,1,0,0,1,1,1,0,
                    0,1,1,0,1,0,0,0,0,1,1,1,1]

    raise ValueError(f"Unsupported RC table for state_size={state_size}, m={m}")


# =========================================================
# Round / final functions
# =========================================================
def simon4_roundfun(qc: QuantumCircuit, l, r, k0, k1, k2, k3,
                    decomp: bool, rc, ex: int):
    n = len(l)
    if n % 2 != 0:
        raise ValueError("state_size must be even.")

    for i in range(1, n, 2):
        apply_ccx(qc, l[(i - 1) % n], l[(i - 8) % n], r[i], decomp)
        qc.cx(k2[i - 1], r[i - 1])

    for i in range(0, n, 2):
        apply_ccx(qc, l[(i - 1) % n], l[(i - 8) % n], r[i], decomp)
        qc.cx(k2[i + 1], r[i + 1])

    for i in range(n):
        qc.cx(l[(i - 2) % n], r[i])
    
    for i in range(n):
        qc.cx(k1[i], k0[i])
    for i in range(n):
        qc.cx(k1[(i+1) % n], k0[i])
    for i in range(n):
        qc.cx(k3[(i+3) % n], k0[i])
    for i in range(n):
        qc.cx(k3[(i+4) % n], k0[i])
    for i in range(2, n):
        qc.x(k0[i])
    if rc[ex % 62] == 1:
        qc.x(k0[0])


def simon4_finalfun(qc: QuantumCircuit, l, r, k0, k1, k2, k3, decomp: bool):
    n = len(l)
    if n % 2 != 0:
        raise ValueError("state_size must be even.")

    for i in range(1, n, 2):
        apply_ccx(qc, l[(i - 1) % n], l[(i - 8) % n], r[i], decomp)
        qc.cx(k0[i - 1], r[i - 1])

    for i in range(0, n, 2):
        apply_ccx(qc, l[(i - 1) % n], l[(i - 8) % n], r[i], decomp)
        qc.cx(k0[i + 1], r[i + 1])

    for i in range(n):
        qc.cx(l[(i - 2) % n], r[i])


def simon2_roundfun(qc: QuantumCircuit, l, r, k0, k1,
                    decomp: bool, rc, ex: int):
    n = len(l)
    if n % 2 != 0:
        raise ValueError("state_size must be even.")

    for i in range(0, n, 2):
        apply_ccx(qc, l[(i - 1) % n], l[(i - 8) % n], r[i], decomp)
        qc.cx(k0[i+1], r[i+1])

    for i in range(1, n, 2):
        apply_ccx(qc, l[(i - 1) % n], l[(i - 8) % n], r[i], decomp)
        qc.cx(k0[i-1], r[i-1])

    for i in range(n):
        qc.cx(l[(i - 2) % n], r[i])
    
    for i in range(n):
        qc.cx(k1[(i + 3) % n], k0[i])
    for i in range(n):
        qc.cx(k1[(i + 4) % n], k0[i])
    if rc[ex % 62] == 1:
        qc.x(k0[0])
    for i in range(2, n):
        qc.x(k0[i])
    

def simon2_finalfun(qc: QuantumCircuit, l, r, k0, k1, decomp: bool):
    n = len(l)
    if n % 2 != 0:
        raise ValueError("state_size must be even.")

    for i in range(1, n, 2):
        apply_ccx(qc, l[(i - 1) % n], l[(i - 8) % n], r[i], decomp)
    for i in range(0, n, 2):
        qc.cx(k0[i], r[i])

    for i in range(0, n, 2):
        apply_ccx(qc, l[(i - 1) % n], l[(i - 8) % n], r[i], decomp)
    for i in range(1, n, 2):
        qc.cx(k0[i], r[i])

    for i in range(n):
        qc.cx(l[(i - 2) % n], r[i])


def simon3_roundfun(qc: QuantumCircuit, l, r, k0, k1, k2,
                    decomp: bool, rc, ex: int):
    n = len(l)
    if n % 2 != 0:
        raise ValueError("state_size must be even.")

    for i in range(1, n, 2):
        apply_ccx(qc, l[(i - 1) % n], l[(i - 8) % n], r[i], decomp)
    for i in range(0, n, 2):
        qc.cx(k1[i], r[i])

    for i in range(0, n, 2):
        apply_ccx(qc, l[(i - 1) % n], l[(i - 8) % n], r[i], decomp)
    for i in range(1, n, 2):
        qc.cx(k1[i], r[i])

    for i in range(n):
        qc.cx(l[(i - 2) % n], r[i])

    for i in range(n):
        qc.cx(k2[(i + 3) % n], k0[i])
    
    for i in range(n):
        qc.cx(k2[(i + 4) % n], k0[i])

    for i in range(2, n):
        qc.x(k0[i])
        
    if rc[ex % 62] == 1:
        qc.x(k0[0])


def simon3_finalfun(qc: QuantumCircuit, l, r, k0, k1, k2, decomp: bool):
    n = len(l)
    if n % 2 != 0:
        raise ValueError("state_size must be even.")

    for i in range(1, n, 2):
        apply_ccx(qc, l[(i - 1) % n], l[(i - 8) % n], r[i], decomp)
    for i in range(0, n, 2):
        qc.cx(k0[i], r[i])

    for i in range(0, n, 2):
        apply_ccx(qc, l[(i - 1) % n], l[(i - 8) % n], r[i], decomp)
    for i in range(1, n, 2):
        qc.cx(k0[i], r[i])

    for i in range(n):
        qc.cx(l[(i - 2) % n], r[i])


# =========================================================
# Circuit builders
# =========================================================
def SIMON4(n: int, decomp: bool):
    l = QuantumRegister(n, "l")
    r = QuantumRegister(n, "r")
    k0 = QuantumRegister(n, "k0")
    k1 = QuantumRegister(n, "k1")
    k2 = QuantumRegister(n, "k2")
    k3 = QuantumRegister(n, "k3")

    if n == 16:
        rounds = 7
    elif n == 24:
        rounds = 8
    elif n == 32:
        rounds = 10
    elif n == 64:
        rounds = 17
    else:
        raise ValueError("Unsupported n for SIMON4")

    rc = get_simon_rc(n, 4)

    qc = QuantumCircuit(l, r, k0, k1, k2, k3, name=f"SIMON{2*n}/{4*n}")

    ex = 0
    simon4_finalfun(qc, l, r, k0, k1, k2, k3, decomp)
    simon4_finalfun(qc, r, l, k1, k2, k3, k0, decomp)
    for _ in range(rounds):
        simon4_roundfun(qc, l, r, k0, k1, k2, k3, decomp, rc, ex); ex += 1
        simon4_roundfun(qc, r, l, k1, k2, k3, k0, decomp, rc, ex); ex += 1
        simon4_roundfun(qc, l, r, k2, k3, k0, k1, decomp, rc, ex); ex += 1
        simon4_roundfun(qc, r, l, k3, k0, k1, k2, decomp, rc, ex); ex += 1
    
    simon4_finalfun(qc, l, r, k2, k3, k0, k1, decomp)
    simon4_finalfun(qc, r, l, k3, k0, k1, k2, decomp)

    regmap = {"l": l, "r": r, "k0": k0, "k1": k1, "k2": k2, "k3": k3}
    return qc, regmap


def SIMON2(n: int, decomp: bool):
    l = QuantumRegister(n, "l")
    r = QuantumRegister(n, "r")
    k0 = QuantumRegister(n, "k0")
    k1 = QuantumRegister(n, "k1")

    if n == 48:
        rounds = 25
    elif n == 64:
        rounds = 33
    else:
        raise ValueError("Unsupported n for SIMON2")

    rc = get_simon_rc(n, 2)

    qc = QuantumCircuit(l, r, k0, k1, name=f"SIMON{2*n}/{2*n}")

    ex = 0
    
    for _ in range(rounds):
        simon2_roundfun(qc, l, r, k0, k1, decomp, rc, ex); ex += 1
        simon2_roundfun(qc, r, l, k1, k0, decomp, rc, ex); ex += 1
        
    simon2_finalfun(qc, l, r, k0, k1, decomp)
    simon2_finalfun(qc, r, l, k1, k0, decomp)

    regmap = {"l": l, "r": r, "k0": k0, "k1": k1}
    return qc, regmap


def SIMON3(n: int, decomp: bool):
    l = QuantumRegister(n, "l")
    r = QuantumRegister(n, "r")
    k0 = QuantumRegister(n, "k0")
    k1 = QuantumRegister(n, "k1")
    k2 = QuantumRegister(n, "k2")
    if n == 24:
        rounds = 5
    elif n == 32:
        rounds = 6
    elif n == 48:
        rounds = 8
    else:
        raise ValueError("Unsupported n for SIMON3")
    rc = get_simon_rc(n, 3)
    qc = QuantumCircuit(l, r, k0, k1, k2, name=f"SIMON{2*n}/{3*n}")
    ex = 0
    simon3_finalfun(qc, l, r, k0, k1, k2, decomp)
    for _ in range(rounds):
        simon3_roundfun(qc, r, l, k0, k1, k2, decomp, rc, ex); ex += 1
        simon3_roundfun(qc, l, r, k1, k2, k0, decomp, rc, ex); ex += 1
        simon3_roundfun(qc, r, l, k2, k0, k1, decomp, rc, ex); ex += 1
        simon3_roundfun(qc, l, r, k0, k1, k2, decomp, rc, ex); ex += 1
        simon3_roundfun(qc, r, l, k1, k2, k0, decomp, rc, ex); ex += 1
        simon3_roundfun(qc, l, r, k2, k0, k1, decomp, rc, ex); ex += 1
    simon3_roundfun(qc, r, l, k0, k1, k2, decomp, rc, ex); ex += 1
    simon3_roundfun(qc, l, r, k1, k2, k0, decomp, rc, ex); ex += 1
    simon3_roundfun(qc, r, l, k2, k0, k1, decomp, rc, ex); ex += 1
    simon3_finalfun(qc, l, r, k1, k2, k0, decomp)
    simon3_finalfun(qc, r, l, k2, k0, k1, decomp)
    regmap = {"l": l, "r": r, "k0": k0, "k1": k1, "k2": k2}
    return qc, regmap


def SIMON128_192(n: int, decomp: bool):
    l = QuantumRegister(n, "l")
    r = QuantumRegister(n, "r")
    k0 = QuantumRegister(n, "k0")
    k1 = QuantumRegister(n, "k1")
    k2 = QuantumRegister(n, "k2")
    rc = get_simon_rc(n, 3)
    qc = QuantumCircuit(l, r, k0, k1, k2, name=f"SIMON{2*n}/192")
    ex = 0
    simon3_finalfun(qc, l, r, k0, k1, k2, decomp)
    for _ in range(11):
        simon3_roundfun(qc, r, l, k0, k1, k2, decomp, rc, ex); ex += 1
        simon3_roundfun(qc, l, r, k1, k2, k0, decomp, rc, ex); ex += 1
        simon3_roundfun(qc, r, l, k2, k0, k1, decomp, rc, ex); ex += 1
        simon3_roundfun(qc, l, r, k0, k1, k2, decomp, rc, ex); ex += 1
        simon3_roundfun(qc, r, l, k1, k2, k0, decomp, rc, ex); ex += 1
        simon3_roundfun(qc, l, r, k2, k0, k1, decomp, rc, ex); ex += 1
    simon3_finalfun(qc, r, l, k1, k2, k0, decomp)
    simon3_finalfun(qc, l, r, k2, k0, k1, decomp)
    # for i in range(n):
    #     qc.swap(l[i], r[i])
    regmap = {"l": l, "r": r, "k0": k0, "k1": k1, "k2": k2}
    return qc, regmap
