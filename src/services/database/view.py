from sqlalchemy_utils.view import CreateView, DropView


class View:
    selectable = None
    __table__ = None

    @classmethod
    def create(cls, op):
        cls.drop(op)
        create_sql = CreateView(cls.__table__.fullname, cls.selectable)
        op.execute(create_sql)
        for idx in cls.__table__.indexes:
            idx.create(op.get_bind())

    @classmethod
    def drop(cls, op):
        drop_sql = DropView(cls.__table__.fullname, cascade=True)
        op.execute(drop_sql)
