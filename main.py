from src.helpers.run_helper import Run


if __name__ == "__main__":
    run = Run()

    input_filepath = "banana"
    print(run.create_run_filepath(input_filepath))

    output_filepath = "potato"
    print(run.create_run_filepath(output_filepath))
