from sqlalchemy import Table, MetaData, Column, Integer, String, event
from sqlalchemy.orm import registry, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.sql.schema import ForeignKey

from allocationvelo.domain import model_component_type, model_component, model_atelier

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


table_ateliers = Table(
    "tb_ateliers",
    metadata,
    Column("identifiant", String(255), primary_key=True),
)

table_components = Table(
    "tb_components",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("identifiant", String(100), nullable=False, index=True, unique=True),
    Column("atelier", String(255), ForeignKey("tb_ateliers.identifiant")),
    Column("component_name", String(50)),
    Column("type_component", String(50)),
    Column("parent_component_id", String(100)),
)


table_component_types = Table(
    "tb_component_types",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("identifiant", String(100), nullable=False, index=True, unique=True),
    Column("atelier", String(255), ForeignKey("tb_ateliers.identifiant")),
    Column("type_component", String(50)),
    Column("parent_type_id", String(100)),
)


def start_mappers():
    mapper_types = mapper_registry.map_imperatively(model_component_type.ComponentType, table_component_types)
    mapper_components = mapper_registry.map_imperatively(model_component.Component, table_components)
    mapper_registry.map_imperatively(
        model_atelier.Atelier,
        table_ateliers,
        properties={
            "component_types": relationship(mapper_types, collection_class=attribute_mapped_collection("identifiant")),
            "components": relationship(
                mapper_components, collection_class=attribute_mapped_collection("component_name")
            ),
        },
    )


@event.listens_for(model_atelier.Atelier, "load")
def receive_load(atelier, _):
    atelier.events = []


# table_association_component_types = Table(
#     "tb_component_types_list = Table(",
#     metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("parent_id", ForeignKey("tb_component_types.identifiant")),
#     Column("child_id", ForeignKey("tb_component_types.identifiant")),
# )

# table_component_types = Table(
#     "tb_component_types",
#     metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("identifiant", String(100), nullable=False, index=True, unique=True),
#     Column("type", String(50)),
# )

# table_components = Table(
#     "tb_components",
#     metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("identifiant", String(100), nullable=False, index=True, unique=True),
#     Column("component_type_id", String(100), nullable=True, index=True),
#     Column("install_on_id", String(100), nullable=True, index=True),
# )

# table_component_types_list = Table(
#     "tb_component_types_list = Table(",
#     metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("component_id", ForeignKey("tb_components.identifiant")),
#     Column("component_types_id", ForeignKey("tb_component_types.identifiant")),
# )


# table_components = Table(
#     "tb_components",
#     metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("identifiant", String(100), nullable=False, index=True, unique=True),
#     # Column("identifiant", Integer, nullable=False),
#     Column("component_type_id", Integer, ForeignKey("tb_component_types.id"), nullable=False),
#     Column("installed_on_id", Integer, ForeignKey("tb_components.id"), nullable=True),
#     # Column("install_status", Boolean, nullable=False),
# )

# installation = Table(
#     "installation",
#     metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("target_id", ForeignKey("components.id")),
#     Column("componenent_id", ForeignKey("components.identifiant")),
# )


# def start_mappers():
#     mapper_types = mapper_registry.map_imperatively(model_component_type.ComponentType, table_component_types)

#     # mapper_registry.map_imperatively(
#     model.ComponentDTO,
#     table_components,
#     properties={
#         "component_type": relationship(model.ComponentType),
#         "component_type_list_id": relationship(
#             mapper_types,
#             secondary=table_component_types_list,
#             collection_class=list,
#         ),
#     },
# )
# mapper_registry.map_imperatively(
#     Test,
#     table_components,
#     properties={
#         "component_type": relationship(model.ComponentType),
#         "components": relationship(
#             Test,
#             backref=backref("installed_on", remote_side=table_components.c.id),
#             collection_class=attribute_mapped_collection("component_type"),
#         ),
#         # "installed_on": relationship(Test, foreign_keys=table_components.c.installed_on_id),
#         # "installed_on": relationship(Test),
#     },
# )
