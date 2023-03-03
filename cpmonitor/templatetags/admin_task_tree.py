from treebeard.templatetags.admin_tree import result_tree as tb_result_tree
from treebeard.templatetags.admin_tree import register


@register.inclusion_tag("admin/tree_change_list_results.html", takes_context=True)
def result_tree(context, cl, request):
    """Overwriting treebeard to allow to drag-drop the tree structure even if filters are enabled."""
    result = tb_result_tree(context, cl, request)
    result["filtered"] = False
    return result
