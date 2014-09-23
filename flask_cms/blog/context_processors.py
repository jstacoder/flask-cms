from flask import url_for,session



def add_admin_head():
    return {'admin_head':admin_head}

def admin_head():
    return '''
    <div class="admin-head">
        <p><span class="glyphicon glyphicon-user"></span> Welcome {3}</p>
        <ul>
            <li><a href="{0}">Add Blog Post</a></li>
            <li><a href="{4}">Profile</a></li>
            <li><a href="{2}">Admin Menu</a></li>
            <li><a href="{1}">Logout</a></li>
        </ul>
    </div>
    '''.format(url_for('blog.add_post'),url_for('auth.logout'),url_for('admin.index'),session.get('email'),url_for('member.profile',member_id=session.get('user_id')))
