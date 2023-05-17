from abc import ABC, abstractmethod
from app.models import MedcatConceptMap, MedcatTextMap
from flask import current_app as app
from mongoengine import DoesNotExist, NotUniqueError
import threading


class Strategy(ABC):

    @abstractmethod
    def execute(self, cat, data):
        pass

class PredictStrategy(Strategy):

    def __init__(self):
        self.lock = threading.RLock()  



    def _after_predict(self, texts, medcat_predictions):
        concept_maps = [MedcatConceptMap(status='fail') if not medcat_predictions[i] else MedcatConceptMap(**medcat_predictions[i]) for i,_ in medcat_predictions.items()]
        for i in range(len(concept_maps)):
            try:
                concept_maps[i].save()
            except NotUniqueError:
                concept_maps[i] = MedcatConceptMap.objects(sct_code=concept_maps[i].sct_code).first()
                pass
        
        for i in range(len(texts)):
            try:
                MedcatTextMap(text=texts[i], map=concept_maps[i]).save()
            except NotUniqueError:
                pass
        
        
    def execute(self, cat, data):
        texts = data['texts']

        medcat_predictions = self._medcat_predict(cat, texts)
        
        result = self._translate_to_uil(medcat_predictions, texts)

        # Storing the data to the database
        thread = threading.Thread(target=self._after_predict, args=(texts,medcat_predictions,))
        thread.start()

        return {
            'name':'Medcat',
            'result': result
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
            "sct_status": selected_entity['meta_anns']['Status']['value'],
            "sct_status_confidence": selected_entity['meta_anns']['Status']['confidence'],
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

        # If the text is less than the threshold, process it in a single thread
        if len(texts) < app.config['MEDCAR_PROC_THRESHOLD']:
            
            res = {}
            for i, text in enumerate(texts):
                entities = cat.get_entities(text)['entities']
                result = self._extract_data(entities)

                res[i] = result

            return res
        
        # Otherwise, process the texts in parallel using MedCAT's multiprocessing function
        nproc = app.config['MEDCAT_NPROC']
        batch_size_chars = len(texts) // nproc + 1
        predictions = cat.multiprocessing(self._data_iterator(texts),
                                        batch_size_chars=batch_size_chars, 
                                        nproc=nproc)
        res={}
        for i, pred in predictions.items():
            result = self._extract_data(pred['entities'])
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
        conceptmap = list(MedcatConceptMap.objects.aggregate(*pipeline))
        sct_dict = {map['sct_code']: map for map in conceptmap}
        
        result = {}
        for idx, prediction in medcat_predictions.items():
            if prediction is None:
                result[idx]=None
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
            raise DoesNotExist('Input text not found')
        
        text_map.map.curated_uil_name = data['curated_uil_name']
        text_map.map.curated_uil_group = data['curated_uil_group']
        text_map.map.save()

class ResetStrategy(Strategy):
    def execute(self, cat, data):

        pass

