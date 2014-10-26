
class LayoutManager:
    LAYOUTS = dict(
        ONE_COL_EMPTY=(12,),
        ONE_COL_LEFTBAR=(2,10), # 2 cols
        ONE_COL_RIGHTBAR=(10,2),# 2 cols 
        ONE_COL_BOTH=(2,8,2), # 3 cols
        TWO_COL_EMPTY=(6,6),
        TWO_COL_LEFTBAR=(2,5,5),
        TWO_COL_RIGHTBAR=(5,5,2),
        TWO_COL_BOTH=(2,4,4,2),
        THREE_COL_EMPTY=(4,4,4),
        THREE_COL_RIGHTBAR=(2,3,4,3),
        THREE_COL_LEFTBAR=(3,4,3,2),
    )
    ROWS = dict(
        BODY='760',
        FOOTER='150',
    )
    
    @staticmethod
    def get_cols(name):
        return LayoutManager.LAYOUTS[name.upper()]

    @staticmethod
    def get_height(name):
        return LayoutManager.ROWS[name.upper()]

