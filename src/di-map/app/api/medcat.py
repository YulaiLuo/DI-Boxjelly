from flask_restful import Resource
from flask import jsonify, request
from marshmallow import Schema, fields, ValidationError, validate

class TranslateSchema(Schema):
    texts = fields.List(fields.Str(), required=True)

class MedCatTranslate(Resource):

    def __init__(self, cat):
        self.cat = cat

    def get(self):
        try:
            data = TranslateSchema().load(request.get_json())
            texts = data['texts']

            # Create a generator to yield each text and its index
            def data_iterator(texts):
                for i, text in enumerate(texts):
                    yield (i, str(text))

            # Process the texts in parallel using MedCAT's multiprocessing function
            batch_size_chars = 500 # Set the batch size in characters
            results = self.cat.multiprocessing(data_iterator(texts), batch_size_chars=batch_size_chars, nproc=2)

            # Extract the entities from the results and do further processing
            res = {}
            for i, result in results.items():
                processed_entities = self.process_entities({'entities': result['entities']})
                res[i] = processed_entities

            # Do further processing to UIL and return the results
            
            # Return the response with the appropriate status code
            response = jsonify({'code': 200, 'res': res})
            response.status_code = 200

            return response
            
        except Exception as e:
            response = jsonify({'code': 400, 'err': 'INVALID_INPUT'})
            response.status_code = 400

            return response
            
    def process_entities(self, entities):
        entities_dict = entities['entities']
        # Create a dictionary to hold the sorted entities
        sorted_entities = {}
        
        # Sort entities by type and confidence
        for entity in entities_dict.values():
            if "disorder" in entity["types"]:
                if "disorder" not in sorted_entities:
                    sorted_entities["disorder"] = []
                sorted_entities["disorder"].append(entity)
            else:
                if "other" not in sorted_entities:
                    sorted_entities["other"] = []
                sorted_entities["other"].append(entity)
        
        # Sort entities within each type by confidence
        for key in sorted_entities:
            sorted_entities[key] = sorted(sorted_entities[key], key=lambda x: x["meta_anns"]["Status"]["confidence"], reverse=True)
        
        # Create a list of only the relevant fields from each entity
        processed_entities = []
        for key in sorted_entities:
            for entity in sorted_entities[key]:
                processed_entity = {
                    "term_name": entity["pretty_name"],
                    "SCTID": entity["cui"], # SNOMED CT ID
                    "type": entity["types"], # semantic tag
                    'raw_text': entity['source_value'],
                    "start_index": entity["start"],
                    "end_index": entity["end"],
                    "similarity": entity["context_similarity"],
                    "confidence": entity["meta_anns"]["Status"]["confidence"],
                    "status": entity["meta_anns"]["Status"]["value"]
                }
                processed_entities.append(processed_entity)
        
        return processed_entities
