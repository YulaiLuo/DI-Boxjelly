from flask_restful import Api
from .medcat import MedCatTranslate

from medcat.cat import CAT
from medcat.cdb import CDB
from medcat.config import Config
from medcat.vocab import Vocab
from medcat.meta_cat import MetaCAT
from medcat.preprocessing.tokenizers import TokenizerWrapperBPE
from tokenizers import ByteLevelBPETokenizer

def init_api(app):
    """
    Initialize the API, adding all routes to the Flask app.

    Args:
        app (Flask): The Flask app
    """
    
    unzip = './app/medcat_model/'
    # Load the vocab model you downloaded
    vocab = Vocab.load(unzip+'vocab.dat')
    # Load the cdb model you downloaded
    cdb = CDB.load(unzip+'cdb.dat')

    # needed to add these two lines
    cdb.config.linking.filters.cuis = set()
    cdb.config.general.spacy_model = unzip+'spacy_model'

    # Download the mc_status model from the models section below and unzip it
    mc_status = MetaCAT.load(unzip+'meta_Status/')
    cat = CAT(cdb=cdb, config=cdb.config, vocab=vocab, meta_cats=[mc_status])

    # Create the API instance
    api = Api()

    # Add route
    api.add_resource(MedCatTranslate, '/map/medcat/single-translate', resource_class_kwargs={'cat': cat})   

    # Initialize the API
    api.init_app(app)



