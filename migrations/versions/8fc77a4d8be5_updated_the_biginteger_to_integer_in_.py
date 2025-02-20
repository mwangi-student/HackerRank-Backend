"""updated the BigInteger to Integer in the models

Revision ID: 8fc77a4d8be5
Revises: cd939cd41be1
Create Date: 2025-02-20 12:49:33.107651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fc77a4d8be5'
down_revision = 'cd939cd41be1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assessment', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('tm_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)

    with op.batch_alter_table('assessmentinvite', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('assessment_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)
        batch_op.alter_column('student_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)
        batch_op.alter_column('invited_by',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)

    with op.batch_alter_table('discussions', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('assessment_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)
        batch_op.alter_column('student_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)
        batch_op.alter_column('tm_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)

    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('question_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)
        batch_op.alter_column('student_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)
        batch_op.alter_column('tm_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)

    with op.batch_alter_table('leaderboard', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('student_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)
        batch_op.alter_column('assessment_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)
        batch_op.alter_column('total_score',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)
        batch_op.alter_column('rank',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)

    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('assessment_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)

    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.alter_column('tm_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)

    with op.batch_alter_table('submission', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('student_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)
        batch_op.alter_column('question_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)
        batch_op.alter_column('assessment_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)
        batch_op.alter_column('score',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('submission', schema=None) as batch_op:
        batch_op.alter_column('score',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('assessment_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('question_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('student_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.alter_column('tm_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)

    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.alter_column('assessment_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('leaderboard', schema=None) as batch_op:
        batch_op.alter_column('rank',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('total_score',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('assessment_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('student_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.alter_column('tm_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('student_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('question_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('discussions', schema=None) as batch_op:
        batch_op.alter_column('tm_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('student_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('assessment_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('assessmentinvite', schema=None) as batch_op:
        batch_op.alter_column('invited_by',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('student_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('assessment_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('assessment', schema=None) as batch_op:
        batch_op.alter_column('tm_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)

    # ### end Alembic commands ###
