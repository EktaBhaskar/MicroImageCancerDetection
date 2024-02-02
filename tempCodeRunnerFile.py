generate_fake_data_time = timeit.timeit(microbiology_runner.generate_fake_data(1, 10000), number=1)
    # print("Generate_fake_data Execution Time:", generate_fake_data_time, "seconds")