import os
import pickle
import click
import mlflow

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error


def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
def run_train(data_path: str):
    X_train, y_train = load_pickle(os.path.join(data_path, "green_train.pkl"))
    print("loaded train", X_train.shape)
    X_val, y_val = load_pickle(os.path.join(data_path, "green_val.pkl"))
    print("loaded val", X_val.shape)

    rf = RandomForestRegressor(max_depth=10, random_state=0)
    print('fitting..')
    rf.fit(X_train, y_train)
    print('fitted. predicting..')
    y_pred = rf.predict(X_val)
    print('predicted. evaluating..')

    rmse = root_mean_squared_error(y_val, y_pred)
    mlflow.log_metric(key="rmse_val", value=rmse)


if __name__ == '__main__':
    mlflow.sklearn.autolog(log_datasets=False)
    with mlflow.start_run():
        run_train()