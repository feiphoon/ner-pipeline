# F: Synthesise annotated abstracts

What:
- Train and validation sets at `data/processed/synthesised_abstracts_for_ner/2021-12-02-23-46-50`
- Name mappings at `data/reference/mpns_v8/mpns_name_mappings/v5`
- Name mappings are stratified to give a good base and balance of types of scientific names (i.e. Plants, Synonyms and Sci-cited Medicinal names). The previous stage produced over 3 million name mappings to work with.
- The volume of abstracts multiplied given a bunch of name mappings, out.
- Replace the labels in the annotated data with new entities.



## The input data

The input data is from the MPNS Pipeline, and is copied over into this repo at `data/reference/mpns_v8/mpns_name_mappings/v5`. It is partitioned by `scientific_name_type`, so:
- `plant`
- `synonym`
- `sci_cited_medicinal`

This allows us to have a selection of Scientific names against Common & Pharmaceutical names, that we can pick from for synthetic annotation.

The following is the data schema  (`scientific_name_type` actually appears as partitions - so the data has to be read into Spark for them to appear this way):

| scientific_name_id | scientific_name                             | scientific_name_length |scientific_name_type | common_names                                                                                                                                                                                                                                            | pharmaceutical_names                   | common_name_count | pharmaceutical_name_count | non_scientific_name_count | mapping_id |
|--------------------|---------------------------------------------|------------------------|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------|-------------------|---------------------------|---------------------------|------------|
| gccgcc-17504       | Psathyrotes ramosissima (Torr.) A.Gray      | 38                     |plant                | [[velvet turtleback, gccgcc-17504, 17]]                                                                                                                                                                                                                 | null                                   | 0                 | 0                         | 0                         | 266510     |
| wcsCmp483782       | Sedum hispanicum L.                         | 19                     |plant                | [[angur-e sheytani, wcsCmp483782, 16]]                                                                                                                                                                                                                  | null                                   | 0                 | 0                         | 0                         | 298364     |
| wcsCmp809318       | Fibraurea tinctoria Lour.                   | 25                     |plant                | [[akar badi, wcsCmp809318, 9], [akar mengkunyit, wcsCmp809318, 15], [areuj gember, wcsCmp809318, 12]]                                                                                                                                                   | [[fibraurea caulis, wcsCmp809318, 16]] | 3                 | 1                         | 4                         | 145584     |


## Stratification

Stratification for training is applied at the top or `scientific_name_type` level, but not at the `non_scientific_name_type` level. The rows will be shuffled within each `scientific_name_type`.

- Scientific
    - Plant
    - Synonym
    - Sci_cited_medicinal
- Non-Scientific
    - Common
    - Pharmaceutical

The name mappings are filtered for mappings with a minimum number of entities (by type), to meet the maximum number of
entities (by type) in the abstracts. This is so that we don't run into a problem of trying to do entity replacement in
an abstract which may have 5 common entities to replace, and a name mapping which has only 4 common entities to swap out.

This also to ensure as many Non-Scientific Names as possible are placed in the training data.
