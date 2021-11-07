# D: Hand annotation

This stage doesn't involve any code. This involves starting a server for an annotation tool called doccano <https://github.com/doccano/doccano>.

## Running the server

Taking instructions from [here](https://github.com/doccano/doccano), we'll choose the Docker setup:

Create a Docker container as follows:
```bash
docker pull doccano/doccano
docker container create --name doccano \
  -e "ADMIN_USERNAME=admin" \
  -e "ADMIN_EMAIL=admin@example.com" \
  -e "ADMIN_PASSWORD=password" \
  -p 8000:8000 doccano/doccano
```

Next, start doccano by running the container:
```bash
docker container start doccano
```

To stop the container, run
```bash
docker container stop doccano -t 5
```
All data created in the container will persist across restarts.

Go to http://127.0.0.1:8000/.


## Annotation setup

The setup of the annotation platform is done through the UI - this part of the config can't be uploaded as a config file and so will just be explained here:

- Corpora upload: This was built as a JSONL in the previous step. No defaults on data column name, label column name and file encoding will be changed in the interface. Respectively the settings will be "text", "label", and "utf-8".
- Labels upload: This was manually constructed as a JSON file in the `mpns-pipeline` repo, and copied over to this. These are uploaded through the doccano interface as well.

## Annotation

I've annotated _only_ the botanical names we know about from the MPNS in this text. This is very much manual.

## Annotation input and output

Our JSONL input with metadata is in the format:

```json
{"text": "Peter Blackburn", "pmid": 1}
{"text": "President Obama", "pmid": 2}
```

Giving the output of the format:

```json
{"id": 1, "data": "Peter Blackburn", "label": [ [0, 15, "PERSON"] ], "pmid": 1}
{"id": 2, "data": "President Obama", "label": [ [10, 15, "PERSON"] ], "pmid": 2}
```

This output is contained in a zip file. A sample is shown at `data/sample_data/sample_doccano_annotation_result/`.

There is a manual decision about which abstracts refer to botanical contexts and which don't. In the sample example, we had retrieved results for the search term of "daisy", and the results included chemistry-related abstracts mentioning "daisy-chains" and had nothing to do with the plant daisy. There is potential here to do a crude filtering to get rid of these abstracts entirely, for example to make an assumption about the content of an abstract based on if it mentions the words "plant" and "flowers". For now, no annotation happened in these irrelevant abstracts.

The items where no annotation happened have been automatically saved into an `unknown.jsonl` file. The rest were saved in an `admin.jsonl` file. The name of the `admin.jsonl` file is directly related to the login name of the annotator - in this case myself logging in as `admin`.

The hand annotation output is in the format:

```json
{
    "id": "ed265177-16a3-4e2e-9289-47516d99e1b5",
    "data": "Isolation of an oleanane-type saponin active from Bellis perennis through antitumor bioassay-guided procedures. Bellis perennis L. (Asteraceae) (common daisy) is a herbaceous perennial plant known as a traditional wound herb; it has been used for the treatment of bruises, broken bones, and wounds. Bellis perennis has also been used in the treatment of headache, common cold, stomachache, eye diseases, eczema, skin boils, gastritis, diarrhea, bleeding, rheumatism, inflammation, and infections of the upper respiratory tract in traditional medicine.",
    "label": [
        [
            50,
            65,
            "common"
        ],
        [
            112,
            130,
            "scientific"
        ],
        [
            145,
            157,
            "common"
        ]
    ],
    "pmid": "24617777"
}
```

Where `pmid` was our metadata from our input, and `id` is a unique hash assigned automatically to each entry by Doccano.
