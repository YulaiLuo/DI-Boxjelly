from flask_restful import Resource
from flask import jsonify, request, make_response
from marshmallow import Schema, fields
from flask import current_app as app

from medcat.cat import CAT
from medcat.cdb import CDB
from medcat.config import Config
from medcat.vocab import Vocab
from medcat.meta_cat import MetaCAT
from medcat.preprocessing.tokenizers import TokenizerWrapperBPE
from tokenizers import ByteLevelBPETokenizer

class PostTranslateSchema(Schema):
    texts = fields.List(fields.Str(), required=True)

class Translate(Resource):

    def __init__(self, cat):
            
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

        self.cat = cat

    def post(self):
        try:
            data = TranslateSchema().load(request.get_json())
            texts = data['texts']
            total_chars = sum(len(text) for text in texts)
        
            # Threshold for using multiprocessing
            threshold = app.config['MEDCAR_PROC_THRESHOLD']
            
            if total_chars <= threshold:
                res = {}
                for i, text in enumerate(texts):
                    result = self.cat.get_entities(text)
                    # Extract the entities from the results and do further processing                
                    processed_entities = self.process_entities({'entities': result['entities']})
                    res[i] = processed_entities
            else:
                # Create a generator to yield each text and its index
                def data_iterator(texts):
                    for i, text in enumerate(texts):
                        yield (i, str(text))

                # Process the texts in parallel using MedCAT's multiprocessing function
                nproc = app.config['MEDCAT_NPROC']
                batch_size_chars = len(texts) // nproc
                results = self.cat.multiprocessing(data_iterator(texts), batch_size_chars=batch_size_chars, nproc=nproc)

                # Extract the entities from the results and do further processing
                res = {}
                for i, result in results.items():
                    processed_entities = self.process_entities({'entities': result['entities']})
                    res[i] = processed_entities

            # Do further processing to UIL and return the results
            
            # Return the response with the appropriate status code
            return make_response(jsonify({'code': 200, 'msg': 'ok','data': res}), 200)
            
        except Exception as e:
            response = jsonify({'code': 400, 'err': 'INVALID_INPUT'})
            response.status_code = 400
            return response
            
    def process_entities(self, entities):
        entities_dict = entities['entities']
        # Create a dictionary to hold the sorted entities
        sorted_entities = {"disorder": [], "organism": [], "finding": [], "procedure": [], "substance": []}
                
        # Sort entities by type and confidence
        for entity in entities_dict.values():
            if "disorder" in entity["types"]:
                sorted_entities["disorder"].append(entity)
            elif "organism" in entity["types"]:
                sorted_entities["organism"].append(entity)
            elif "finding" in entity["types"]:
                sorted_entities["finding"].append(entity)
            elif "procedure" in entity["types"]:
                sorted_entities["procedure"].append(entity)
            elif "substance" in entity["types"]:
                sorted_entities["substance"].append(entity)
            else:
                pass
                # if "other" not in sorted_entities:
                #     sorted_entities["other"] = []
                # sorted_entities["other"].append(entity)
        
        # Sort entities within each type by confidence
        for key in sorted_entities:
            sorted_entities[key] = sorted(sorted_entities[key], key=lambda x: x["meta_anns"]["Status"]["confidence"], reverse=True)
        
        # Create a list of only the relevant fields from each entity
        processed_entities = []
        for key in sorted_entities:
            for entity in sorted_entities[key]:
                processed_entity = {
                    "sct_term": entity["pretty_name"],
                    "sct_code": entity["cui"], # SNOMED CT ID
                    "type": entity["types"], # semantic tag
                    "start_index": entity["start"],
                    "end_index": entity["end"],
                    "similarity": entity["context_similarity"],
                    "confidence": entity["meta_anns"]["Status"]["confidence"],
                    "status": entity["meta_anns"]["Status"]["value"]
                }
                processed_entities.append(processed_entity)
        
        return processed_entities
