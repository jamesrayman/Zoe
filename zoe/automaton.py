class Automaton:
    def __init__(self, init_state, init_mem, transitions):
        self.state = init_state
        self.mem = init_mem
        self.transitions = transitions

    def check(self):
        for condition, next_state, transition, output in self.transitions[self.state]:
            if condition(self.mem):
                self.state = next_state
                res = output(self.mem)
                self.mem = transition(self.mem)
                return False, res

        return True, None

    def process(self, c):
        self.mem += c

        res = []
        while True:
            done, out = self.check()
            if done:
                return res
            elif out is not None:
                res += [out]
