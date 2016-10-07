
def test_wsd():
    from sematch.disambiguation import WSD
    wsd = WSD()
    sentence = ' '.join(['I', 'went', 'to', 'the', 'bank', 'to', 'deposit', 'money', '.'])
    assert wsd.disambiguate_graph(sentence) is not None