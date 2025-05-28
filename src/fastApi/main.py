from fastapi import FastAPI, HTTPException, Body, UploadFile, File
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from profiler.core import *
import pandas as pd
import io
import tempfile
import os

app = FastAPI(title="Data Profiler API", description="API for data profiling and dependency analysis")

class ProfilerResponse(BaseModel):
    fds: List[str]
    dataset_name: str


@app.post("/profile-file", response_model=ProfilerResponse)
async def profile_dataset_from_file(
    file: UploadFile = File(...),
    na_values: str = "empty",
    sparsity: float = 0.0
):
    print(f"Received sparsityyyy: {sparsity}")
    print(f"Received na_values: {na_values}")
    try:
        # Create a temporary file to save the uploaded CSV
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
            # Read the uploaded file content
            content = await file.read()
            # Write to the temporary file
            temp_file.write(content)
            temp_path = temp_file.name
        
        try:
            # Process the file using the existing fdx function
            fds = fdx(
                dataset_path=temp_path,
                na_values=na_values,
                sparsity=sparsity
            )
            
            # Extract dataset name from the original filename
            dataset_name = file.filename.split("/")[-1].split(".")[0]

            print(fds)
            print(type(fds))
            
            return ProfilerResponse(
                fds=fds,
                dataset_name=dataset_name
            )
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing dataset: {str(e)}")


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
    fds = []
    for right, lefts in parent_sets.items():
        if len(lefts) > 0:
            fds.append(f"{', '.join(lefts)} -> {right}")
    # pf.session.timer.to_csv()
    return fds


@app.get("/")
def read_root():
    return {"message": "Welcome to the Data Profiler API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)