"""add document hash

Revision ID: 6f653abd5603
Revises: e095fdfd4a48
Create Date: 2026-08-10 18:49:22.901019

"""
from typing import Sequence, Union
import hashlib

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f653abd5603'
down_revision: Union[str, Sequence[str], None] = 'e095fdfd4a48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add the column first so existing documents can be populated.
    op.add_column(
        "Documents",
        sa.Column(
            "document_hash",
            sa.Text(),
            nullable=True
        )
    )

    connection = op.get_bind()

    # Fetch existing documents.
    documents = connection.execute(
        sa.text("""
            SELECT document_id, document_bytes
            FROM "Documents"
            WHERE document_bytes IS NOT NULL
        """)
    ).fetchall()

    # Generate SHA-256 hash for every existing document.
    for document in documents:
        document_hash = hashlib.sha256(
            document.document_bytes
        ).hexdigest()

        connection.execute(
            sa.text("""
                UPDATE "Documents"
                SET document_hash = :document_hash
                WHERE document_id = :document_id
            """),
            {
                "document_hash": document_hash,
                "document_id": document.document_id
            }
        )

    # Existing documents should now all have a hash.
    op.alter_column(
        "Documents",
        "document_hash",
        nullable=False
    )

    # Prevent duplicate documents.
    op.create_unique_constraint(
        "uq_documents_document_hash",
        "Documents",
        ["document_hash"]
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "uq_documents_document_hash",
        "Documents",
        type_="unique"
    )

    op.drop_column(
        "Documents",
        "document_hash"
    )