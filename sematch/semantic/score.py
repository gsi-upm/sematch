
class Score:

    def method(self, name):
        def function(syn1, syn2):
            score = getattr(self, name)(syn1,syn2)
            return abs(score)
        return function

    def k_method(self,name):
        def function(syn1, syn2, k):
            score = getattr(self, name)(syn1,syn2,k)
            return abs(score)
        return function