from abc import ABC, abstractmethod
from app.models import MedcatConceptMap, MedcatTextMap
from flask import current_app as app
from mongoengine import DoesNotExist, NotUniqueError
from fuzzywuzzy import fuzz
from pymongo import UpdateOne
import threading, re


class Strategy(ABC):

    @abstractmethod
    def execute(self, cat, data):
        pass

class PredictStrategy(Strategy):

    def __init__(self):
        self.lock = threading.RLock()  

    def _after_predict(self, texts, medcat_predictions):

        # concept_maps = [MedcatConceptMap(status='fail') if not medcat_predictions[i] else MedcatConceptMap(**medcat_predictions[i]) for i,_ in medcat_predictions.items()]
        concept_maps = [MedcatConceptMap(**medcat_predictions[i]) for i,_ in medcat_predictions.items() if medcat_predictions[i]]

        with self.lock:
            
            concept_maps_updates = [
                UpdateOne(
                    {'sct_code':concept_map.sct_code},
                    {'$set':concept_map.to_mongo().to_dict()},
                    upsert=True
                ) for concept_map in concept_maps
            ]
            MedcatConceptMap._get_collection().bulk_write(concept_maps_updates)

            # texts_map_updates = [
            #     UpdateOne(
            #         {'text': text},
            #         {'$set': {'text': text, 'map': concept_maps[i].id}},
            #         upsert=True
            #     ) for i, text in enumerate(texts)
            # ]
            # MedcatTextMap._get_collection().bulk_write(texts_map_updates)

    def _find_similar(self, failed_text, text_maps):
        if len(text_maps)<=0:
            return None
        
        similarities = [fuzz.ratio(failed_text, doc.text) for doc in text_maps]
        if len(similarities)<=0:
            return None
        
        idx, max_similarity = max(enumerate(similarities), key=lambda x: x[1])
        return text_maps[idx], max_similarity
        
    def _process_failed(self, curated_results, texts):
        failed_indices = [i for i in range(len(curated_results)) if curated_results[i] is None]
        # failed_texts = [texts[i] for i in failed_indices]
        
        for i in failed_indices:
            failed_text = texts[i]

            text_maps = MedcatTextMap.objects(text=re.compile(failed_text, re.IGNORECASE))

            res = self._find_similar(failed_text, text_maps)
            if not res:
                continue
            text_map, similarity = res
            curated_results[i] = {
                'text': failed_text,
                'name':  text_map.curated_uil_name,
                'ontology': 'UIL',
                'accuracy': similarity/100,
                'status': 'success',
                'extra': {
                    '0':{
                        'display_name': 'Notification',
                        'value': 'This text is originally failed, but mapped to the most similar text from history mapping'
                    }
                }
            }

        return curated_results
        
    def execute(self, cat, data):
        # step 1: Read texts from the requests
        texts = data['texts']

        # step 2: Predict the texts to snomed-ct using MedCAT
        medcat_predictions = self._medcat_predict(cat, texts)

        # step 3: (Concept Map) Convert the smoed-ct codes to UIL codes based on the history snomed-ct curation
        curated_results = self._translate_to_uil(medcat_predictions, texts)

        # step 4: (Text Map) Convert the failed text(Not even mapped to snomed ct) directly to uil based on the history text curation
        result = self._process_failed(curated_results, texts)

        # step 5: Store the medcat mapping result to the database
        threading.Thread(target=self._after_predict, args=(texts,medcat_predictions,)).start()

        return {
            'name':'Medcat',    # the name of mapper
            'result': result    # the result of mapping
        }
    
    def _select_entities(self, entities):
        highest_context_similarity_idx = max(entities, key=lambda x: entities[x]['context_similarity'])
        return  entities[highest_context_similarity_idx]
    
    def _extract_data(self, entities):
        # If no entities is mapped, return a default 
        if len(entities)<=0:
            return None

        # If mapping success, select the most appropriate entity and extract key data
        selected_entity = self._select_entities(entities)
        result = {
            "accuracy":selected_entity['acc'],
            "sct_code":selected_entity['cui'],
            "sct_term":selected_entity['detected_name'],
            "sct_pretty_name": selected_entity['pretty_name'],
            "sct_status": None if not selected_entity['meta_anns']['Status'] else selected_entity['meta_anns']['Status']['value'],
            "sct_status_confidence": None if not selected_entity['meta_anns']['Status'] else selected_entity['meta_anns']['Status']['confidence'],
            "sct_types": selected_entity['types'],
            "sct_types_ids": selected_entity['type_ids'],
            "status": 'success'
        }
        return result
    
    def _data_iterator(self, texts):
        for i, text in enumerate(texts):
            yield (i, str(text))

    def _medcat_predict(self, cat, texts):
        
        # Return an empty dictionary if there are no entities
        if len(texts) <=0:
            return {}
        
        res = {}
        for i, text in enumerate(texts):
            entities = cat.get_entities(text)['entities']
            result = self._extract_data(entities)

            res[i] = result

        return res

    def _translate_to_uil(self,medcat_predictions, texts):

        sct_codes = [prediction['sct_code'] for prediction in medcat_predictions.values() if prediction]
        pipeline = [
            {'$match':{'sct_code':{'$in':sct_codes}}},
            {'$project':{
                    '_id':0,
                    'sct_code':1,
                    'curated_uil_name':1,
                    'curated_uil_group':1
                }
            }
        ]
        conceptmaps = list(MedcatConceptMap.objects.aggregate(*pipeline))
        sct_dict = {map['sct_code']: map for map in conceptmaps}
        
        result = {}
        for idx, prediction in medcat_predictions.items():
            if prediction is None:
                result[idx] = None
            else:
                history_map = sct_dict.get(prediction['sct_code'], None)
                uil_name = None if not history_map else history_map['curated_uil_name']
                result[idx] = {
                    'text': texts[int(idx)],
                    'name': uil_name if uil_name else prediction['sct_pretty_name'],
                    'ontology': 'UIL' if uil_name else 'SNOMED-CT',
                    'accuracy': prediction['accuracy'],
                    'status': 'success',
                    'extra': {
                        '0':{
                            'display_name':'SNOMED-CT Code',
                            'value': prediction['sct_code']
                        },
                        '1':{
                            'display_name':'SNOMED-CT Name',
                            'value': prediction['sct_term']
                        },
                        '2':{
                            'display_name':'SNOMED-CT Status',
                            'value': prediction['sct_status']
                        },
                        '3':{
                            'display_name':'SNOMED-CT Status Confidence',
                            'value': prediction['sct_status_confidence']
                        },
                        '4':{
                            'display_name':'SNOMED-CT Status Types',
                            'value': ' '.join(prediction['sct_types'])
                        }
                    }
                }

        return result


class RetrainStrategy(Strategy):
    def execute(self, cat, data):
        text_map = MedcatTextMap.objects(text=data['text']).first()
        if not text_map:
            MedcatTextMap(text=data['text'], 
                          curated_uil_name=data['curated_uil_name'], 
                          curated_uil_group=data['curated_uil_group']).save()
        else:
            text_map.curated_uil_name = data['curated_uil_name']
            text_map.curated_uil_group = data['curated_uil_group']
            text_map.save()

        #Predict the sct code to conduct the concept map
        entities = cat.get_entities(data['text'])['entities']
        if len(entities)>0:
            highest_context_similarity_idx = max(entities, key=lambda x: entities[x]['context_similarity'])
            sct_code = entities[highest_context_similarity_idx]['cui']
            concept_map = MedcatConceptMap.objects(sct_code=sct_code).first()
            if not concept_map:
                pass
            else:
                concept_map.curated_uil_name = data['curated_uil_name']
                concept_map.curated_uil_group = data['curated_uil_group']
                concept_map.save()

        
        

class ResetStrategy(Strategy):
    def execute(self, cat, data):

        pass

