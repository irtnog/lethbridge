"""model the state of the Second Thargoid War

Revision ID: a41aac16b9b4
Revises: 549d345a9779
Create Date: 2023-07-31 19:40:07.149465+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a41aac16b9b4"
down_revision = "549d345a9779"
branch_labels = None
depends_on = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


def upgrade_postgresql() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "thargoid_war",
        sa.Column("currentState", sa.String(), nullable=False),
        sa.Column("successState", sa.String(), nullable=False),
        sa.Column("failureState", sa.String(), nullable=False),
        sa.Column("progress", sa.Numeric(), nullable=False),
        sa.Column("daysRemaining", sa.Integer(), nullable=False),
        sa.Column("portsRemaining", sa.Integer(), nullable=False),
        sa.Column("successReached", sa.Boolean(), nullable=False),
        sa.Column("system_id64", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["system_id64"],
            ["system.id64"],
        ),
        sa.PrimaryKeyConstraint("system_id64"),
    )
    # ### end Alembic commands ###


def downgrade_postgresql() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("thargoid_war")
    # ### end Alembic commands ###


def upgrade_sqlite() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "thargoid_war",
        sa.Column("currentState", sa.String(), nullable=False),
        sa.Column("successState", sa.String(), nullable=False),
        sa.Column("failureState", sa.String(), nullable=False),
        sa.Column("progress", sa.Numeric(), nullable=False),
        sa.Column("daysRemaining", sa.Integer(), nullable=False),
        sa.Column("portsRemaining", sa.Integer(), nullable=False),
        sa.Column("successReached", sa.Boolean(), nullable=False),
        sa.Column("system_id64", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["system_id64"],
            ["system.id64"],
        ),
        sa.PrimaryKeyConstraint("system_id64"),
    )
    # ### end Alembic commands ###


def downgrade_sqlite() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("thargoid_war")
    # ### end Alembic commands ###
