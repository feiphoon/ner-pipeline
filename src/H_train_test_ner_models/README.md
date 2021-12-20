# H: Train and test custom NER models

What:
- Conversion of train, validation (dev) and test data to `.spacy` format
- Training all models in `model_runner.ipynb` (Jupyter notebook)

The inputs are at:
- Train data: `data/processed/converted_train_test_data_for_ner/train`
- Validation data: `data/processed/converted_train_test_data_for_ner/dev`
- Test data: `data/processed/converted_train_test_data_for_ner/test`
- Training config for each model: `data/processed/converted_train_test_data_for_ner/training_config`

The output is at:
- Best and last models for each trained model: `data/processed/converted_train_test_data_for_ner/output`
- Visualised results for each trained model (in HTML format): `data/processed/converted_train_test_data_for_ner/results`
