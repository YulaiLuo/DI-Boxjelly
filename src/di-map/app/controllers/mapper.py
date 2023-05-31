from abc import ABC, abstractmethod

class MapperController(ABC):

    @abstractmethod
    def predict(self, data):
        """Process the mapping request from the center service
        Deal with the single text mapping request

        Args:
            data (json): _description_
        """
        pass

    @abstractmethod
    def retrain(self, data):
        """Accept request from the center service about 
        the curated information from user

        Args:
            data (json): _description_
        """
        pass
    
    @abstractmethod
    def reset(self, data):
        """Make the system reset to the initial default state

        Args:
            data (json): _description_
        """
        pass