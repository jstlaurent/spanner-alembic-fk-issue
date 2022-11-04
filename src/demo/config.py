from typing import Annotated

from pydantic import BaseSettings, constr


class Settings(BaseSettings):
    GCLOUD_PROJECT: Annotated[str, constr(strip_whitespace=True, min_length=1)] = 'local-gcp-emulators'
    SPANNER_INSTANCE: Annotated[str, constr(strip_whitespace=True, min_length=1)] = 'hydra-db-local'
    SPANNER_DATABASE: Annotated[str, constr(strip_whitespace=True, min_length=1)] = 'demo'

    @property
    def SPANNER_URL(self):
        if not self.SPANNER_DATABASE:
            raise ValueError('SPANNER_DATABASE setting needs to be defined.')

        return (
            'spanner+spanner://'
            f'/projects/{self.GCLOUD_PROJECT}'
            f'/instances/{self.SPANNER_INSTANCE}'
            f'/databases/{self.SPANNER_DATABASE}'
        )

    # A spanner session expires after 60 minutes of inactivity
    # https://cloud.google.com/spanner/docs/sessions#handle_deleted_sessions)
    # Because SqlAlchemy is pooling Sessions, when a session becomes inactive, the next call to the DB will fail
    # To avoid this behavior, we are forcing SqlAlchemy to recycle session older than 50 minutes.
    # For more details, check the section "Dealing with Disconnects" of the following doc
    # https://docs.sqlalchemy.org/en/14/core/pooling.html?highlight=reconnect#dealing-with-disconnects
    SPANNER_SESSION_RECYCLE_AGE: int = 50 * 60

    class Config:
        env_file = '.env'


settings = Settings()
