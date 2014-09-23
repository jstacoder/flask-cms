# coding: utf-8
from imports import Page, Tag
from faker.factory import Factory
from sqlalchemy.exc import IntegrityError, InvalidRequestError

def get_faker():
    faker = Factory()
    return faker.create()

def make_tag():
    f = get_faker()
    t = Tag()
    t.name = f.word()
    t.description = f.text()
    try:
        t.save()
    except IntegrityError:
        from ext import db
        db.session.rollback
    except InvalidRequestError:
        from ext import db
        db.session.rollback
    else:
        return t


def make_page():
    f = get_faker()
    p = Page()
    p.name = f.uri_page()
    p.description = f.text()
    p.slug = f.slug()
    p.title = p.slug.upper()
    p.add_to_nav = True
    p.add_left_sidebar = False
    p.add_right_sidebar = False
    p.visible = True
    p.meta_title = p.slug.title()
    p.short_url = f.uri_path()
    p.date_added = f.date_time()
    p.save()
    return p
