from flask_restful import Resource
from flask import jsonify, request
from marshmallow import Schema, fields, ValidationError, validate

class TranslateSchema(Schema):
    text = fields.Str(required=True)

class MedCatTranslate(Resource):

    def __init__(self, cat):
        self.cat = cat

    def post(self):
        data = TranslateSchema().load(request.form)
        text = data['text']
        entities = self.cat.get_entities(text)['entities']

        # Do further processing to UIL and return the results
        res = self.process_entities({'entities': entities})
        return res
    
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
                    "snomed_ct_code": entity["cui"],
                    "type": entity["types"],
                    "start_index": entity["start"],
                    "end_index": entity["end"],
                    "similarity": entity["context_similarity"],
                    "confidence": entity["meta_anns"]["Status"]["confidence"],
                    "status": entity["meta_anns"]["Status"]["value"]
                }
                processed_entities.append(processed_entity)
        
        return processed_entities
