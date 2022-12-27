
import pathlib

import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer


__here__ = pathlib.Path(__file__).parent
data_dir = __here__ / ".." / ".."/"data"

nlp_json_file = data_dir / "nlp_generated_skills.json"
pickle_file = data_dir/"job_title_embeddings.pkl"

assert nlp_json_file.exists()


def get_job_embeddings(job_titles):
    """Given an array of job titles, uses a SentenceTransformer model to concert the array to embeddings,
    and returns the embeddings values to be stored

    The model_name (taken from sentence_transformers) is a hard coded value, and can be changed to any of the models"""

    model_name = "all-MiniLM-L6-v2"

    model = SentenceTransformer(model_name)
    # Sentences are encoded by calling model.encode()
    embeddings = model.encode(job_titles)
    embedding_df = pd.DataFrame(index=job_titles, data=embeddings)

    return embedding_df


def create_job_title_embeddings():
    """Given a django query (from views.create_job_embeddings) produces an embedding matrix of skills and job titles

    User data will be combined with a sample of nlp generated data from nlp_generated_skills.json.
    The sample size is hardcoded (default to 10000), can be reduced to speed up processing time based on load testing

     The final matrix is stored as a pickle file in the api directory"""

    skill_sample_size = 10000

    nlp_jobs_df = pd.read_json(nlp_json_file)[["user_id", "job_title"]].iloc[0:skill_sample_size]
    df = nlp_jobs_df.copy()

    # converts to numpy array for speed
    unique_job_titles = df.drop_duplicates(subset=["job_title"]).dropna(axis=0)["job_title"].to_numpy()
    embeddings = get_job_embeddings(unique_job_titles)

    # todo - add to database in some way
    embeddings.to_pickle(pickle_file)

def return_similar_title_skills(job_title, user_skills, job_embeddings):
    """Given a job title, a list of all user skills, and previously generated job embeddings, returns likely skills

    The number of skills returned is a hard coded value (default to 10), as is the model name.
    The model assumes no skill ratings are provided (and defaults to each having a score of 1)
    """

    skill_count = 10
    model_name = "all-MiniLM-L6-v2"
    missing_ratings = False

    if job_title not in job_embeddings.index.to_list():
        user_skills = user_skills[user_skills["job_title"] != job_title].copy()

    unique_job_titles = user_skills.drop_duplicates(subset=["job_title"]).dropna(axis=0)["job_title"].to_numpy()

    if missing_ratings:
        skills_to_dummy = user_skills[["user_id", "skill_name"]]
        long_skills = skills_to_dummy.copy().rename(columns={"user_id": "user_id"})
        long_skills["rating"] = 1

    else:
        skills_to_dummy = user_skills[["user_id", "skill_name", "rating"]]
        long_skills = skills_to_dummy.copy().rename(columns={"user_id": "user_id"})

    if job_title is None:
        top_skills = (
            long_skills.groupby("skill_name")["rating"]
            .sum()
            .sort_values(ascending=False)
            .iloc[0:skill_count]
            .index.to_list()
        )
        return top_skills, None

    sparse_df = (
        long_skills.groupby(["user_id", "skill_name"])["rating"].sum().astype("Sparse[int]").unstack(fill_value=0)
    )

    model = SentenceTransformer(model_name)
    embeddings = model.encode(job_title)
    job_embedding = embeddings.reshape((1, embeddings.shape[0]))

    dist = np.linalg.norm(job_embedding - job_embeddings, axis=1)
    jobs_by_dist = np.argsort(dist)

    title_lookup = user_skills[["user_id", "job_title"]].drop_duplicates().set_index("user_id")

    dist_df = pd.DataFrame(columns=["distance", "job_title"])

    dist_df["distance"] = dist
    dist_df["job_title"] = unique_job_titles

    distance_title_df = (
        title_lookup.reset_index()
        .merge(dist_df, right_on="job_title", left_on="job_title", how="left")
        .set_index("user_id")
    )
    comparison_df = (
        distance_title_df.merge(sparse_df, left_index=True, right_index=True)
        .fillna(0)
        .copy()
        .drop(columns=["job_title", "job_title"])
    )
    similar_skill_dist = comparison_df.corr()["distance"].sort_values()

    returned_skills = list(similar_skill_dist.iloc[0:skill_count].index)
    returned_jobs = unique_job_titles[jobs_by_dist][0:skill_count]
    return returned_skills, returned_jobs


def recommend_relevant_job_skills(job_title):
    """Given a Django request of user skills and job title, and returns a list of recommended skills for that title

    All existing users skill will be combined with a sample from nlp_generated_skills.json
    """

    skill_sample_size = 10000

    nlp_jobs_df = pd.read_json(nlp_json_file)[["user_id", "skill_name", "job_title", "rating"]].iloc[
        0:skill_sample_size
    ]

    df = nlp_jobs_df.copy()

    loaded_embeddings = pd.read_pickle(pickle_file)

    similar_title_skills_returns = return_similar_title_skills(job_title, df, loaded_embeddings)
    return similar_title_skills_returns[0]
