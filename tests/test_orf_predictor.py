from genomekit.modules.orf_predictor import startcodon


def simple_test():
    sequence = "AUGAUGCCGCCA"
    x = startcodon(sequence)
    assert x == 2
