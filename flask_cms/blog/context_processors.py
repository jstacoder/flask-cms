from flask import url_for,session,render_template_string



def add_admin_head():
    return {'admin_head':admin_head}

def admin_head():
    return render_template_string('''
    <div class="admin-head">
        <p>{{get_icon('user',lib='font_awesome',size='lg')}} Welcome {{session.get('email')}}</p>        <ul>
            <li>
                <a href="{{url_for('blog.add_post')}}">Add Blog Post</a>
            </li>
            <li>
                <a href={#"{{url_for('member.profile',member_id=session.get('user_id'))}}#}#" id="hide-btn">Hide</a>
            </li>
            <li>
                <a href="{{url_for('admin.index')}}">Admin Menu</a>
            </li>
            <li>
                <a href="{{url_for('auth.logout')}}">Logout</a>
            </li>
        </ul>
    </div>
    ''')
