"""initial schema

Revision ID: 48be4072fe58
Revises:
Create Date: 2022-06-01 18:37:12.396138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "48be4072fe58"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "conda_channel",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Unicode(length=255), nullable=False),
        sa.Column("last_update", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "conda_store_configuration",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("disk_usage", sa.BigInteger(), nullable=True),
        sa.Column("free_storage", sa.BigInteger(), nullable=True),
        sa.Column("total_storage", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "namespace",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Unicode(length=255), nullable=True),
        sa.Column("deleted_on", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "specification",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Unicode(length=255), nullable=False),
        sa.Column("spec", sa.JSON(), nullable=False),
        sa.Column("sha256", sa.Unicode(length=255), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sha256"),
    )
    op.create_table(
        "conda_package",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("channel_id", sa.Integer(), nullable=True),
        sa.Column("build", sa.Unicode(length=64), nullable=False),
        sa.Column("build_number", sa.Integer(), nullable=False),
        sa.Column("constrains", sa.JSON(), nullable=True),
        sa.Column("depends", sa.JSON(), nullable=False),
        sa.Column("license", sa.Text(), nullable=True),
        sa.Column("license_family", sa.Unicode(length=64), nullable=True),
        sa.Column("md5", sa.Unicode(length=255), nullable=False),
        sa.Column("name", sa.Unicode(length=255), nullable=False),
        sa.Column("sha256", sa.Unicode(length=64), nullable=False),
        sa.Column("size", sa.BigInteger(), nullable=False),
        sa.Column("subdir", sa.Unicode(length=64), nullable=True),
        sa.Column("timestamp", sa.BigInteger(), nullable=True),
        sa.Column("version", sa.Unicode(length=64), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["channel_id"],
            ["conda_channel.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "channel_id",
            "subdir",
            "name",
            "version",
            "build",
            "build_number",
            "sha256",
            name="_conda_package_uc",
        ),
    )
    op.create_table(
        "environment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("namespace_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Unicode(length=255), nullable=False),
        sa.Column("current_build_id", sa.Integer(), nullable=True),
        sa.Column("deleted_on", sa.DateTime(), nullable=True),
        # sa.ForeignKeyConstraint(['current_build_id'], ['build.id'], use_alter=True),
        sa.ForeignKeyConstraint(
            ["namespace_id"],
            ["namespace.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("namespace_id", "name", name="_namespace_name_uc"),
    )

    op.create_table(
        "solve",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("specification_id", sa.Integer(), nullable=False),
        sa.Column("scheduled_on", sa.DateTime(), nullable=True),
        sa.Column("started_on", sa.DateTime(), nullable=True),
        sa.Column("ended_on", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["specification_id"],
            ["specification.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "build",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("specification_id", sa.Integer(), nullable=False),
        sa.Column("environment_id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("QUEUED", "BUILDING", "COMPLETED", "FAILED", name="buildstatus"),
            nullable=True,
        ),
        sa.Column("size", sa.BigInteger(), nullable=True),
        sa.Column("scheduled_on", sa.DateTime(), nullable=True),
        sa.Column("started_on", sa.DateTime(), nullable=True),
        sa.Column("ended_on", sa.DateTime(), nullable=True),
        sa.Column("deleted_on", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["environment_id"],
            ["environment.id"],
        ),
        sa.ForeignKeyConstraint(
            ["specification_id"],
            ["specification.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_foreign_key(
        constraint_name="fk_environment_current_build_id_build_id",
        source_table="environment",
        referent_table="build",
        local_cols=["current_build_id"],
        remote_cols=["id"],
    )

    op.create_table(
        "solve_conda_package",
        sa.Column("solve_id", sa.Integer(), nullable=False),
        sa.Column("conda_package_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["conda_package_id"], ["conda_package.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["solve_id"], ["solve.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("solve_id", "conda_package_id"),
    )
    op.create_table(
        "build_artifact",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("build_id", sa.Integer(), nullable=True),
        sa.Column(
            "artifact_type",
            sa.Enum(
                "DIRECTORY",
                "LOCKFILE",
                "LOGS",
                "YAML",
                "CONDA_PACK",
                "DOCKER_BLOB",
                "DOCKER_MANIFEST",
                name="buildartifacttype",
            ),
            nullable=False,
        ),
        sa.Column("key", sa.Unicode(length=255), nullable=True),
        sa.ForeignKeyConstraint(
            ["build_id"],
            ["build.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "build_conda_package",
        sa.Column("build_id", sa.Integer(), nullable=False),
        sa.Column("conda_package_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["build_id"], ["build.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["conda_package_id"], ["conda_package.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("build_id", "conda_package_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("build_conda_package")
    op.drop_table("build_artifact")
    op.drop_table("solve_conda_package")
    op.drop_table("build")
    op.drop_table("solve")
    op.drop_table("environment")
    op.drop_table("conda_package")
    op.drop_table("specification")
    op.drop_table("namespace")
    op.drop_table("conda_store_configuration")
    op.drop_table("conda_channel")
    # ### end Alembic commands ###
