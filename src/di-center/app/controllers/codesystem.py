
from bson import ObjectId
from app.models import ConceptVersion, ConceptGroup, Concept, CodeSystem
class CodeSystemController:

    def get_code_system_data(code_system):
        
        pipeline = [
            # Step one: Match the ConceptVersions of CodeSystem
            {"$match": {"code_system": ObjectId(code_system.id)}},
            # Step two: Add related Concept, ConceptGroup, and Tag docs to every ConceptVersion doc
            {"$lookup": {
                "from": "concept",
                "localField": "concept",
                "foreignField": "_id",
                "as": "concept_doc"
            }},
            {"$lookup": {
                "from": "concept_group",
                "localField": "group",
                "foreignField": "_id",
                "as": "group_doc"
            }},
            {"$lookup": {
                "from": "tag",
                "localField": "tags",
                "foreignField": "_id",
                "as": "tag_docs"
            }},
            # Step 3: Format the doc strtucture to desired format
            {"$project": {
                "_id": 0,
                "group_name": {"$arrayElemAt": ["$group_doc.name", 0]},
                "concept_name": {"$arrayElemAt": ["$concept_doc.name", 0]},
                "tag_names": "$tag_docs.name",
                "alias": 1,
                "tags":{
                    "$filter": {
                        "input": "$tag_docs",
                        "as": "tag",
                        "cond": {"$eq": ["$$tag.source", "official"]}
                    }
                },
                "my_tags": {
                    "$filter": {
                        "input": "$tag_docs",
                        "as": "tag",
                        "cond": {"$eq": ["$$tag.source", "user"]}
                    }
                },
            }},
            # Step 4: Group the concept version by groups, and collect each group into one array
            {"$group": {
                "_id": "$group_name",
                "concept_versions": {"$push": {
                    "concept_name": "$concept_name",
                    "alias": "$alias",
                    "tags": "$tags.name",
                    "my_tags": "$my_tags.name"
                }}
            }},
            # Step 5: Reformat the docs sturcture to the final output
            {"$project": {
                "_id": 0,
                "group_name": "$_id",
                "concept_versions": 1
            }},
            # Step 6: Sort by group_name
            {"$sort": {"group_name": 1}}
        ]

        result = list(ConceptVersion.objects().aggregate(*pipeline))
        return result
