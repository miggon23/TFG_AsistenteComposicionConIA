import mainDemo as demo
from abc import ABC, abstractmethod

class GenerationStrategy(ABC):
    @abstractmethod
    def generate_melodies(self, *, n_bars, n_sims = 1, markov, temperature = 1):
        pass

class MagentaGenerationStrategy(GenerationStrategy):
    def generate_melodies(*, n_bars, n_sims = 1, markov, temperature = 1):
        demo.generate_magenta(n_bar=n_bars, n_sims=n_sims, temperature=temperature)

class MarkovGenerationStrategy(GenerationStrategy):
    def generate_melodies(*, n_bars, n_sims = 1, markov, temperature = 1):
        demo.generate_markov(generator=markov, n_bar=n_bars, temperature = temperature)

class RNNGenerationStrategy(GenerationStrategy):
    def generate_melodies(*, n_bars, n_sims = 1, markov, temperature = 1):
        demo.generate_rnn(n_bar=n_bars, temperature=temperature)