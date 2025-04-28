from app.extensions import db
from app.models.node import Node
from app.models.group import Group
from app.models.edge import Edge
from app.models.project import Project

# The order matters due to foreign key constraints (edges, nodes, groups, projects)
db.session.execute('TRUNCATE TABLE edge RESTART IDENTITY CASCADE;')
db.session.execute('TRUNCATE TABLE node RESTART IDENTITY CASCADE;')
db.session.execute('TRUNCATE TABLE "group" RESTART IDENTITY CASCADE;')
db.session.execute('TRUNCATE TABLE project RESTART IDENTITY CASCADE;')
db.session.commit()