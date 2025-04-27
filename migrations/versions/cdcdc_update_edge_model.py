"""Add edge_label to edges table

Revision ID: add_edge_label_column
Revises: accc094ef7ef
Create Date: 2024-01-30 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_edge_label_column'
down_revision = 'accc094ef7ef'  # This is your last migration ID
branch_labels = None
depends_on = None

def upgrade():
    # Add edge_label column to edges table
    op.add_column('edges', 
        sa.Column('edge_label', sa.String(255), nullable=True)
    )

def downgrade():
    # Remove edge_label column from edges table
    op.drop_column('edges', 'edge_label')