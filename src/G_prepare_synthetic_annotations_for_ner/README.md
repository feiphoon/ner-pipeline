# G: Preparee synthetic annotations for NER

What:
- Columns are renamed for spaCy expected structure (`label` to `entities`)
- Augmented data is shuffled (reproducibly)
- This data is then split to an 80:20 ratio for the NER training step, and written to separate train and dev folders.
