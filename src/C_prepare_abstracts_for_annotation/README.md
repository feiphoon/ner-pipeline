# C: Prepare abstracts for annotation

At this stage, we extract the information we need for annotation from each abstract, and pack all the entries into one JSONL file which can be uploaded into Doccano.

The required JSONL input format for Doccano is:

```json
{"text": "Peter Blackburn"}
{"text": "President Obama"}
```

The output JSONL format from Doccano is:
```json
{"data": "Peter Blackburn", "label": [ [0, 15, "PERSON"] ]}
{"data": "President Obama", "label": [ [10, 15, "PERSON"] ]}
```

Our own metadata can be added and will be included in the output after annotation:

```json
{"text": "Peter Blackburn", "pmid": 1}
{"text": "President Obama", "pmid": 2}
```

Giving the output of:
```json
{"id": 1, "data": "Peter Blackburn", "label": [ [0, 15, "PERSON"] ], "pmid": 1}
{"id": 2, "data": "President Obama", "label": [ [10, 15, "PERSON"] ], "pmid": 2}
```
