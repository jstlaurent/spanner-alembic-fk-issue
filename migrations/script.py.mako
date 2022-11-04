<%!
    import re
    def _indent(text: str) -> str:
        text = re.compile(r"^", re.M).sub("    ", text).strip()
        text = re.compile(r" +$", re.M).sub("", text)
        return text
%>

"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    with op.get_context().autocommit_block():
        ${upgrades if upgrades else "pass" | _indent}


def downgrade():
    with op.get_context().autocommit_block():
        ${downgrades if downgrades else "pass" | _indent}
