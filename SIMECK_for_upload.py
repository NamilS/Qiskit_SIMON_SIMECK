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

def get_simeck_rounds(n: int):
    if n == 16:
        return 7
    elif n == 24:
        return 8
    elif n == 32:
        return 10
    raise ValueError("Unsupported n for SIMECK4")

def get_simeck_rc():
    return [0] * 62

def simeck_data_fun(qc: QuantumCircuit, l, r, k, decomp: bool):
    n = len(l)

    for i in range(0, n, 2):
        apply_ccx(qc, l[i % n], l[(i - 5) % n], r[i], decomp)
        qc.cx(k[i + 1], r[i + 1])

    for i in range(1, n, 2):
        apply_ccx(qc, l[i % n], l[(i - 5) % n], r[i], decomp)
        qc.cx(k[i - 1], r[i - 1])

    for i in range(n):
        qc.cx(l[(i - 1) % n], r[i])

def simeck_key_update(qc: QuantumCircuit, src, dst, decomp: bool, rc_bit: int):
    n = len(src)

    for i in range(1, n, 2):
        apply_ccx(qc, src[i % n], src[(i - 5) % n], dst[i], decomp)
    for i in range(0, n, 2):
        apply_ccx(qc, src[i % n], src[(i - 5) % n], dst[i], decomp)

    for i in range(n):
        qc.cx(src[(i - 1) % n], dst[i])

    for i in range(2, n):
        qc.x(dst[i])

    if rc_bit == 1:
        qc.x(dst[0])

def simeck_roundfun(qc: QuantumCircuit, l, r, kin, ksrc, kout,
                    decomp: bool, rc, ex: int):
    simeck_data_fun(qc, l, r, kin, decomp)
    simeck_key_update(qc, ksrc, kout, decomp, rc[ex % 62])

def simeck_finalfun(qc: QuantumCircuit, l, r, k, decomp: bool):
    simeck_data_fun(qc, l, r, k, decomp)

def SIMECK4(n: int, decomp: bool):
    l = QuantumRegister(n, "l")
    r = QuantumRegister(n, "r")
    k0 = QuantumRegister(n, "k0")
    k1 = QuantumRegister(n, "k1")
    k2 = QuantumRegister(n, "k2")
    k3 = QuantumRegister(n, "k3")

    rounds = get_simeck_rounds(n)
    rc = get_simeck_rc()

    qc = QuantumCircuit(l, r, k0, k1, k2, k3, name=f"SIMECK{2*n}/{4*n}")

    ex = 0

    simeck_finalfun(qc, l, r, k0, decomp)
    simeck_finalfun(qc, r, l, k1, decomp)

    for _ in range(rounds):
        simeck_roundfun(qc, l, r, k2, k1, k0, decomp, rc, ex); ex += 1
        simeck_roundfun(qc, r, l, k3, k2, k1, decomp, rc, ex); ex += 1
        simeck_roundfun(qc, l, r, k0, k3, k2, decomp, rc, ex); ex += 1
        simeck_roundfun(qc, r, l, k1, k0, k3, decomp, rc, ex); ex += 1

    simeck_finalfun(qc, l, r, k2, decomp)
    simeck_finalfun(qc, r, l, k3, decomp)

    regmap = {"l": l, "r": r, "k0": k0, "k1": k1, "k2": k2, "k3": k3}
    return qc, regmap
