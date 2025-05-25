from profiler.core import *


def fdx(dataset_path, na_values="empty", sparsity=0.0):

    pf = Profiler(workers=1, tol=1e-6, eps=0.05, embedtxt=True)
    pf.session.load_data(
        name="customer",
        src=FILE,
        fpath=dataset_path,
        check_param=True,
        na_values=na_values,
    )

    # implement later the change_dtypes method

    pf.session.load_embedding(save=True, path="data/", load=False)
    pf.session.load_training_data(multiplier=None, difference=True)

    # autoregress_matrix = pf.session.learn_structure(sparsity=sparsity, infer_order=True)
    pf.session.learn_structure(sparsity=sparsity, infer_order=True)

    dataset_name = dataset_path.split("/")[-1].split(".")[0]
    output_path = "./results/" + dataset_name
    parent_sets = pf.session.get_dependencies(score="fit_error", write_to=output_path)

    # pf.session.timer.to_csv()
    return parent_sets


if __name__ == "__main__":
    fdx(
        dataset_path="../datasets/new_datasets/hate_crimes.csv",
        na_values="empty",
        sparsity=0.02,
    )
