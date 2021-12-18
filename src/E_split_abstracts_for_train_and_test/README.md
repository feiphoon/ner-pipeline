# E: Data split

This stage is where we split our hand annotated data for training and testing. Briefly:

- All hand-annotated data is shuffled (with a seed)
- start with a Train/Test split of 60:40.

We extract the contents of the annotated abstracts zip and split the data.

Because this was done in PySpark, to safeguard against non-deterministic shuffling,
all entries were first ordered by `pmid`, then assigned an `order` number using seeded randomisation.
The entries were then sorted by this `order` number, and the `row_number` Windowing function
was applied to give a contiguous integer value to each row.

The entries were then assigned a boolean `is_train` flag depending on the value of this number
divided by the total number of rows, and compared against the 60:40 split. Entries where 
`is_train` is True went to the train set, and the difference went to the test set.

This resulted in 22 items for the training set and 15 items for the test set.
