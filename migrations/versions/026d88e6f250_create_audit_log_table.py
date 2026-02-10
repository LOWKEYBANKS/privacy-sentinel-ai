"""create_audit_log_table

Revision ID: 026d88e6f250
Revises: 
Create Date: 2026-02-10 09:33:44.717405

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '026d88e6f250'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'analysis_audit_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content_hash', sa.String(length=16), nullable=False),
        sa.Column('risk_score', sa.Integer(), nullable=False),
        sa.Column('risk_count', sa.Integer(), nullable=False),
        sa.Column('client_ip', sa.String(length=45), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_content_hash', 'analysis_audit_log', ['content_hash'])
    op.create_index('idx_timestamp', 'analysis_audit_log', ['timestamp'])


def downgrade() -> None:
    op.drop_index('idx_timestamp', table_name='analysis_audit_log')
    op.drop_index('idx_content_hash', table_name='analysis_audit_log')
    op.drop_table('analysis_audit_log')
