import mainDemo as demo
from abc import ABC, abstractmethod

from App.AppEnums.generationModesEnum import GenerationMode

class GenerationStrategy(ABC):
    @abstractmethod
    def generate_melodies(self, *, n_bars, n_sims = 1, markov, temperature = 1):
        pass

class MagentaGenerationStrategy(GenerationStrategy):
    def generate_melodies(self, *, n_bars, n_sims = 1, markov, temperature = 1):
        print("Generated with magenta")
        return demo.generate_magenta(n_bar=n_bars, n_sims=n_sims, temperature=temperature)

class MarkovGenerationStrategy(GenerationStrategy):
    def generate_melodies(self, *, n_bars, n_sims = 1, markov, temperature = 1):
        print("Generated with markov")
        return demo.generate_markov(generator=markov, n_bar=n_bars, n_sims=n_sims)

class RNNGenerationStrategy(GenerationStrategy):
    def generate_melodies(self, *, n_bars, n_sims = 1, markov, temperature = 1):
        print("Generated with RNN")
        return demo.generate_rnn(n_bar=n_bars, temperature=temperature)
    
strategy_per_mode = {
    GenerationMode.MAGENTA.value: MagentaGenerationStrategy(),
    GenerationMode.MARKOV.value: MarkovGenerationStrategy(),
    GenerationMode.RNN.value: RNNGenerationStrategy()
}   