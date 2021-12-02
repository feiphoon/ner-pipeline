from invoke import task, Collection


@task
def build(c):
    c.run(
        "DOCKER_BUILDKIT=1 docker build -t punchy/ner-pipeline:0.1.0 .",
        pty=True,
    )


@task
def build_no_cache(c):
    c.run(
        "DOCKER_BUILDKIT=1 docker build --no-cache -t punchy/ner-pipeline:0.1.0 .",
        pty=True,
    )


@task
def pyspark_get_abstracts(c):
    c.run(
        "docker run -v $(pwd):/job punchy/ner-pipeline:0.1.0 main.py \
            --name 'ner-pipeline-container'\
                ;CONTAINER_ID=$(docker ps -lq)\
                    ;docker cp `echo $CONTAINER_ID`:/data .",
        pty=True,
    )


@task
def pyspark_split_abstracts(c):
    c.run(
        "docker run -v $(pwd):/job punchy/ner-pipeline:0.1.0 split_abstracts_runner.py \
            --name 'ner-pipeline-container'\
                ;CONTAINER_ID=$(docker ps -lq)\
                    ;docker cp `echo $CONTAINER_ID`:data/processed/split_annotated_abstracts \
                        data/processed/",
        pty=True,
    )


@task
def pyspark_synthesise_annotations(c):
    c.run(
        "docker run -v $(pwd):/job punchy/ner-pipeline:0.1.0 synthesise_annotated_abstracts_runner.py \
            --name 'ner-pipeline-container'\
                ;CONTAINER_ID=$(docker ps -lq)\
                    ;docker cp `echo $CONTAINER_ID`:data/processed/synthesised_annotated_abstracts \
                        data/processed/",
        pty=True,
    )


ns = Collection()
ps = Collection("ps")

ps.add_task(build)
ps.add_task(build_no_cache)
ps.add_task(pyspark_get_abstracts, name="get_abstracts")
ps.add_task(pyspark_split_abstracts, name="split_abstracts")
ps.add_task(pyspark_synthesise_annotations, name="synthesise_annotations")

ns.add_collection(ps)


@task
def test(c):
    c.run("python -m pytest -vv", pty=True)


@task
def lint(c):
    c.run("python -m flake8 main.py", pty=True)
    c.run("python -m flake8 src/.", pty=True)
    c.run("python -m flake8 tests/.", pty=True)
    c.run("python -m black --check .", pty=True)


ns.add_task(test)
ns.add_task(lint)
