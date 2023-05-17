from abc import ABC, abstractmethod
from app.models import MedcatConceptMap, MedcatTextMap
from flask import current_app as app
from mongoengine import DoesNotExist
import threading

lock = threading.Lock()

class Strategy(ABC):

    @abstractmethod
    def execute(self, cat, data):
        pass

class PredictStrategy(Strategy):

    def _after_predict(self, texts, medcat_predictions):
        print(texts,medcat_predictions)
        with lock:
            existing_sct_codes = MedcatConceptMap.objects().distinct('sct_code')
            existing_sct_texts = MedcatTextMap.objects().distinct('text')

            # Storing the data to the database
            concept_maps = [MedcatConceptMap(**medcat_predictions[idx]) 
                            for idx, _ in medcat_predictions.items()
                            if medcat_predictions[idx]['sct_code'] not in existing_sct_codes]

            text_maps = [MedcatTextMap(text=texts[i], map=concept_maps[i]) 
                        for i in range(len(texts))
                        if texts[i] not in existing_sct_texts]
            if len(concept_maps)>0:
                MedcatConceptMap.objects.insert(concept_maps)

            if len(text_maps)>0:
                MedcatTextMap.objects.insert(text_maps)
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
            return {
                "accuracy":0,
                "sct_code":'',
                "sct_term":'',
                "sct_pretty_name": '',
                "sct_status": '',
                "sct_status_confidence": 0,
                "sct_types": [],
                "sct_types_ids": [],
                "status": 'fail'
            }

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

        sct_codes = [prediction['sct_code'] for prediction in medcat_predictions.values()]
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
            if prediction['status'] == 'fail':
                result[idx] = {
                    'text': texts[int(idx)],
                    'name': '',
                    'ontology': '',
                    'accuracy': '',
                    'status': 'fail',
                    'extra':{
                        '0':{
                            'display_name':'Fail',
                            'value': 'This text is not mapped to any SNOMED-CT, \n\
                                  so we cannot map it into UIL concept.'
                        },
                        '1':{
                            'display_name':'Suggestion',
                            'value': 'Try to curate it! \n \
                                  Next time I will figure it out!'
                        }
                    }
                }
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
        text_map = TextMap.objects(text=data['text']).first()
        if not text_map:
            raise DoesNotExist('Input text not found')
        
        text_map.map.curated_uil_name = data['uil_name']
        text_map.map.curated_uil_group = data['uil_group']
        text_map.map.save()

class ResetStrategy(Strategy):
    def execute(self, cat, data):

        pass

