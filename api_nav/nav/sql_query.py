get_tree = """
                    SELECT node.name, COUNT(parent.name)
                    FROM nav_nestedcategory AS node,
                         nav_nestedcategory AS parent
                    WHERE node.lft BETWEEN parent.lft AND parent.rgt and node.lft >= :lft  and node.rgt <= :rgt
                    GROUP BY node.name
                    ORDER BY node.lft;
"""
