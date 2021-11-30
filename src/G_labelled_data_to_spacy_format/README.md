# G: Labelled data to spaCy format


This stage is to convert our labelled data to spaCy training format.

The spaCy training format is a list of tuples, each of which is a labelled corpus.

```python
{
    "text": str,
    "entities": List[Tuple[int, int, str]]
}
```

Example:

```python
("Potato corpus", {"entities": [(0, 6, "VEGETABLE")]})
```

This is based on the spaCy documentation https://spacy.io/api/data-formats#training, and a tip from https://www.machinelearningplus.com/nlp/training-custom-ner-model-in-spacy/.

Conversion to the new binary spaCy format has to follow.


Desired output example:

```python
[
    (
        "Insulin Mimetic Properties of Extracts Prepared from <i>Bellis perennis</i>. Diabetes mellitus (DM) and consequential cardiovascular diseases lead to millions of deaths worldwide each year; 90% of all people suffering from DM are classified as Type 2 DM (T2DM) patients. T2DM is linked to insulin resistance and a loss of insulin sensitivity. It leads to a reduced uptake of glucose mediated by glucose transporter 4 (GLUT4) in muscle and adipose tissue, and finally hyperglycemia. Using a fluorescence microscopy-based screening assay we searched for herbal extracts that induce GLUT4 translocation in the absence of insulin, and confirmed their activity in chick embryos. We found that extracts prepared from <i>Bellis perennis</i> (common daisy) are efficient inducers of GLUT4 translocation in the applied in vitro cell system.",
        {
            "entities": [
                (56, 71, "common"),
                (714, 729, "common"),
                (735, 747, "common"),
                (1253, 1268, "common"),
            ]
        },
    )
]
```
