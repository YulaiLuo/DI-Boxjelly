from .mapper import MapperController
from medcat.cat import CAT
from medcat.cdb import CDB
from medcat.vocab import Vocab
from medcat.meta_cat import MetaCAT
from .strategy import PredictStrategy, RetrainStrategy, ResetStrategy
import os


class MedcatController(MapperController):

    def __init__(self):
        super().__init__()

        unzip = '/data/di-data/di-map/medcat_model/'  # Define the model path
        # Load the vocab model you downloaded
        vocab = Vocab.load(unzip+'vocab.dat')
        # Load the cdb model you downloaded
        cdb = CDB.load(unzip+'cdb.dat')

        # needed to add these two lines
        cdb.config.linking.filters.cuis = set()
        cdb.config.general.spacy_model = unzip+'spacy_model'

        # Download the mc_status model from the models section below and unzip it
        mc_status = MetaCAT.load(unzip+'meta_Status/')
        cat = CAT(cdb=cdb, config=cdb.config,
                  vocab=vocab, meta_cats=[mc_status])

        # Initialize the MedCAT model
        self.cat = cat
        self.predict_strategy = PredictStrategy()
        self.retrain_strategy = RetrainStrategy()
        self.reset_strategy = ResetStrategy()

    def predict(self, data):
        return self.predict_strategy.execute(self.cat, data)

    def retrain(self, data):
        return self.retrain_strategy.execute(self.cat, data)

    def reset(self, data):
        return self.reset_strategy.execute(self.cat, data)
