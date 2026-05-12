import math


def calculate_tm_nn(sequence, conc=50e-9, na=50e-3):
    """
    Calculate melting temperature (Tm) using nearest-neighbor (SantaLucia) model
    and molecular weight of a DNA sequence.

    Parameters:
        sequence (str): DNA sequence (e.g., "ATGC")
        conc (float): Strand concentration in M (default = 50 nM)
        na (float): Sodium (Na) concentration in M (default = 50 mM)

    Returns:
        tm (float): Melting temperature in °C
        mw (float): Molecular weight in g/mol
    """

    # ---- Input validation ----
    sequence = sequence.upper()
    valid_bases = {"A", "T", "G", "C"}

    if not all(base in valid_bases for base in sequence):
        raise ValueError("Sequence contains invalid characters. Only A, T, G, C allowed.")

    if len(sequence) < 2:
        raise ValueError("Sequence must be at least 2 nucleotides long.")

    # ---- Nearest-neighbor parameters (ΔH kcal/mol, ΔS cal/mol*K) ----
    nn_params = {
        "AA": (-7.9, -22.2),
        "TT": (-7.9, -22.2),
        "AT": (-7.2, -20.4),
        "TA": (-7.2, -21.3),
        "CA": (-8.5, -22.7),
        "TG": (-8.5, -22.7),
        "GT": (-8.4, -22.4),
        "AC": (-8.4, -22.4),
        "CT": (-7.8, -21.0),
        "AG": (-7.8, -21.0),
        "GA": (-8.2, -22.2),
        "TC": (-8.2, -22.2),
        "CG": (-10.6, -27.2),
        "GC": (-9.8, -24.4),
        "GG": (-8.0, -19.9),
        "CC": (-8.0, -19.9),
    }

    # ---- Initiation values ----
    delta_h = 0.2  # kcal/mol
    delta_s = -5.7  # cal/mol*K

    # ---- Sum nearest-neighbor contributions ----
    for i in range(len(sequence) - 1):
        pair = sequence[i : i + 2]
        dh, ds = nn_params[pair]
        delta_h += dh
        delta_s += ds

    # ---- Gas constant ----
    r = 1.987  # cal/mol*K

    # ---- Tm calculation (Kelvin → Celsius) ----
    tm = (delta_h * 1000) / (delta_s + r * math.log(conc)) - 273.15

    # ---- Salt correction ----
    tm += 16.6 * math.log10(na)

    # ---- Molecular Weight ----
    weights = {"A": 313.21, "T": 304.2, "G": 329.21, "C": 289.18}

    mw = sum(weights[base] for base in sequence) - 61.96
    return tm, mw
