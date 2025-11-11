"""Initial migration - create predictions and feedback tables

Revision ID: 001
Revises: 
Create Date: 2025-11-09 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create predictions table
    op.create_table(
        'predictions',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('image_path', sa.String(500), nullable=False),
        sa.Column('pred_label', sa.String(200), nullable=False),
        sa.Column('pred_conf', sa.Float(), nullable=False),
        sa.Column('heatmap_path', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    
    # Create feedback table
    op.create_table(
        'feedback',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('prediction_id', sa.String(36), nullable=False),
        sa.Column('correct', sa.Boolean(), nullable=False),
        sa.Column('true_label', sa.String(200), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['prediction_id'], ['predictions.id'], ),
        sa.UniqueConstraint('prediction_id')
    )
    
    # Create indices
    op.create_index('idx_predictions_created_at', 'predictions', ['created_at'])
    op.create_index('idx_predictions_label', 'predictions', ['pred_label'])
    op.create_index('idx_feedback_prediction_id', 'feedback', ['prediction_id'])


def downgrade() -> None:
    op.drop_index('idx_feedback_prediction_id', table_name='feedback')
    op.drop_index('idx_predictions_label', table_name='predictions')
    op.drop_index('idx_predictions_created_at', table_name='predictions')
    op.drop_table('feedback')
    op.drop_table('predictions')
