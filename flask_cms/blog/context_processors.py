from flask import url_for,session,render_template_string



def add_admin_head():
    return {'admin_head':admin_head}

def admin_head():
    # type: ()-> str
    return render_template_string('''
    
    <div class="admin-head">
        <div class="admin-head2 hidden"><p>show menu</p></div>
        <div class='inner'>
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
    </div>
    <script>
        const hideBtn = document.getElementById("hide-btn")
        const menu = document.querySelector(".admin-head .inner")
        const show = document.querySelector(".admin-head .admin-head2")
        hideBtn.addEventListener("click", ()=> {
            menu.classList.add('hidden')
            show.classList.remove("hidden")            
        })
        show.addEventListener("click", ()=>{
            show.classList.add("hidden")
            menu.classList.remove("hidden")
        })
    </script>
    ''')
