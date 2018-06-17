from .exceptions import *
import random

class GuessAttempt(object):
    
    def __init__(self, guess, hit=None, miss=None):
        self.guess = guess
        self.hit = hit
        self.miss = miss
    
        if self.hit == True and self.miss == True:
            raise InvalidGuessAttempt
    
    def is_hit(self):
        if self.hit == None:
            return False
        else:
            return True

    def is_miss(self):
        if self.miss == None:
            return False
        else:
            return True


class GuessWord(object):
    
    def __init__(self, answer):
        self.answer = answer
        self.masked = '*'*len(self.answer)

        if len(self.answer) == 0:
            raise InvalidWordException
    
    def perform_attempt(self, guess):
        if len(guess) > 1:
            raise InvalidGuessedLetterException

        guess = guess.lower()
        self.answer = self.answer.lower()
        
        if guess in self.answer:
            result = ''
            index = 0
            for i in self.answer:
                if i.lower() == guess:
                    result += guess
                else:
                    result += self.masked[index]
                index += 1
            self.masked = result
        
        if guess in self.answer:
            attempt = GuessAttempt(guess, hit=True)
        else:
            attempt = GuessAttempt(guess, miss=True)
        return attempt
    

class HangmanGame(object):
    number_of_guesses = 0
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=WORD_LIST, number_of_guesses=5):
        self.word_list = word_list
        self.number_of_guesses = number_of_guesses
        self.previous_guesses = []
        self.remaining_misses = number_of_guesses
        self.word = GuessWord(HangmanGame.select_random_word(word_list))
    
    @classmethod
    def select_random_word(cls, word_list):
        if word_list == []:
            raise InvalidListOfWordsException

        cls.word_to_guess = random.choice(word_list)
        return cls.word_to_guess
    
    def guess(self, guess):
        if self.is_finished() is True:
            raise GameFinishedException
    
        guess = guess.lower()
        self.previous_guesses.append(guess)
        
        attempt = self.word.perform_attempt(guess)
        if attempt.is_miss():
            self.remaining_misses -= 1
        
        if HangmanGame.is_won(self) is True:
            raise GameWonException
        
        if HangmanGame.is_lost(self) is True:
            raise GameLostException
        
        return attempt
    
    def is_finished(self):
        if self.word.masked == self.word.answer or self.remaining_misses is 0:
            return True
        else:
            return False
    
    def is_won(self):
        if self.word.masked == self.word.answer:
            return True
        else:
            return False
    
    def is_lost(self):
        if self.word.masked is not self.word.answer and self.remaining_misses is 0:
            return True
        else:
            return False
        
