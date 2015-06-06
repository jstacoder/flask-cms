from jinja2 import Environment, BaseLoader
from core.views import col, row
jinja2_env = Environment(
    block_start_string="{{%",
    block_end_string="%}}",
    variable_start_string="{{{",
    variable_end_string="}}}",
    trim_blocks=True,
)

import sys

make_row = lambda y,**x: (row(y,**x),)

def make_layout(cols,use_footer=True,footer_cols=((6,'140'),(6,'140'))):
    cur = 1
    content = []
    rw = []
    for cls,h in cols:
        rw.append((cls,h),)
        cur += h
        if cur >= 12:
            content.append(rw)
            rw = []
            cur = 1
    return content
        

def get_rows(rows):
    rtn = []
    for r in rows:
        rtn.append(make_row(r['h'],r['cols']))
    return tuple(rtn)




def main():
    content_a = '510'
    content_b = '170'
    footer_h = '140'

    content = (
                row(content_a,
                    cols=(
                        col(2,content_a),
                        col(2,content_a,offset=8),
                    )
                ),
                row(content_b,
                    cols=(
                        col(4,content_b),
                        col(4,content_b),
                        col(4,content_b),
                    )
                ),      
    )
    footer = (
                row(footer_h,
                    cols=(
                        col(3,footer_h),
                        col(3,footer_h),
                        col(3,footer_h),
                        col(3,footer_h),
                    )
                ),
    )
    if len(sys.argv) > 1:
        print jinja2_env.from_string(
                open(sys.argv[1],'r').read()
        ).render(
                dict(
                    rows=content+footer,fluid=True
                )
        )

if __name__ == "__main__":
    main()
