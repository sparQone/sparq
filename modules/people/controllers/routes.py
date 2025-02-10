@blueprint.route("/updates")
@login_required
def updates():
    """Company updates page"""
    return render_template("updates/index.html",  # Changed from "people-updates.html"
                        active_page='updates',
                        title="Company Updates",
                        module_home='people_bp.people_home') 